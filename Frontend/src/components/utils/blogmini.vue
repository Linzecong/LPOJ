<template>
  <el-card>
    <div slot="header">
      <b>最新博客</b>
      <el-button
        style="float: right;"
        type="primary"
        @click="allblog"
        size="mini"
      >查看全部</el-button>
    </div>
    <el-table :data="tableData3" @cell-click="blogclick" size="small">
      <el-table-column prop="username" label="User" :width="150"></el-table-column>
      <el-table-column prop="title" label="Title (Click to view content)">
        <template slot-scope="scope">
          <el-popover trigger="hover" placement="top" :width="500">
            <p>摘要: {{ scope.row.summary }}</p>
            <div slot="reference" class="name-wrapper">
              <b>{{ scope.row.title }}</b>
            </div>
          </el-popover>
        </template>
      </el-table-column>
      <el-table-column prop="time" label="Time" :width="160"></el-table-column>
    </el-table>
  </el-card>
</template>

<script>
import moment from "moment";
export default {
  name: "blogmini",
  data() {
    return {
      tableData3: []
    };
  },
  methods: {
    blogclick(row, column, cell, event) {
      window.open(row.url);
    },
    allblog() {
      this.$router.push({
        name: "blog"
      });
    }
  },
  created() {
    this.$axios
      .get("/blog/?limit=10&offset=0")
      .then(response => {
        for (var i = 0; i < response.data.results.length; i++) {
          response.data.results[i].time = moment(
            response.data.results[i].time
          ).format("YYYY-MM-DD HH:mm:ss");
        }
        this.tableData3 = response.data.results;
      })
      .catch(error => {
        this.$message.error(
          "服务器错误！" + "(" + JSON.stringify(error.response.data) + ")"
        );
      });
  }
};
</script>

<style  scoped>
</style>