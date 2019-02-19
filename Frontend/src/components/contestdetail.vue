<template>
    <h1>{{ msg }}</h1>
</template>

<script>
export default {
  name: 'contestdetail',
  data () {
    return {
      msg: this.$route.params.contestID
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>

h1{
  position: relative;
}

</style>
