<template>
    <h1>{{ msg }}</h1>
</template>

<script>
export default {
  name: 'problemdetail',
  data () {
    return {
      msg: '欢迎来到LPOJ'
    }
  },
  created(){
    console.log(123);
    this.msg= this.$route.params.problemID
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>

h1{
  position: relative;
}

</style>
