<template>
  <el-row :gutter="10">
    <el-col :span="5">
      <el-row :gutter="10">
        <el-card>
          <h3>{{ msg }}</h3>
          <h3>当前版本：1.1</h3>
          <h3>支持语言：C/C++</h3>
          <h3>编译参数：g++ -O2 -std=c++11</h3>
        </el-card>
        <el-card style="margin-top:10px">
        <h4>Top User</h4>
        <el-table :data="tableData" border style="width: 100%" @cell-click="userclick">
          <el-table-column type="index" width="40"></el-table-column>
          <el-table-column prop="username" label="User"></el-table-column>
          <el-table-column prop="score" label="Score"></el-table-column>
        </el-table>
        </el-card>
      </el-row>
    </el-col>
    <el-col :span="19">
      <el-card>
        <rankchart></rankchart>
      </el-card>
      <el-card style="margin-top:10px">
        <center><h4>Current Status</h4></center>
        <statue></statue>
      </el-card>
    </el-col>
  </el-row>
</template>

<script>
import statue from "@/components/statue";
import rankchart from "@/components/rankchart";
export default {
  components: {
    rankchart,
    statue
  },
  name: "main",
  data() {
    return {
      msg: "欢迎来到LPOJ",
      tableData: []
    };
  },
  created() {
    this.$axios
      .get("/api/userdata/?limit=10&offset=0")
      .then(response => {
        this.tableData = response.data.results;
      })
      .catch(error => {
        this.$message.error("服务器错误！" + "(" + error + ")");
      });
  },
  methods: {
    userclick(row, column, cell, event){
      this.$router.push({
          name: "user",
          query: { username: row.username }
        });
    },
  }
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>
