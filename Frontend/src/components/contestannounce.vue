<template>
  <el-card>
    <p :key="index" v-for="(item,index) in tabledata" v-html="item"/>
  </el-card>
</template>

<script>
export default {
  name: "contestannounce",
  data() {
    return {
      tabledata: []
    };
  },
  methods:{
    reflash(){
      this.tabledata=[]
      this.$axios
            .get("/contestannouncement/?contestid" + this.$route.params.contestID)
            .then(response => {

              for(let i=0;i<response.data.length;i++){
              this.tabledata.push(response.data[i]["announcement"]) 
              }

            });
    }
  },
  mounted() {
    this.reflash()
  }
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>

</style>
