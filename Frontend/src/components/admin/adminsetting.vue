<template>
  <el-row>
    <el-row>
      <el-form label-position="right">
        <el-form-item label="学校名称">
          <el-input v-model="name" placeholder="School Name" style="width:200px"></el-input>
          <el-input v-model="ojname" placeholder="OJ Name" style="width:200px"></el-input>
        </el-form-item>
        <el-form-item label="是否开启WIKI（用于比赛时防止查阅资料）">
          <el-switch v-model="wikiopen" active-text="开启" inactive-text="关闭"></el-switch>
        </el-form-item>
      </el-form>
      <el-button style="margin-top:20px;" type="primary" @click="click">提交</el-button>
    </el-row>
  </el-row>
</template>

<script>
export default {
  name: "adminsetting",
  data() {
    return {
      name: "",
      ojname: "",
      wikiopen:true,
    };
  },
  methods: {
    click() {
      if (this.name == "无") {
        this.$axios
          .post("/settingboard/", {
            schoolname: this.name,
            ojname: this.ojname,
            openwiki:this.wikiopen
          })
          .then(res => {
            this.$message.success("提交成功！");
          })
          .catch(error => {
            this.$message.error(
              "服务器错误！" + "(" + JSON.stringify(error.response.data) + ")"
            );
          });
      } else {
        this.$axios
          .put("/settingboard/1/", {
            schoolname: this.name,
            ojname: this.ojname,
            openwiki:this.wikiopen
          })
          .then(res => {
            this.$message.success("提交成功！");
          })
          .catch(error => {
            this.$message.error(
              "服务器错误！" + "(" + JSON.stringify(error.response.data) + ")"
            );
          });
      }
    }
  },
  created() {
    this.$axios
      .get("/settingboard/")
      .then(res => {
        if (res.data.length > 0) {
          this.name = res.data[0].schoolname;
          this.ojname = res.data[0].ojname;
          this.wikiopen = res.data[0].openwiki
        } else this.name = "无";
      })
      .catch(error => {
        this.$message.error(
          "服务器错误！" + "(" + JSON.stringify(error.response.data) + ")"
        );
      });
  }
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.el-tag + .el-tag {
  margin-left: 10px;
}
</style>
