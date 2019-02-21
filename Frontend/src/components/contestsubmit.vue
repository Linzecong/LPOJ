<template>
    <el-card><statue></statue></el-card>
</template>

<script>
import statue from '@/components/statue'
export default {
  name: 'contestsubmit',
  data () {
    return {
      msg: 'contestsubmit'
    }
  },
  components: {
    statue,
  },
  created(){
    
  },
  methods:{
    aaa(){
      console.log(123124)
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
