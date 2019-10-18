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
      languagelist: ["C++","C","Python3","Swift5.1","Java"]
    };
  },
  created() {
    this.$axios
      .get("/settingboard/")
      .then(res => {
        if (res.data.length > 0) {
          this.languagelist = res.data[0].openlanguage.split("|");
        } 
      })
      .catch(error => {
        this.$message.error(
          "服务器错误！" + "(" + JSON.stringify(error.response.data) + ")"
        );
      });
  },
  methods: {}
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>
