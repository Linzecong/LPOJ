// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import ElementUI from 'element-ui';
import 'element-ui/lib/theme-chalk/index.css';
import App from './App'
import router from './router'
import Vuex from 'vuex'
import md5 from 'js-md5';
import axios from 'axios';
import VueClipboard from 'vue-clipboard2'
Vue.use(VueClipboard)

Vue.use(Vuex)
Vue.config.productionTip = false
Vue.use(ElementUI);
Vue.prototype.$md5 = md5;


//开启debug模式
Vue.config.debug = true;
axios.defaults.withCredentials = true;
axios.defaults.baseURL = process.env.API_ROOT
Vue.prototype.$axios = axios;


const store = new Vuex.Store({
  state: {
  },
})

if (sessionStorage.acpro != "")
  store.state.acpro = sessionStorage.acpro

var curTime = new Date()
var secs = curTime.getTime()
var lastsecs = sessionStorage.storagetime
if (secs - lastsecs > 14 * 24 * 60 * 60 * 1000 && lastsecs != undefined)
  sessionStorage.setItem("username", "");
sessionStorage.setItem("storagetime", secs);


if (sessionStorage.username != ""&&sessionStorage.username!=undefined) {
  axios
    .get("/userdata/?username=" + sessionStorage.username)
    .then(response => {
      sessionStorage.setItem("rating", response.data[0].rating);
      var acpro = response.data[0].acpro.split("|")
      acpro.shift()
      store.state.acpro = acpro
      sessionStorage.setItem("acpro", acpro);
    });
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

