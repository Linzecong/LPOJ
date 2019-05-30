# 前端开发

## Vue.js 介绍
Vue.js是一个构建 Web 界面的成熟的渐进式框架。它的目标是通过尽可能简单的接口来实现响应式的数据绑定和组合的视图组件，然后再将这些组件组合起来。它不仅上手容易，而且还便于与第三方库或既有项目整合。本系统将采用它进行开发，而且学习起来非常简单，拓展性非常好，用户可以使用自己的组件，非常简单且高效的自定义自己的页面。 同时结合Element的UI库进行精致的页面设计，给用户呈现一个较好的网页。同时使用Js中的Axios库，可以异步的向后台请求数据，然后使用Js解析后台返回的Json数据，通过Vue的数据绑定功能，可以非常简单且便利的将数据呈现给用户。

## 系统结构
Vue.js 是使用 MVVC模式开发，所谓MVVC即 Model,View, Viewmodel。其中Model层用于存储数据，ViewModel层用于网页元素的变化和实现数据之间的双向绑定。View层用于显示数据。相比于其他框架，我们可以花费更多的代码时间在View和Model层的编写上，从而不必关心中间的消息是如何传递的。因为Vue在底层通过观察者模式已经很好地帮我们实现了。因此本系统主要通过如下方式实现数据绑定：

对于每一个页面都以组件的形式开发，然后组件与组件之间互不干扰。页面之间的跳转通过路由实现。组件内的数据在Created函数中通过Axois库进行后台的API访问，获取后绑定到data中，然后再由vue的model数据绑定，自动的呈现给用户，在之前我们只需要定义好页面即可。前端的页面采用Element库开发。

## 工具与框架介绍

1. **Nodejs** 一个让JavaScript运行在服务端的开发平台
2. **NPM** JavaScript的包管理工具
3. **Webpack** Webpack是一个模块打包器。主要目标是将JS等各种文件打包在一起,打包后的文件用于在浏览器中使用
4. **Vue.js** 一个前端框架
5. **ElementUI** 一个用Vue实现的前端库
6. **Axios** 一个Js实现的用于发送http请求的库
7. 还有各种各样用Vue实现的前端库

## 安装LPOJ前端

在开始开发前，让我们先做一些准备工作！

首先要安装nodejs和npm

不同系统根据自己的情况来安装，如果是Ubuntu系统，执行如下命令即可。

```bash
sudo apt install nodejs
sudo apt install npm
```

接下来我们只需要安装各种库即可，得益于NPM，这里只需执行一个非常简单的命令即可。

```bash
cd Frontend
npm install
```

第一次安装需要等待大概二十多分钟左右，安装完毕后可以执行如下命令来查看前端是否能运行。

```bash
npm run dev
```

然后打开浏览器访问 **localhost:8080** 如果能看到页面，证明前端已成功安装。


## 打包前端

假如我们对前端做出了修改，需要发布到Web服务器上时，就需要把前端进行打包，得益于Webpack，我们只需要执行如下一个简单的命令即可

```bash
npm run build
```

打包完毕后，可以在Frontend文件夹中看到一个dist文件夹，我们只需要把里面的内容拷贝到Web服务器上的Web根目录即可。

## 安装Web服务器

根据自己需要安装自己喜欢的Web服务器即可。不同的Web服务器可能需要不同的设置，具体的话自行百度。也可以参阅部署教程来使用Nginx服务器

## 前端配置

在本节将介绍LPOJ中的一些前端设置，需要的话可以自行修改。在修改前，需要一定的前端知识。

### package.json

在**Frontend/package.json**中描述了本OJ用到的一些库，如果你需要使用其他版本，或者安装自己的库，只需执行如下命令即可

```bash
npm install yourpackage
```

### 打包设置

在 **Frontend/build**文件夹中，包含了一些打包和开发中的一些配置，需要的话自行修改。

### 代理设置

为了解决跨域问题和开发的便利性，这里使用了代理设置，将后端的地址代理一下来解决跨域问题。

在 **Frontend/config/index.js**文件中，修改

```js
proxyTable: {
    '/api': {
        target: 'http://localhost:8000', //此处是你的后端地址，不能有多余的斜杠
        changeOrigin: true,
        pathRewrite:{
            '^/api':'/' //重写的路径
        }
    }
},
```

其中**port**设置的是开发环境时访问的端口。

同时在 **dev.env.js**和**prod.env.js**中**API_ROOT**设置的就是代理访问的地址。本OJ设置的是**api**，所以最后访问时就是用**localhost:8080/api/yourapi/**来访问即可。具体的说明可以参考 **Vue 代理设置**

在**Frontend/src/main.js**中有关于**Axios**的设置，要修改的话自行百度。

```js
//开启debug模式
Vue.config.debug = true;
axios.defaults.withCredentials = true; //实现跨域访问
axios.defaults.baseURL = process.env.API_ROOT //设置根路径，代码中访问可以省略api三个字母。
Vue.prototype.$axios = axios;
```

## 开发说明

本系统采用Vue的组建式开发，整个前端由若干个组建组成，往后会一一说明。具体代码结构如下

1. **/src/components** 保存了网站主要的控件
1. **/src/components/admin** 保存了网站后台相关的控件
1. **/src/components/chart** 保存了网站图表相关的控件
1. **/src/components/contest** 保存了网站比赛页面相关的控件
1. **/src/components/mainpage** 保存了网站主要的页面的相关控件
1. **/src/components/problem** 保存了网站题目相关的控件
1. **/src/components/utils** 保存了网站一些有用的控件
1. **/src/components/wiki** 保存了网站Wiki页相关的控件
1. **/src/components/main.vue** 保存了网站的首页
1. **/src/router/index.js** 保存了网站的路由信息
1. **/src/App.vue** 保存了网站的入口
1. **/src/login.vue** 保存了登录控件
1. **/src/register.vue** 保存了注册控件
1. **/src/main.js** 保存了网站的Js入口
1. **/index.html** 默认网站

如果要修改网站，实际上也是添加或修改组件，然后导入到自己的网站中。

网站的大概的运行结构如下

1. 渲染index.html
1. 运行main.js生成网页
2. 将App.vue组件嵌入到index.html中，其中App.vue包括了菜单栏，登录框，注册框和页脚。
3. 根据路由，将各个页面渲染到App.vue的中间。


## 如何添加新页面

本节将会介绍如何在网站中添加一个自己的页面，并且可以通过地址栏访问它。

在阅读本节前，需要有简单的Vue知识。

### 编写Vue组件
首先我们在**components**目录中新建一个文件**mycom.vue**，其内容如下：

```html
<template>
  <el-row :gutter="12">
      <el-row :gutter="10">
        <welcomemessage></welcomemessage> <!-- 注册后的组件，可以直接引用来嵌入到页面中，详见Vue教程 -->
      </el-row>
      <el-row :gutter="10">
        {{msg}}
      </el-row>
  </el-row>
</template>

<script>
import welcomemessage from "@/components/utils/welcomemessage"; //导入现有的组件，或者自己开发的组件
export default {
  name: "mycom",
  components: {
    welcomemessage, //注册组件
  },
  data() {
    return {
      msg:"Hello World" //数据项，详见Vue教程
    };
  },
  created() {},
  methods: {}
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.el-row {
  margin-bottom: 12px;
}
</style>

```

如果学过Vue简单的组件开发，则会明白代码中内容的含义。

Vue的组件由三部分组成

1. **template** 网页主体
2. **script** 网页js
3. **style** 网页的CSS

具体编写，参考Vue教程。由于本OJ引入了**ElementUI**且在**main.js**中进行了全局注册,因此可以直接使用**ElementUI**的控件，如用**el-row**来实现排版。

### 添加路由信息

编写完自己的组件后，如果要给他添加一个路由，则需要修改 **/src/router/** 中的index.js

首先我们先**import**我们自己的组件，记住路径不能写错。

```js
import mycon from '@/components/mycon'
```
然后我们再添加自己的路由信息。我们在**routers**中添加一项内容

```js
{
    path: '/mycon', //路由地址
    name: 'mycon', //路由名称
    component: main //路由对应的控件
},
```

如无意外，我们已经成功的实现自己的页面现在执行 **npm run dev** 来运行自己的网站，然后通过浏览器访问

**localhost:8080/mycon/**

即可看到自己编写的控件的效果。

## 说明文档

本节接下来的内容将依次介绍本OJ现有的控件及其方法和具体实现，方便大家二次修改和引用。

本说明文档仅做简要说明，具体实现自行看详细代码。

### [main.js](https://github.com/Linzecong/LPOJ/blob/master/Frontend/src/main.js)

网页入口Js，全局注册了若干库，如**Vuex**和**ElementUI**

### [App.vue](https://github.com/Linzecong/LPOJ/blob/master/Frontend/src/App.vue)

包括了网页的菜单栏，登录按钮，注册按钮和页脚等。菜单栏通过**v-bind:router="true"**设置可以实现通过**index**属性，点击后直接跳转路由。

**component**

| name | 作用  | 
| :--  | :-- |
| [login](/dev/frontend.html#login-vue) | 登录框  | 
| [register](/dev/frontend.html#register-vue) | 注册框  | 

**data**

| name | 作用  | 
| :--  | :-- |
| activeIndex | 当前激活的菜单序号  | 
| school | OJ名称  | 
| loginshow | 是否显示登录框  | 
| username | 用户名  | 
| name | 昵称  | 
| isadmin | 是否是管理员  | 

**methods**

| name | 作用  | 补充说明 |
| :--  | :-- | :-- |
| loginopen | 打开登录框  | 通过ref实现 |
| registeropen | 打开注册框  | 通过ref实现 | 
| handleCommand | 处理用户菜单栏的路由跳转 | 通过$router.push直接跳转 |

**mounted**

> 实现了是否是管理员的判断和初始化OJ名称

### [login.vue](https://github.com/Linzecong/LPOJ/blob/master/Frontend/src/login.vue)

实现了登录框，直接通过**el-dialog**实现

**data**

| name | 作用  | 
| :--  | :-- |
| dialogLoginVisible | 是否显示登录框  | 
| form | 登录信息的表单  |

**methods**

| name | 作用  | 补充说明 |
| :--  | :-- | :-- |
| open | 打开登录框  | visible.sync实现 |
| loginClick | 登录函数  | 先将密码MD5哈希，然后提交表单，根据返回结果判断是否登录成功，登录成功后再获取一些必要的信息后自动刷新一下来更新内容。 | 

### [register.vue](https://github.com/Linzecong/LPOJ/blob/master/Frontend/src/register.vue)

实现了注册框，直接通过**el-dialog**实现

**data**

| name | 作用  | 
| :--  | :-- |
| dialogRegisterVisible | 是否显示注册框  | 
| form | 注册信息的表单  |

**methods**

| name | 作用  | 补充说明 |
| :--  | :-- | :-- |
| open | 打开注册框  | visible.sync实现 |
| registerClick | 注册函数  | 先判断填写信息是否满足要求，然后将密码MD5哈希，然后提交表单，根据返回结果判断是否注册成功 | 

### [main.vue](https://github.com/Linzecong/LPOJ/blob/master/Frontend/src/components/main.vue)

实现了首页，主要是将各种控件组合在一起。

**component**

| name | 作用  | 
| :--  | :-- |
| [rankchart](/dev/frontend.html#rankchart-vue) | 个人排名图表  | 
| [teamchart](/dev/frontend.html#teamchart-vue) | 队伍排名图表  | 
| [ojmessage](/dev/frontend.html#ojmessage-vue) | 留言板  | 
| [welcomemessage](/dev/frontend.html#welcomemessage-vue) | 左上角的控件  | 
| [topuser](/dev/frontend.html#topuser-vue) | 排行榜前十用户  | 
| [soulrow](/dev/frontend.html#soulrow-vue) | 顶部的三个卡片控件  | 
| [ratingrule](/dev/frontend.html#ratingrule-vue) | OJ规则控件  | 
| [contestmini](/dev/frontend.html#contestmini-vue) | 近期比赛控件  | 

**data**

| name | 作用  | 
| :--  | :-- |
| label | 一些标题  |

### [admin.vue](https://github.com/Linzecong/LPOJ/blob/master/Frontend/src/components/mainpage/admin.vue)

**component**

| name | 作用  | 
| :--  | :-- |

**data**

| name | 作用  | 
| :--  | :-- |

**methods**

| name | 作用  | 补充说明 |
| :--  | :-- | :-- |

**mounted**

> 

### [billboard.vue](https://github.com/Linzecong/LPOJ/blob/master/Frontend/src/components/mainpage/billboard.vue)
### [blog.vue](https://github.com/Linzecong/LPOJ/blob/master/Frontend/src/components/mainpage/blog.vue)
### [contest.vue](https://github.com/Linzecong/LPOJ/blob/master/Frontend/src/components/mainpage/contest.vue)
### [problem.vue](https://github.com/Linzecong/LPOJ/blob/master/Frontend/src/components/mainpage/problem.vue)
### [rank.vue](https://github.com/Linzecong/LPOJ/blob/master/Frontend/src/components/mainpage/rank.vue)
### [setting.vue](https://github.com/Linzecong/LPOJ/blob/master/Frontend/src/components/mainpage/setting.vue)
### [statue.vue](https://github.com/Linzecong/LPOJ/blob/master/Frontend/src/components/mainpage/statue.vue)
### [user.vue](https://github.com/Linzecong/LPOJ/blob/master/Frontend/src/components/mainpage/user.vue)
### [wiki.vue](https://github.com/Linzecong/LPOJ/blob/master/Frontend/src/components/mainpage/wiki.vue)
### rankchart.vue
### ratingchart.vue
### teamchart.vue
### problemdetail.vue
### algorithmselect.vue
### blogmini.vue
### contestmini.vue
### ojmessage.vue
### prostatistice.vue
### ratingrule.vue
### soulrow.vue
### statusmini.vue
### topuser.vue
### welcomemessage.vue
### wikidetail.vue
### contestannounce.vue
### contestcomment.vue
### contestdetail.vue
### contestoverview.vue
### contestproblem.vue
### contestrank.vue
### contestsubmit.vue
### contesttutorial.vue
### adminaddcontest.vue
### adminaddproblem.vue
### adminboard.vue
### adminchangecontest.vue
### adminchangepro.vue
### adminmanageuser.vue
### adminrejudge.vue
### adminsetting.vue
### admintrainning.vue
### algorithm.vue
### code.vue
### trainning.vue
### basic.vue
### dp.vue
### ds.vue
### editalgorithm.vue
### geometry.vue
### graph.vue
### intro.vue
### math.vue
### search.vue
### string.vue
### codeedit.vue
### viewcode.vue
### viewcodedetail.vue
### trainningdetail.vue


