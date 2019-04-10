<template>
  <el-card shadow="always" id="card">
    <h1 :style="color">{{username}}</h1>
    <h2>Name: {{ name }}</h2>
    <h2>Des: {{ des }}</h2>
    <h2>AC: {{ ac }}</h2>
    <h2>Submittion: {{ submittion }}</h2>
    <h2>Score: {{ score }}</h2>
    <h2>Rating: {{ rating }}</h2>

    <el-table
      @cell-click="problemclick"
      :default-sort="{prop: 'time', order: 'descending'}"
      :data="tableData"
      size="mini"
      :row-style="ratingcolor"
    >
      <el-table-column type="index"></el-table-column>
      <el-table-column prop="problem" label="Problem"></el-table-column>
      <el-table-column prop="language" label="Lang"></el-table-column>
      <el-table-column prop="result" label="Status" :width="250">
        <template slot-scope="scope">
          <el-tag size="medium" :type="statuetype(scope.row.result)" disable-transitions hit>
            {{ scope.row.result }}
            <i class="el-icon-loading" v-show="statuejudge(scope.row.result)"></i>
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="submittime" label="Time"></el-table-column>
    </el-table>
  </el-card>
</template>

<script>
export default {
  name: "user",
  data() {
    return {
      username: "",
      name: "",
      des: "",
      ac: "",
      submittion: "",
      score: "",
      rating: "",
      tableData: [],
      color: ""
    };
  },
  methods: {
    ratingcolor({ row, rowIndex }) {


      if (row.rating >= 3000) return "color:red;";
      if (row.rating >= 2600) return "color:#BB5E00;";
      if (row.rating >= 2200) return "color:#E6A23C;";
      if (row.rating >= 2050) return "color:#930093;";
      if (row.rating >= 1900) return "color:#0000AA;";
      if (row.rating >= 1700) return "color:#007799;";
      if (row.rating >= 1500) return "color:#227700;";
      if (row.rating >= 1350) return "color:#67C23A;";
      if (row.rating >= 1200) return "color:#909399;";
      return "color:#303133;font-weight: bold;";
    },
    statuetype: function(type) {
      if (type == "Pending") return "info";
      if (type == "Judging") return "";
      if (type == "Wrong Answer") return "danger";
      if (type == "Compile Error") return "warning";
      if (type == "Presentation Error") return "warning";
      if (type == "Waiting") return "info";
      if (type == "Accepted") return "success";
      if (type == "Time Limit Exceeded") return "warning";
      if (type == "Time Limit Exceeded") return "warning";
      if (type == "Memory Limit Exceeded") return "warning";
      if (type == "Runtime Error") return "warning";
      if (type == "System Error") return "danger";

      return "danger";
    },
    statuejudge: function(type) {
      if (type == "Pending") return true;
      if (type == "Judging") return true;
      if (type == "Wrong Answer") return false;
      if (type == "Compile Error") return false;
      if (type == "Presentation Error") return false;
      if (type == "Waiting") return true;
      if (type == "Accepted") return false;
      if (type == "Time Limit Exceeded") return false;
      if (type == "Time Limit Exceeded") return false;
      if (type == "Memory Limit Exceeded") return false;
      if (type == "Runtime Error") return false;
      if (type == "System Error") return false;
      return false;
    },
    problemclick: function(row, column, cell, event) {
      this.$router.push({
        name: "problemdetail",
        query: { problemID: row.problem }
      });
    }
  },
  created() {
    this.username = this.$route.query.username;
    if (this.username) {
      this.$axios.get("/user/?username=" + this.username).then(response => {
        this.name = response.data[0].name;
      });

      this.$axios.get("/userdata/?username=" + this.username).then(response => {
        this.ac = response.data[0].ac;
        this.submittion = response.data[0].submit;
        this.des = response.data[0].des;
        this.score = response.data[0].score;
        this.rating = response.data[0].rating;
        var style = "";
      if (this.rating >= 3000) style = "color:red;font-weight: bold;";
      else if (this.rating >= 2600) style = "color:#BB5E00;font-weight: bold;";
      else if (this.rating >= 2200) style = "color:#E6A23C;font-weight: bold;";
      else if (this.rating >= 2050) style = "color:#930093;font-weight: bold;";
      else if (this.rating >= 1900) style = "color:#0000AA;font-weight: bold;";
      else if (this.rating >= 1700) style = "color:#007799;font-weight: bold;";
      else if (this.rating >= 1500) style = "color:#227700;font-weight: bold;";
      else if (this.rating >= 1350) style = "color:#67C23A;font-weight: bold;";
      else if (this.rating >= 1200) style = "color:#909399;font-weight: bold;";
      else style = "color:#303133;font-weight: bold;";
      this.color = style
      });

      

      this.$axios
        .get("/judgestatusdistinct/?user=" + this.username + "&result=0")
        .then(response => {
          for (var i = 0; i < response.data.length; i++) {
            response.data[i]["submittime"] =
              response.data[i]["submittime"].split("T")[0] +
              " " +
              response.data[i]["submittime"].split("T")[1].split(".")[0];

            if (response.data[i]["result"] == "-1") {
              response.data[i]["result"] = "Pending";
            }

            if (response.data[i]["result"] == "-2") {
              response.data[i]["result"] = "Judging";
            }

            if (response.data[i]["result"] == "-3")
              response.data[i]["result"] = "Wrong Answer";

            if (response.data[i]["result"] == "-4")
              response.data[i]["result"] = "Compile Error";

            if (response.data[i]["result"] == "-5")
              response.data[i]["result"] = "Presentation Error";

            if (response.data[i]["result"] == "-6") {
              response.data[i]["result"] = "Waiting";
            }

            if (response.data[i]["result"] == "0")
              response.data[i]["result"] = "Accepted";

            if (response.data[i]["result"] == "1")
              response.data[i]["result"] = "Time Limit Exceeded";

            if (response.data[i]["result"] == "2")
              response.data[i]["result"] = "Time Limit Exceeded";

            if (response.data[i]["result"] == "3")
              response.data[i]["result"] = "Memory Limit Exceeded";

            if (response.data[i]["result"] == "4")
              response.data[i]["result"] = "Runtime Error on test";

            if (response.data[i]["result"] == "5")
              response.data[i]["result"] = "System Error";
          }
          this.tableData = response.data;
        });
    }
  }
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
#card {
  margin: 200px;
  padding: 200px;
}
.el-tag {
  text-align: center;
  font-weight: bold;
}
</style>
