<template>
  <el-card>
    <div slot="header">
      <b>Welcome to {{school}}</b>
    </div>
    <b>Version：2.1</b>
    <br>
    <h3>Safer and More Robust!</h3>
    <h3><a href="https://github.com/Linzecong/LPOJ" target="_blank" style="text-decoration: none;color:#409EFF;">Github (Star Me!)</a></h3>
  </el-card>
</template>

<script>
export default {
  name: "welcomemessage",
  data() {
    return {
      school:"LPOJ",
    };
  },
  created() {
    this.$axios
      .get("/settingboard/")
      .then(res => {
        if (res.data.length > 0) this.school = res.data[0].ojname;
        else this.school = "LPOJ";
      })
      .catch(error => {
        this.$message.error(
          "服务器错误！" + "(" + JSON.stringify(error.response.data) + ")"
        );
      });
  },
};
</script>

<style  scoped>
</style>