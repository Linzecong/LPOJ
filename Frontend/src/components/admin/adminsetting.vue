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
        <el-button style="margin-top:20px;" type="primary" @click="click">提交</el-button>
      </el-form>
      <br>
      <h3>Banner设置</h3>
      <el-table :data="tableData" size="small">
        <el-table-column prop="msg" label="Banner"></el-table-column>
        <el-table-column prop="time" label="Time"></el-table-column>
        <el-table-column fixed="right" label="操作" width="160">
          <template slot-scope="scope">
            <el-button @click="delmsg(scope.row)" type="danger" size="small">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
      <br>
      <el-input v-model="msg" placeholder="请输入Banner，支持Html" style="width:400px"></el-input>
      <el-button type="primary" @click="sendbanner">提交</el-button>
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
      wikiopen: true,
      tableData: [],
      msg: ""
    };
  },
  methods: {
    sendbanner() {
      this.$axios
        .post("/banner/", { msg: this.msg })
        .then(res => {
          this.$message.success("提交成功！");
          this.reflash();
        })
        .catch(error => {
          this.$message.error(
            "服务器错误！" + "(" + JSON.stringify(error.response.data) + ")"
          );
        });
    },
    reflash() {
      this.$axios
        .get("/banner/")
        .then(res => {
          this.tableData = res.data;
        })
        .catch(error => {
          this.$message.error(
            "服务器错误！" + "(" + JSON.stringify(error.response.data) + ")"
          );
        });
    },
    delmsg(row) {
      this.$axios.delete("/banner/" + row.id + "/").then(response => {
        this.$message.success("删除成功！");
        this.reflash();
      });
    },
    click() {
      if (this.name == "无") {
        this.$axios
          .post("/settingboard/", {
            schoolname: this.name,
            ojname: this.ojname,
            openwiki: this.wikiopen
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
            openwiki: this.wikiopen
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
          this.wikiopen = res.data[0].openwiki;
        } else this.name = "无";
        this.reflash();
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
