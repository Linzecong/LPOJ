<template>
<el-card>
    <h1>{{ msg }}</h1>
    <h1> 当前版本：1.0 </h1>
    <h1> 支持语言：C/C++ </h1>
    <h1> 编译参数：g++ -O2 -std=c++11 </h1>
</el-card>

</template>

<script>
export default {
  name: 'main',
  data () {
    return {
      msg: '欢迎来到LPOJ'
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>

</style>
