<template>
  <el-card>
    <el-table :data="tableData" @cell-click="blogclick" size="medium">

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
    <el-pagination
      @size-change="handleSizeChange"
      @current-change="handleCurrentChange"
      :current-page="currentpage"
      :page-sizes="[20, 40, 60]"
      :page-size="pagesize"
      layout="total, sizes, prev, pager, next, jumper"
      :total="totalblog"
    ></el-pagination>
  </el-card>
</template>

<script>
import moment from "moment";
export default {
  name: "rank",
  data() {
    return {
      currentpage: 1,
      pagesize: 20,
      totalblog: 10,
      tableData: [],
    };
  },
  methods: {
    blogclick(row, column, cell, event) {
      window.open(row.url)
    },

    getData(limit, offset) {
      this.$axios
        .get("/blog/?limit=" + limit + "&offset=" + offset)
        .then(response => {

          for (var i = 0; i < response.data.results.length; i++) {
            response.data.results[i].time=moment(
              response.data.results[i].time
            ).format("YYYY-MM-DD HH:mm:ss");
          }
          this.tableData = response.data.results;
          this.totalblog = response.data.count;
        })
        .catch(error => {
          this.$message.error("服务器错误！" + "(" + JSON.stringify(error.response.data) + ")");
        });
    },
    handleSizeChange(val) {
      this.pagesize = val;
      this.getData(this.pagesize, (this.currentpage - 1) * this.pagesize);
    },
    handleCurrentChange(val) {
      this.currentpage = val;
      this.getData(this.pagesize, (this.currentpage - 1) * this.pagesize);
    }
  },
  created() {
    this.getData(20, 0);
  }
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.title {
  font-weight: bold
}
</style>
