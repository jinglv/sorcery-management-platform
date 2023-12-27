# vue-admin-template
## Build Setup

```bash
# clone the project
git clone https://github.com/PanJiaChen/vue-admin-template.git

# enter the project directory
cd vue-admin-template

# install dependency
npm install

# develop
npm run dev
```

This will automatically open http://localhost:9528

## Build

```bash
# build for test environment
npm run build:stage

# build for production environment
npm run build:prod
```

## Advanced

```bash
# preview the release environment effect
npm run preview

# preview the release environment effect + static resource analysis
npm run preview -- --report

# code format check
npm run lint

# code format check and auto fix
npm run lint -- --fix
```

## 问题

1. npm run dev启动报错：`Error: error:0308010C:digital envelope routines::unsupported`，解决方法：执行`export NODE_OPTIONS=--openssl-legacy-provider`

## 使用icon

- https://www.iconfont.cn/

## 下拉选中选择树形结构

- vue-treeselect： https://javasoho.com/vuetreeselect/index_cn.html#node

- select和tree组合实现：https://cloud.tencent.com/developer/article/1945603

## vue-json-viewer

https://www.npmjs.com/package/vue-json-viewer

## echarts

官网：https://echarts.apache.org/zh/index.html

全局引用，在main.js

```
// 引入echarts-5.0
import * as echarts from 'echarts'
Vue.prototype.$echarts = echarts
```

## Ace文本编辑器使用

官方网站：https://ace.c9.io/

```
npm install ace-builds --save
```

- 如何使用: https://blog.csdn.net/weixin_52137696/article/details/130320172(https://blog.csdn.net/qq_27971677/article/details/121991097 注：有些老)
- 子父组件传值问题：https://blog.csdn.net/xdlhw1997/article/details/121062178

## 富文本编辑器--wangeditor

官网：https://www.wangeditor.com/

```
npm i wangeditor --save
```

### 代码高亮

```npm
npm install highlight.js -S
```

## 内容复制到剪切板

```
npm install vue-clipboard2 --save
```

## 聊天对话框使用

JwChat官网：https://codegi.gitee.io/jwchatdoc/
学习地址：https://blog.csdn.net/Jie_1997/article/details/120154717

## 环境部署

1. 编写nginx配置文件
2. 编写Dockerfile
3. 工程目录下生产环境编译打包
    - npm run build:prod
4. Docker构建镜像并运行容器
    - docker build -t sorcery_management_front .
    - docker run --name sorcery_management_front -d -p 9528:80 -v /root/sorcery-management-platform/backend/static:/root/static sorcery_management_front