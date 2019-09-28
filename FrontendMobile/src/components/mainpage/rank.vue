<template>
  <mu-container>
    <mu-data-table
      :data="tableData"
      @row-click="userclick"
      :rowStyle="ratingcolor"
      :columns="columns"
      :loading="loading"
    >
      <template slot-scope="scope">
        <td>{{scope.row.rank}}</td>
        <td>{{scope.row.username}}</td>
        <td>{{scope.row.rating}}</td>
        <td>{{scope.row.score}}</td>
        <td>{{scope.row.des}}</td>
        <td>{{scope.row.ac}}</td>
        <td>{{scope.row.submit}}</td>
        <td>{{scope.row.rate}}</td>
      </template>
    </mu-data-table>
    <br>
    <mu-flex justify-content="center">
      <mu-pagination
        raised
        :page-count="5"
        :total="totaluser"
        :current.sync="currentpage"
        @change="handleCurrentChange"
      ></mu-pagination>
    </mu-flex>
  </mu-container>
</template>

<script>
export default {
  name: "rank",
  data() {
    return {
      currentpage: 1,
      pagesize: 10,
      totaluser: 10,
      tableData: [],
      loading: true,
      columns: [
        { title: "Rank", name: "rank", width:80 },
        { title: "UserID", name: "username", width:190  },
        { title: "Rating", name: "rating" },
        { title: "Score", name: "score" },
        { title: "Mood", name: "des" },
        { title: "AC", name: "ac" },
        { title: "Submit", name: "submit" },
        { title: "AC/Submit", name: "rate" }
      ]
    };
  },
  methods: {
    ratingcolor(  rowIndex,row ) {
      if (row.rating >= 3000) return "color:red;font-weight: bold;";
      if (row.rating >= 2600) return "color:#BB5E00;font-weight: bold;";
      if (row.rating >= 2200) return "color:#E6A23C;font-weight: bold;";
      if (row.rating >= 2050) return "color:#930093;font-weight: bold;";
      if (row.rating >= 1900) return "color:#0000AA;font-weight: bold;";
      if (row.rating >= 1700) return "color:#007799;font-weight: bold;";
      if (row.rating >= 1500) return "color:#227700;font-weight: bold;";
      if (row.rating >= 1350) return "color:#67C23A;font-weight: bold;";
      if (row.rating >= 1200) return "color:#909399;font-weight: bold;";
      return "color:#303133;font-weight: bold;";
    },
    userclick(index, row, event) {
      this.$router.push({
        name: "user",
        query: { username: row.username }
      });
    },

    getData(limit, offset) {
      this.loading = true;
      this.$axios
        .get("/userdata/?limit=" + limit + "&offset=" + offset)
        .then(response => {
          //console.log(response.data.results[0])
          for (var i = 0; i < response.data.results.length; i++) {
            //console.log(response.data.results[i]["ac"])
            response.data.results[i]["rank"] = offset + i + 1;
            response.data.results[i]["rate"] =
              (
                (response.data.results[i]["ac"] /
                  response.data.results[i]["submit"]) *
                100
              ).toFixed(2) + "%";

            if (response.data.results[i]["submit"] == 0) {
              response.data.results[i]["rate"] = "00.00%";
            }
          }
          this.tableData = response.data.results;
          this.totaluser = response.data.count;
          this.loading = false;
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
.el-carousel__item:nth-child(2n) {
  background-color: #afd1f1;
}

.el-carousel__item:nth-child(2n + 1) {
  background-color: #a7f5ff;
}
.image {
  width: 130px;
  height: 130px;
  display: block;
}
</style>
