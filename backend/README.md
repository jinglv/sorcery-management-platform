# 安装依赖

- django-ninja
- requests
- faker
- jmespath
- pystache

# 接口文档查看

服务启动后，访问：http://{{ip:port}}/api/docs

# 切换MySQL数据源

创建文件my.cnf内容如下：

```
[client]
host = 127.0.0.1
port = 3306
database = Name
user = USER
password = PASSWORD
default-character-set = utf8
```

在settings.py中将DATABASES修改为如下内容：

```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'OPTIONS': {
            'read_default_file': os.path.join(BASE_DIR, 'my.cnf')
         }
    }
}
```

初始化数据库：CREATE DATABASE {database_name};

安装模块

```
python3 -m pip install pymysql
```

在项目的主目录下的`__init__.py`加入如下内容：

```
import pymysql

pymysql.version_info = (1, 4, 3, "final", 0)  # 指定了pymysql的版本：1.4.3,按照你版本修改
pymysql.install_as_MySQLdb()
```

执行命令

```
# 检查表结构是否变更
./manage.py makemigrations

# 同步表数据
./manage.py migrate
```

# HttpRunner执行

- httprunner == 2.5.7

验证安装

```shell
hrun -V
```

报错：ImportError: cannot import name 'soft_unicode' from 'markupsafe' (
/usr/local/var/pyenv/versions/3.9.0/envs/venv3.9.0/lib/python3.9/site-packages/markupsafe/__init__.py)

markupsafe版本不兼容，需要降下版本，安装httprunner时，markupsafe版本是2.1.3（最新版本），需要降到1.1.1版本

- MarkupSafe == 1.1.1

这时候在执行`hrun -V`可以正常展示

```shell
(venv3.9.0) lvjing@bogon backend % hrun -V
2.5.7
```

## 分层概念

- 接口定义（api），接口信息的详细描述
- 测试用例（testcase）应该是完整且独立的，每条测试用例应该是都可以独立运行的，且是测试步骤（teststep）的有序集合，每一个测试步骤对应一个API的请求描述
- 测试用例集（testsuite）是测试用例的无需集合，集合中的测试用例应该都是相互独立，不存在先后依赖关系的，如果确实存在先后依赖管理，那就需要再测试用例中完成依赖的处理

## 层级结构

- debugtalk.py放置在项目根目录下，假设为PRJ_ROOT_DIR/debugtalk.py
- .env放置在项目根目录下，路径为PRJ_ROOT_DIR/.env
- 接口定义(API)放置在PRJ_ROOT_DIR/api/目录下
- 测试用例（testcase）放置在PRJ_ROOT_DIR/testcase/目录下
- 测试用例集（testsuite）文件必须放置在PRJ_ROOT_DIR/testsuite/目录下
- data文件夹：存储参数化文件，或者项目依赖的文件，路径为PRJ_ROOT_DIR/data/
- reports文件夹：存储HTML测试报告，生成路径为PRJ_ROOT_DIR/reports/

## HttpRunner执行类

```python
from httprunner.api import HttpRunner

runner = HttpRunner(
    failfast=True,  # 用例只要有一个失败/异常，就不继续执行了
    save_tests=True,  # 保存用例，生成logs目录下保存
    log_level="INFO",  # 日志等级
    log_file="test.log"
)
path_or_tests = './api/demo_api.yml'
# path_or_tests 指定运行用例的地址
summary = runner.run(path_or_tests)
```

## Celery异步运行项目

官方Github地址：https://github.com/celery/celery

Django框架使用Celery地址：https://docs.celeryq.dev/en/latest/django/first-steps-with-django.html#using-celery-with-django

Celery扮演生产者和消费者的角色

Celery本身不提供队列服务，推荐使用Redis或者RabbitMQ实现队列服务，所以在使用Celery提前是要安装部署好Redis或者MQ等消息队列服务

Docker安装Redis教程：https://blog.csdn.net/weixin_45821811/article/details/116211724

### 使用步骤

1. 定义Celery，在proj/proj/目录下创建celery.py
2. 在celery.py写入如下内容
   ```python
    import os
 
    from celery import Celery
     
    # Set the default Django settings module for the 'celery' program.
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'proj.settings')
     
    app = Celery('proj')
     
    # Using a string here means the worker doesn't have to serialize
    # the configuration object to child processes.
    # - namespace='CELERY' means all celery-related configuration keys
    #   should have a `CELERY_` prefix.
    app.config_from_object('django.conf:settings', namespace='CELERY')
     
    # Load task modules from all registered Django apps.
    app.autodiscover_tasks()
     
     
    @app.task(bind=True, ignore_result=True)
    def debug_task(self):
        print(f'Request: {self.request!r}')
 
   ```
   注意：将代码中项目的名称改为对应的工程名称
3. 在proj/proj/__init__.py中写入如下代码
    ```python
    # This will make sure the app is always imported when
    # Django starts so that shared_task will use this app.
    from .celery import app as celery_app
    
    __all__ = ('celery_app',)
    ```
4. 在settings.py加入如下内容，本案例的消息中间件使用的是Redis（提前是安装配置完成Redis，并可以正常连接Redis）
   ```python
   #  celery 配置连接redis
   # 链接Redis 'redis://用户名:密码@127.0.0.1:6379'
   CELERY_BROKER_URL = 'redis://:123456@127.0.0.1:6379'
   CELERY_RESULT_BACKEND = 'redis://:123456@127.0.0.1:6379'
   
   CELERY_TASK_SERIALIZER = 'json'
   CELERY_RESULT_SERIALIZER = 'json'
   CELERY_ACCEPT_CONTENT = ['json']
   CELERY_TIMEZONE = 'Asia/Shanghai'
   CELERY_TASK_TRACK_STARTED = True
   # 设置任务超时时间，单位秒，超时即中止，执行下个任务
   CELERY_TASK_TIME_LIMIT = 30 * 60
   ```
5. 启动一个worker，命令如下：
   ```python
   celery -A Django项目名称 worker -l info
   ```
   运行示例
   ```python
   (venv3.9.0) lvjing@bogon backend % celery -A backend worker -l info
 
   -------------- celery@bogon v5.3.1 (emerald-rush)
   --- ***** ----- 
   -- ******* ---- macOS-13.4.1-x86_64-i386-64bit 2023-07-24 08:43:16
   - *** --- * --- 
     - ** ---------- [config]
     - ** ---------- .> app:         backend:0x10ec961c0
     - ** ---------- .> transport:   redis://:**@127.0.0.1:6379//
     - ** ---------- .> results:     redis://:**@127.0.0.1:6379/
     - *** --- * --- .> concurrency: 12 (prefork)
     -- ******* ---- .> task events: OFF (enable -E to monitor tasks in this worker)
     --- ***** ----- 
      -------------- [queues]
                     .> celery           exchange=celery(direct) key=celery
                

   [tasks]
     . apis.tasks.add
     . backend.celery.debug_task
   
   [2023-07-24 08:43:16,806: INFO/MainProcess] Connected to redis://:**@127.0.0.1:6379//
   [2023-07-24 08:43:16,815: INFO/MainProcess] mingle: searching for neighbors
   [2023-07-24 08:43:17,844: INFO/MainProcess] mingle: all alone
   [2023-07-24 08:43:17,883: INFO/MainProcess] celery@bogon ready.

   ```
   看到这一句的时候Connected to redis://:**@127.0.0.1:6379//，就说明Redis已经链接成功了
6. 完成以上配置后，就可以使用`@shared_task`装饰器，配置接口可异步执行
   ```python
   from celery import shared_task

   @router.get("/task/demo", auth=None)
   def task_demo(request):
       """
       简单celery调用示例
       """
       res = add.delay(10, 20)
       print(res.task_id)
       return response(item=res.task_id)
   
   
   @shared_task
   def add(x, y):
       return x + y
   ```
   执行接口：http://127.0.0.1:8000/api/apis/task/demo
   返回结果：
   ```json
   {
    "success": true,
    "error": {
        "code": "",
        "message": ""
    },
    "result": "898bae88-f762-40bc-9cbc-80a743c25412"
   }
   ```
   result展示的是返回的task_id

### 报错

celery启动报错：

```shell
[2023-06-08 01:07:11,671: WARNING/MainProcess] D:\program\ANACONDA3\envs\medical\lib\site-packages\celery\worker\consumer\consumer.py:498: CPendingDeprecationWarning: The broker_connection_retry configuration setting will no longer determine
whether broker connection retries are made during startup in Celery 6.0 and above.
If you wish to retain the existing behavior for retrying connections on startup,
you should set broker_connection_retry_on_startup to True.
  warnings.warn(
```

解决：在settings.py文件设置

```python
CELERY_BROKER_CONNECTION_RETRY_ON_STARTUP = True
```

## 环境部署

生成依赖包文件requirements.txt

```shell
pip freeze > requirements.txt
```

## mysql数据库

```shell
docker run -d --name mysql -p 3306:3306 -v /root/data/mysql:/var/lib/mysql -e MYSQL_ROOT_PASSWORD=123456 mysql:latest
```

### 生产环境部署访问静态资源404

### 生产环境跨域配置

### uwsgi

常用命令

```shell
# 启动
uwsgi --ini uwsgi.ini
# 停止 
uwsgi --stop uwsgi.pid
# 重启
uwsgi --reload uwsgi.pid
# 停止所有uwsgi进程
pkill -f uwsgi -9
# 查看所有uwsgi进程
ps aux | grep uwsgi
```