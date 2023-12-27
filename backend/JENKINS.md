# Jenkins调度平台

## Jenkins满足所有调度平台需求

| 需求        | Jenkins对应关系                 |
| ----------- | ------------------------------- |
| 调用脚本    | 在构建的shell中可以直接执行命令 |
| 分布式      | 节点管理                        |
| 支持API调用 | Jenkins对外开发的API            |
| 报告获取    | 多种报告插件                    |

## Jenkins API的使用

Jenkins官方文档：

- https://www.jenkins.io/doc/book/using/remote-access-api/
- https://www.jenkins.io/doc/book/managing/cli/

Python第三方库

- https://github.com/pycontribs/jenkinsapi

## Jenkins常见API

### 站点API

- 创建job
- 复制job
- ...

### Job API

- 启用Job
- 执行Job
- ...

### Build API

- 根据BuildNumber获取build信息
- ...

## JenkinsAPI使用添加token

## Python JenkinsAPI使用

安装Jenkinsapi：`pip install jenkinsapi`

### 基础调用

- 配置Jenkins服务地址
- 配置Jenkins用户名
- 配置Jenkins用户token

```python
from jenkinsapi.jenkins import Jenkins

# Jenkins服务地址
BASE_URL = "http://8.140.112.xxx:8080/jenkins"
# Jenkins用户名
USERNAME = "admin"
# Jenkins用户token
PASSWORD = "1119bcaaffedd5b97b42863a50758f3239"


def get_version():
    """
    获取Jenkins实例对象，关联Jenkins服务
    """
    jenkins = Jenkins(BASE_URL, USERNAME, PASSWORD)
    return jenkins.version
```

- 根据job名称获取job对象
- 构建job
- 获取当前job最后一次完成构建的编号

```python
def build_job():
    """
    jenkins job操作
    """
    # Jenkins job名称
    JOB = "test"
    # 获取Jenkins对象
    jenkins = Jenkins(BASE_URL, USERNAME, PASSWORD)
    # 根据job名称获取job对象
    ck_job = jenkins.get_job(JOB)
    # 构建job
    ck_job.invoke()
    # 获取当前job最后一次完成构建的编号
    last_build_number = ck_job.get_next_build_number()
    return last_build_number
```

### 带有参数的Job调用

前提是Jenkins配置的Job带有参数

- 通过build_params关键字传递构建参数

  ```python
  # 要求使用字典格式
  # key值为Jenkins中设定的参数名称
  # value为给参数传递的值
  def build_job_params(params_key="gitlab", params_value="test"):
      """
      Jenkins执行带有参数的job
      """
      # Jenkins job名称
      JOB = "test"
      # 获取Jenkins对象
      jenkins = Jenkins(BASE_URL, USERNAME, PASSWORD)
      # 根据job名称获取job对象
      ck_job = jenkins.get_job(JOB)
      # 构建job
      ck_job.invoke(build_params={params_key: params_value})
      # 获取当前job最后一次完成构建的编号
      last_build_number = ck_job.get_next_build_number()
      return last_build_number
  ```
