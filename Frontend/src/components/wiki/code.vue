<template>
  <el-card>
    <center>
      <h2>欢迎来到代码库</h2>
      <h3>你可以选择你要查看的代码库或者编辑自己的代码库</h3>
    </center>
    <br>
    选择一个版本 或
    <el-button @click="edit" type="primary" style="margin-left:15px;">编辑自己的代码</el-button>
    <el-table :data="tableData" @cell-click="userclick">
      <el-table-column type="index"></el-table-column>
      <el-table-column prop="username" label="User" :width="200"></el-table-column>
      <el-table-column prop="des" label="Des" :width="200"></el-table-column>
      <el-table-column prop="time" label="Last Edit Time"></el-table-column>
    </el-table>
  </el-card>
</template>

<script>
import moment from "moment";
export default {
  name: "mbcode",
  data() {
    return {
      tableData: []
    };
  },
  created() {
    this.$axios
      .get("/mbcode/")
      .then(response => {
        for (let i = 0; i < response.data.length; i++)
          response.data[i].time = moment(response.data[i].time).format(
            "YYYY-MM-DD HH:mm:ss"
          );
        this.tableData = response.data;
      })
      .catch(error => {
        this.$message.error(
          "服务器错误！" + "(" + JSON.stringify(error.response.data) + ")"
        );
      });
  },
  methods: {
    edit() {
      this.$router.push({
        name: "codeedit"
      });
    },
    userclick: function(row, column, cell, event) {
      this.$router.push({
        name: "viewcode",
        params: { username: row.username }
      });
    }
  }
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>
