<template>
  <el-card>
    <div slot="header">
      <b>Welcome to {{school}}</b>
    </div>
    <b>Version：3.2</b>
    <br>
    <h3>添加TodoList！</h3>
    <h3><a href="https://github.com/Linzecong/LPOJ" target="_blank" style="text-decoration: none;color:#409EFF;">Github (Star Me!)</a></h3>
    <h3><a href="https://docs.lpoj.cn" target="_blank" style="text-decoration: none;color:#67C23A;">Documentation</a></h3>
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