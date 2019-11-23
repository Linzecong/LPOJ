<template>
  <el-card>
    <div slot="header">
      <b>Welcome to {{school}}</b>
    </div>
    <b>Version：3.3</b>
    <br>
    <h3><a href="https://www.lpoj.cn/problemdetail?problemID=5777" target="_blank" style="text-decoration: none;color:#409EFF;">添加模板题支持！快来试试这题</a></h3>
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


    var sb = this.$store.state.sb
    if( sb ==undefined){
      this.$axios
      .get("/settingboard/")
      .then(res => {
        if (res.data.length > 0) this.school = res.data[0].ojname;
        else this.school = "LPOJ";
        this.$store.state.sb = res.data
      })
      .catch(error => {
        this.$message.error(
          "服务器错误！" + "(" + JSON.stringify(error.response.data) + ")"
        );
      });
    }
    else{
      if (sb.length > 0) this.school = sb[0].ojname;
        else this.school = "LPOJ";
    }


  },
};
</script>

<style  scoped>
</style>