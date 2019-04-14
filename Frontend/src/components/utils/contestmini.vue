<template>
  <el-card>
    <div slot="header">
      <b>近期比赛</b>
    </div>
    <el-table
      :data="tableData2"
      @cell-click="contestclick"
      :default-sort="{prop: 'begintime', order: 'descending'}"
    >
      <el-table-column prop="id" label="ID" :width="100"></el-table-column>
      <el-table-column prop="title" label="Title"></el-table-column>
      <el-table-column prop="begintime" label="Begin Time"></el-table-column>
      <el-table-column prop="lasttime" label="Duration"></el-table-column>
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
    </el-table>
  </el-card>
</template>

<script>
import moment from "moment";
export default {
  name: "ratingrule",
  data() {
    return { tableData2: [] };
  },
  created() {
    this.$axios
      .get("/contestcominginfo/")
      .then(response => {
        for (var i = 0; i < response.data.length; i++) {
          response.data[i]["begintime"] = moment(
            response.data[i]["begintime"]
          ).format("YYYY-MM-DD HH:mm:ss");
          response.data[i]["lasttime"] =
            parseInt(response.data[i]["lasttime"] / 60 / 60) +
            ":" +
            parseInt((response.data[i]["lasttime"] / 60) % 60) +
            ":" +
            parseInt((response.data[i]["lasttime"] % 60) % 60);

          if (response.data[i]["auth"] == "1")
            response.data[i]["auth"] = "Public";
          if (response.data[i]["auth"] == "2")
            response.data[i]["auth"] = "Private";
          if (response.data[i]["auth"] == "0")
            response.data[i]["auth"] = "Protect";
        }
        this.tableData2 = response.data;
      })
      .catch(error => {
        this.$message.error(
          "服务器错误！" + "(" + JSON.stringify(error.response.data) + ")"
        );
      });
  },
  methods: {
    contestauth(type) {
      if (type == "Public") return "success";
      if (type == "Protect") return "warning";
      if (type == "Private") return "danger";
    },
    contestclick(row, column, cell, event) {
      this.$router.push({
        name: "contestdetail",
        params: { contestID: row.id }
      });
    }
  }
};
</script>

<style  scoped>
#leveltag {
  text-align: center;
  font-weight: bold;
}
</style>