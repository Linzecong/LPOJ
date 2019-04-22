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
axios.defaults.withCredentials=true;
axios.defaults.baseURL = process.env.API_ROOT
Vue.prototype.$axios = axios;



const store = new Vuex.Store({
  state: {
  },
})

if(localStorage.acpro!="")
  store.state.acpro=localStorage.acpro

if (localStorage.username != "") {
  axios
    .get("/userdata/?username=" + localStorage.username)
    .then(response => {
      localStorage.setItem("rating", response.data[0].rating);
      var acpro = response.data[0].acpro.split("|")
      acpro.shift()
      store.state.acpro=acpro
      localStorage.setItem("acpro", acpro);
    });
} else {
  localStorage.setItem("username", "");
  localStorage.setItem("name", "");
  localStorage.setItem("rating", "");
  localStorage.setItem("type", "");
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

