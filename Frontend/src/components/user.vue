<template>
  <el-card shadow="always" id="card">
    <h1>{{ username }}</h1>
    <h2>Name: {{ name }}</h2>
    <h2>Des: {{ des }}</h2>
    <h2>AC: {{ ac }}</h2>
    <h2>Submittion: {{ submittion }}</h2>
    <h2>Score: {{ score }}</h2>
    <h2>Rating: {{ rating }}</h2>

<el-table @cell-click="problemclick" :default-sort = "{prop: 'time', order: 'descending'}" :data="tableData" :row-class-name="tableRowClassName">
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
      <el-table-column prop="time" label="Time"></el-table-column>
    </el-table>
   
    
  </el-card>
</template>

<script>
export default {
  name: "user",
  data() {
    return {
      username: "404",
      name: "404",
      des: "404",
      ac: "404",
      submittion: "404",
      score: "404",
      rating: "404",
      tableData:[]
    };
  },
  methods: {
    tableRowClassName({ row, rowIndex }) {
      if (row.result == "Pending") return "info-row";
      if (row.result == "Judging") return "judging-row";
      if (row.result == "Wrong Answer") return "danger-row";
      if (row.result == "Compile Error") return "warning-row";
      if (row.result == "Presentation Error") return "warning-row";
      if (row.result == "Waiting") return "info-row";
      if (row.result == "Accepted") return "success-row";
      if (row.result == "Time Limit Exceeded") return "warning-row";
      if (row.result == "Time Limit Exceeded") return "warning-row";
      if (row.result == "Memory Limit Exceeded") return "warning-row";
      if (row.result == "Runtime Error") return "warning-row";
      if (row.result == "System Error") return "warning-row";
      return "";
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
      this.$axios
        .get(
          "http://" +
            this.$ip +
            ":" +
            this.$port +
            "/user/?username=" +
            this.username
        )
        .then(response => {
            this.name=response.data[0].name;
            this.des=response.data[0].des;
            this.score=response.data[0].score;
            this.rating=response.data[0].rating;
        });
      
      this.$axios
        .get(
          "http://" +
            this.$ip +
            ":" +
            this.$port +
            "/userdata/?username=" +
            this.username
        )
        .then(response => {
            this.ac=response.data[0].ac;
            this.submittion=response.data[0].submit;
        });

      this.$axios.get("http://" +
            this.$ip +
            ":" +
            this.$port +
            "/judgestatus/?username=" +
            this.username).then(response => {
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
.el-table .warning-row {
  background: #fff9f9;
}

.el-table .success-row {
  background: #e6ffdf;
}

.el-table .info-row {
  background: #fffff7;
}

.el-table .judging-row {
  background: #f7ffff;
}

.el-table .danger-row {
  background: #fff9f9;
}

.el-tag {
  text-align: center;
  font-weight: bold;
}
</style>
