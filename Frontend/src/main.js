// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'
import router from './router'
import Vuex from 'vuex'
import md5 from 'js-md5';
import axios from 'axios';
import VueClipboard from 'vue-clipboard2'
import 'babel-polyfill' //兼容IE6

import ElementUI from 'element-ui';
import 'element-ui/lib/theme-chalk/index.css';
Vue.use(ElementUI);


import { ExpansionPanel } from 'muse-ui';
Vue.use(ExpansionPanel);


Vue.use(VueClipboard)
Vue.use(Vuex)

Vue.config.productionTip = false
Vue.prototype.$md5 = md5;

//开启debug模式
Vue.config.debug = true;
axios.defaults.withCredentials = true;
axios.defaults.baseURL = process.env.API_ROOT
Vue.prototype.$axios = axios;

const store = new Vuex.Store({
  state: {
    loginip:"后台获取",
    logininfo:"后台获取"
  },
})

axios
.get("/settingboard/")
.then(res => {
  store.state.sb = res.data
});


if (sessionStorage.username != ""&&sessionStorage.username!=undefined) {
  //获取一下用户的AC题目，全局保存。
  axios
    .get("/userdata/?username=" + sessionStorage.username)
    .then(response => {
      sessionStorage.setItem("rating", response.data[0].rating);
      var acpro = response.data[0].acpro.split("|")
      acpro.shift() //因为最前面会多出一个空，去掉它
      store.state.acpro = acpro
      sessionStorage.setItem("acpro", acpro);
    });
    //更新一下本地的rating，如果没有登录则刷新一下，更新成功返回updated，否则返回ok
  axios
    .get("/updaterating/")
    .then(response => {
      if (response.data == "ok") {
        sessionStorage.setItem("username", "");
        sessionStorage.setItem("name", "");
        sessionStorage.setItem("rating", "");
        sessionStorage.setItem("type", "");
        sessionStorage.setItem("acpro", "");
        router.go(0)
      }
    });
} else {
  sessionStorage.setItem("username", "");
  sessionStorage.setItem("name", "");
  sessionStorage.setItem("rating", "");
  sessionStorage.setItem("type", "");
  sessionStorage.setItem("acpro", "");
}



new Vue({
  el: '#app',
  router,
  components: { App },
  store,
  template: '<App/>',
  render: h => h(App),
  created() {
    
  }
})

