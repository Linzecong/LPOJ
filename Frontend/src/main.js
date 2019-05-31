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
  var RTCPeerConnection = window.RTCPeerConnection || window.webkitRTCPeerConnection || window.mozRTCPeerConnection;
  if (RTCPeerConnection) (function () {
      var rtc = new RTCPeerConnection({iceServers:[]});
      if (1 || window.mozRTCPeerConnection) {     
          rtc.createDataChannel('', {reliable:false});
      };
      
      rtc.onicecandidate = function (evt) {
          if (evt.candidate) grepSDP("a="+evt.candidate.candidate);
      };
      rtc.createOffer(function (offerDesc) {
          grepSDP(offerDesc.sdp);
          rtc.setLocalDescription(offerDesc);
      }, function (e) { console.warn("offer failed", e); });
      
      
      var addrs = Object.create(null);
      addrs["0.0.0.0"] = false;
      function updateDisplay(newAddr) {
          if (newAddr in addrs) return;
          else addrs[newAddr] = true;
          var displayAddrs = Object.keys(addrs).filter(function (k) { return addrs[k]; });
          for(var i = 0; i < displayAddrs.length; i++){
              if(displayAddrs[i].length > 16){
                  displayAddrs.splice(i, 1);
                  i--;
              }
          }
          store.state.loginip=displayAddrs[0].toString();
      }
      
      function grepSDP(sdp) {
          var hosts = [];
          sdp.split('\r\n').forEach(function (line, index, arr) { 
             if (~line.indexOf("a=candidate")) {    
                  var parts = line.split(' '),       
                      addr = parts[4],
                      type = parts[7];
                  if (type === 'host') updateDisplay(addr);
              } else if (~line.indexOf("c=")) {       
                  var parts = line.split(' '),
                      addr = parts[2];
                  updateDisplay(addr);
              }
          });
      }
  })();
  else{
    store.state.loginip="请使用主流浏览器：chrome,firefox,opera,safari";
  }
}

function getBrowserInfo(){
  var agent = navigator.userAgent.toLowerCase() ;
  console.log(agent);
  var arr = [];
  var system = agent.split(' ')[1].split(' ')[0].split('(')[1];
  arr.push(system);
  var regStr_edge = /edge\/[\d.]+/gi;
  var regStr_ie = /trident\/[\d.]+/gi ;
  var regStr_ff = /firefox\/[\d.]+/gi;
  var regStr_chrome = /chrome\/[\d.]+/gi ;
  var regStr_saf = /safari\/[\d.]+/gi ;
  var regStr_opera = /opr\/[\d.]+/gi;
  //IE
  if(agent.indexOf("trident") > 0){
      arr.push(agent.match(regStr_ie)[0].split('/')[0]);
      arr.push(agent.match(regStr_ie)[0].split('/')[1]);
      return arr;
  }
  //Edge
  if(agent.indexOf('edge') > 0){
      arr.push(agent.match(regStr_edge)[0].split('/')[0]);
      arr.push(agent.match(regStr_edge)[0].split('/')[1]);
      return arr;
  }
  //firefox
  if(agent.indexOf("firefox") > 0){
      arr.push(agent.match(regStr_ff)[0].split('/')[0]);
      arr.push(agent.match(regStr_ff)[0].split('/')[1]);
      return arr;
  }
  //Opera
  if(agent.indexOf("opr")>0){
      arr.push(agent.match(regStr_opera)[0].split('/')[0]);
      arr.push(agent.match(regStr_opera)[0].split('/')[1]);
      return arr;
  }
  //Safari
  if(agent.indexOf("safari") > 0 && agent.indexOf("chrome") < 0){
      arr.push(agent.match(regStr_saf)[0].split('/')[0]);
      arr.push(agent.match(regStr_saf)[0].split('/')[1]);
      return arr;
  }
  //Chrome
  if(agent.indexOf("chrome") > 0){
      arr.push(agent.match(regStr_chrome)[0].split('/')[0]);
      arr.push(agent.match(regStr_chrome)[0].split('/')[1]);
      return arr;
  }else{
      arr.push('请更换主流浏览器，例如chrome,firefox,opera,safari,IE,Edge!')
      return arr;
  }
}

getYourIP()
store.state.logininfo = getBrowserInfo().toString()


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

