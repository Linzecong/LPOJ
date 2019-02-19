<template>
  <el-row>
    <el-table :data="tableData" @cell-click="contestclick" :default-sort="{prop: 'begintime', order: 'descending'}">
      <el-table-column prop="id" label="ID" :width="100"></el-table-column>
      <el-table-column prop="title" label="Title"></el-table-column>
      <el-table-column prop="level" label="Level">
        <template slot-scope="scope1">
          <el-tag
            id="leveltag"
            size="medium"
            :type="contestlevel(scope1.row.level)"
            disable-transitions
            hit
          >{{ scope1.row.level }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="begintime" label="Begin Time"></el-table-column>
      <el-table-column prop="lasttime" label="Duration"></el-table-column>
      <el-table-column prop="type" label="Type"></el-table-column>
      <el-table-column prop="auth" label="Openness">
        <template slot-scope="scope">
          <el-tag
            id="leveltag"
            size="medium"
            disable-transitions
            hit
            :type="contestauth(scope.row.auth)"
          >{{ scope.row.auth }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="creator" label="Owner"></el-table-column>
    </el-table>
    <el-pagination
      @size-change="handleSizeChange"
      @current-change="handleCurrentChange"
      :current-page="currentpage"
      :page-sizes="[10, 20, 30, 50]"
      :page-size="pagesize"
      layout="total, sizes, prev, pager, next, jumper"
      :total="totalcontest"
    ></el-pagination>
  </el-row>
</template>

<script>
export default {
  name: "contest",
  data() {
    return {
      currentpage: 1,
      pagesize: 10,
      totalcontest: 10,
      tableData: []
    };
  },
  methods: {
    contestclick: function(row, column, cell, event) {
      this.$router.push({
        name: "contestdetail",
        params: { contestID: row.id }
      });
    },
    contestlevel: function(type) {
      if (type == "Easy") return "info";
      if (type == "Medium") return "success";
      if (type == "Hard") return "";
      if (type == "VeryHard") return "warning";
      if (type == "ExtremelyHard") return "danger";
    },
    contestauth: function(type) {
      if (type == "Public") return "success";
      if (type == "Protect") return "warning";
      if (type == "Private") return "danger";
    },
    handleSizeChange(val) {
      this.pagesize = val;

      this.$http
        .get(
          "http://" +
            this.$ip +
            ":" +
            this.$port +
            "/contestinfo/?limit=" +
            this.pagesize +
            "&offset=" +
            (this.currentpage - 1) * this.pagesize
        )
        .then(response => {
          for (var i = 0; i < response.data.results.length; i++) {
            if (response.data.results[i]["level"] == "1")
              response.data.results[i]["level"] = "Easy";
            if (response.data.results[i]["level"] == "2")
              response.data.results[i]["level"] = "Medium";
            if (response.data.results[i]["level"] == "3")
              response.data.results[i]["level"] = "Hard";
            if (response.data.results[i]["level"] == "4")
              response.data.results[i]["level"] = "VeryHard";
            if (response.data.results[i]["level"] == "5")
              response.data.results[i]["level"] = "ExtremelyHard";

            response.data.results[i]["begintime"] =
              response.data.results[i]["begintime"].split("T")[0] +
              " " +
              response.data.results[i]["begintime"].split("T")[1].split(".")[0];

            response.data.results[i]["lasttime"] =
              response.data.results[i]["lasttime"] + " S";

            if (response.data.results[i]["auth"] == "1")
              response.data.results[i]["auth"] = "Public";
            if (response.data.results[i]["auth"] == "2")
              response.data.results[i]["auth"] = "Private";
            if (response.data.results[i]["auth"] == "0")
              response.data.results[i]["auth"] = "Protect";
          }
          this.tableData = response.data.results;
          this.totalcontest = response.data.count;
        });
    },
    handleCurrentChange(val) {
      this.currentpage = val;

      this.$http
        .get(
          "http://" +
            this.$ip +
            ":" +
            this.$port +
            "/contestinfo/?limit=" +
            this.pagesize +
            "&offset=" +
            (this.currentpage - 1) * this.pagesize
        )
        .then(response => {
          for (var i = 0; i < response.data.results.length; i++) {
            if (response.data.results[i]["level"] == "1")
              response.data.results[i]["level"] = "Easy";
            if (response.data.results[i]["level"] == "2")
              response.data.results[i]["level"] = "Medium";
            if (response.data.results[i]["level"] == "3")
              response.data.results[i]["level"] = "Hard";
            if (response.data.results[i]["level"] == "4")
              response.data.results[i]["level"] = "VeryHard";
            if (response.data.results[i]["level"] == "5")
              response.data.results[i]["level"] = "ExtremelyHard";

            response.data.results[i]["begintime"] =
              response.data.results[i]["begintime"].split("T")[0] +
              " " +
              response.data.results[i]["begintime"].split("T")[1].split(".")[0];

            response.data.results[i]["lasttime"] =
              response.data.results[i]["lasttime"] + " S";

            if (response.data.results[i]["auth"] == "1")
              response.data.results[i]["auth"] = "Public";
            if (response.data.results[i]["auth"] == "2")
              response.data.results[i]["auth"] = "Private";
            if (response.data.results[i]["auth"] == "0")
              response.data.results[i]["auth"] = "Protect";
          }
          this.tableData = response.data.results;
          this.totalcontest = response.data.count;
        });
    }
  },
  created() {
    this.$http
      .get(
        "http://" +
          this.$ip +
          ":" +
          this.$port +
          "/contestinfo/?limit=10&offset=0"
      )
      .then(response => {
        for (var i = 0; i < response.data.results.length; i++) {
          if (response.data.results[i]["level"] == "1")
            response.data.results[i]["level"] = "Easy";
          if (response.data.results[i]["level"] == "2")
            response.data.results[i]["level"] = "Medium";
          if (response.data.results[i]["level"] == "3")
            response.data.results[i]["level"] = "Hard";
          if (response.data.results[i]["level"] == "4")
            response.data.results[i]["level"] = "VeryHard";
          if (response.data.results[i]["level"] == "5")
            response.data.results[i]["level"] = "ExtremelyHard";

          response.data.results[i]["begintime"] =
            response.data.results[i]["begintime"].split("T")[0] +
            " " +
            response.data.results[i]["begintime"].split("T")[1].split(".")[0];

          response.data.results[i]["lasttime"] =
            response.data.results[i]["lasttime"] + " S";

          if (response.data.results[i]["auth"] == "1")
            response.data.results[i]["auth"] = "Public";
          if (response.data.results[i]["auth"] == "2")
            response.data.results[i]["auth"] = "Private";
          if (response.data.results[i]["auth"] == "0")
            response.data.results[i]["auth"] = "Protect";
        }
        this.tableData = response.data.results;
        this.totalcontest = response.data.count;
      });
  }
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
#leveltag {
  text-align: center;
  font-weight: bold;
}
.el-row {
  margin-bottom: 20px;
}
</style>
