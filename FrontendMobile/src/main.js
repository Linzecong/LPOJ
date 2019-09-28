// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import { Table, TableColumn } from 'element-ui';
import 'element-ui/lib/theme-chalk/index.css';
import App from './App'
import router from './router'
import Vuex from 'vuex'
import md5 from 'js-md5';
import axios from 'axios';
import VueClipboard from 'vue-clipboard2'
import 'babel-polyfill' //兼容IE6
import MuseUI from 'muse-ui';
import 'muse-ui/dist/muse-ui.css';
import Toast from 'muse-ui-toast';

Vue.use(VueClipboard)
Vue.use(Vuex)
Vue.config.productionTip = false

Vue.use(Table)
Vue.use(TableColumn)

Vue.use(MuseUI);
Vue.prototype.$md5 = md5;
Vue.use(Toast);

//开启debug模式
Vue.config.debug = true;
axios.defaults.withCredentials = true;
axios.defaults.baseURL = process.env.API_ROOT
Vue.prototype.$axios = axios;

const store = new Vuex.Store({
  state: {
  },
})



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

function getYourIP(){
  
  store.state.loginip='mobile';
    
}


try {
  getYourIP()
  store.state.logininfo = 'mobile'
} catch (error) {
  console.log(error)
}



new Vue({
  el: '#app',
  router,
  components: { App },
  store,
  template: '<App/>',
  render: h => h(App),
  created() {
    if(this.$store.state.loginip.indexOf("请使用主流浏览器")>=0){
      this.$toast.success("推荐使用主流浏览器，例如Chrome,Firefox,Opera,Safari等，如果是360浏览器，请关闭极速模式！")
    }
  }
})

