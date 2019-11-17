<template>
  <mu-card>
    <mu-card-title :title="'Welcome to '+school"></mu-card-title>
    <mu-card-text>
      <b>Mobile Version：1.0</b>
      <br />
      <h3>
        <a
          href="https://github.com/Linzecong/LPOJ"
          target="_blank"
          style="text-decoration: none;color:#409EFF;"
        >Github (Star Me!)</a>
      </h3>
      <h3>
        <a
          href="https://docs.lpoj.cn"
          target="_blank"
          style="text-decoration: none;color:#67C23A;"
        >Documentation</a>
      </h3>
      服务器流量需要一定的开支！欢迎捐赠，一起把LPOJ做好~我会把你们的名字放在LPOJ首页！谢谢大家支持！~~<br><br>捐赠地址：<a href="https://docs.lpoj.cn/faq/">https://docs.lpoj.cn/faq/</a>
    </mu-card-text>
  </mu-card>
</template>

<script>
export default {
  name: "welcomemessage",
  data() {
    return {
      school: "LPOJ"
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
        this.$toast.error(
          "服务器错误！" + "(" + JSON.stringify(error.response.data) + ")"
        );
      });
  }
};
</script>

<style  scoped>
</style>