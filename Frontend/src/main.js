// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import ElementUI from 'element-ui';
import 'element-ui/lib/theme-chalk/index.css';
import App from './App'
import router from './router'
import VueResource from 'vue-resource';
import Vuex from 'vuex'
import md5 from 'js-md5';
import axios from 'axios';
import {codemirror} from 'vue-codemirror'
import 'codemirror/lib/codemirror.css'
Vue.use(codemirror)

Vue.use(Vuex)
Vue.config.productionTip = false
Vue.use(ElementUI);
Vue.use(VueResource)
Vue.prototype.$md5 = md5;

Vue.prototype.$ip = "localhost";
Vue.prototype.$port = "8000";


//开启debug模式
Vue.config.debug = true;
axios.defaults.withCredentials=true;
Vue.prototype.$axios = axios;


const store = new Vuex.Store({
  state: {
  },
})

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

