<template>
  <div>
    <el-option v-for="item in languagelist" :key="item" :label="item" :value="item"></el-option>
  </div>
</template>

<script>
export default {
  name: "languageselect",

  data() {
    return {
      languagelist: ["C++","C","Python3","Python2","Swift5.1","Java"]
    };
  },
  created() {

    var sb = this.$store.state.sb
    if( sb ==undefined){
      this.$axios
      .get("/settingboard/")
      .then(res => {
        if (res.data.length > 0) {
          this.languagelist = res.data[0].openlanguage.split("|");
        } 
        this.$store.state.sb = res.data
      })
      .catch(error => {
        this.$message.error(
          "服务器错误！" + "(" + JSON.stringify(error.response.data) + ")"
        );
      });
    }
    else{
      if (sb.length > 0) {
          this.languagelist = sb[0].openlanguage.split("|");
        } 
    }

  },
  methods: {}
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>
