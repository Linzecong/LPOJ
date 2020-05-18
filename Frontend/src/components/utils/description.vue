<template>
  <div>

    <center>
    <h2 style="color:#409EFF;">欢迎来到本OJ</h2>
    
    <h3>这是一个基于Vue.js和Django的轻量级在线评测系统</h3>
    <h3>有任何好的意见可以在左下角留言板留言</h3>
    <h3><a style="text-decoration: none;color:#409EFF;" target="_blank" href="https://www.lpoj.cn">欢迎访问公网版本 www.lpoj.cn</a></h3>
    <h3><a style="text-decoration: none;color:#67C23A;" target="_blank" href="https://docs.lpoj.cn/doc/oj.html#status%E8%AF%B4%E6%98%8E">使用文档</a></h3>
    
    </center>
    <el-divider></el-divider>
    <h2>FAQ：</h2>
    <h4>判题机使用Linux系统</h4>
    <h4>Java: 主类名字请写更改为Main后再提交。Java提供3倍的时限</h4>
    <h4>Python: Python不提供编译过程, 所以一切因为Python代码编写错误引发的错误, 均判为Runtime Error</h4>
    <h4>C++：支持__int128</h4>
    <h4>判题机会自动的去掉行末空格（不会去掉换行）</h4>
    <el-divider></el-divider>
    <h3>编译参数:</h3>
    <h4>C++: g++ -O2 -std=c++14</h4>
    <h4>C: g++ -O2 -std=c11</h4>
    <h4>Java: JDK-8</h4>
    <br>

  </div>
</template>

<script>
export default {
  name: "description",
  data() {
    return {

    };
  },
  methods:{
    
  }
};
</script>

<style  scoped>
</style>