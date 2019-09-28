<template>
  <mu-container>
    <mu-card>
      <mu-card-title title="Blogs"></mu-card-title>

      <mu-card-text>
        <mu-data-table
          :columns="columns"
          :data="tableData"
          @row-click="blogclick"
        >
          <template slot-scope="scope">
            <td>{{scope.row.username}}</td>
            <td>{{scope.row.title}}</td>
            <td>{{scope.row.time}}</td>
          </template>
        </mu-data-table>
      </mu-card-text>
    </mu-card>
    <br />
    <mu-flex justify-content="center">
      <mu-pagination
        raised
        :page-count="5"
        :total="totalblog"
        :current.sync="currentpage"
        @change="handleCurrentChange"
      ></mu-pagination>
    </mu-flex>
  </mu-container>
</template>

<script>
import moment from "moment";
export default {
  name: "rank",
  data() {
    return {
      currentpage: 1,
      pagesize: 10,
      totalblog: 10,
      tableData: [],
      columns: [
        { title: "UserName", name: "username" },
        { title: "Title", name: "title" },
        { title: "Time", name: "time" }
      ]
    };
  },
  methods: {
    blogclick(index,row) {
      window.open(row.url);
    },

    getData(limit, offset) {
      this.$axios
        .get("/blog/?limit=" + limit + "&offset=" + offset)
        .then(response => {
          for (var i = 0; i < response.data.results.length; i++) {
            response.data.results[i].time = moment(
              response.data.results[i].time
            ).format("YYYY-MM-DD HH:mm:ss");
          }
          this.tableData = response.data.results;
          this.totalblog = response.data.count;
        })
        .catch(error => {
          this.$toast.error(
            "服务器错误！" + "(" + JSON.stringify(error.response.data) + ")"
          );
        });
    },

    handleCurrentChange(val) {
      this.currentpage = val;
      this.getData(this.pagesize, (this.currentpage - 1) * this.pagesize);
    }
  },
  created() {
    this.getData(10, 0);
  }
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.title {
  font-weight: bold;
}
</style>
