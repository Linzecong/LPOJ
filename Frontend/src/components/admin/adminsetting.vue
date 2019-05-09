<template>
  <el-row>
    <el-row>
      <el-form label-position="right">
        <el-form-item label="学校名称">
          <el-input v-model="name" placeholder="GDUFS" style="width:200px"></el-input>
          <el-button type="primary" @click="click">提交</el-button>
        </el-form-item>
      </el-form>
    </el-row>
  </el-row>
</template>

<script>
export default {
  name: "adminsetting",
  data() {
    return {
      name: ""
    };
  },
  methods: {
    click() {
      if (this.name == "无") {
        this.$axios
          .post("/settingboard/1/", {
            schoolname: this.name
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
            schoolname: this.name
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
        if (res.data.length > 0) this.name = res.data[0].schoolname;
        else this.name = "无";
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
