<template>
  <el-card shadow="always" id="card">
    <el-table  :default-sort = "{prop: 'id', order: 'descending'}" :data="tableData" style="width: 100%" :row-class-name="tableRowClassName">
      <el-table-column prop="id" label="ID" :width="40"></el-table-column>
      <el-table-column prop="user" label="User"></el-table-column>
      <el-table-column prop="problem" label="Problem"></el-table-column>
      <el-table-column prop="result" label="Status" :width="190">
        <template slot-scope="scope">
          <el-tag size="medium" :type="statuetype(scope.row.result)" disable-transitions hit>
            {{ scope.row.result }}
            <i class="el-icon-loading" v-show="statuejudge(scope.row.result)"></i>
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="time" label="Time"></el-table-column>
      <el-table-column prop="memory" label="Memory"></el-table-column>
      <el-table-column prop="length" label="Length"></el-table-column>
      <el-table-column prop="language" label="Language"></el-table-column>
      <el-table-column prop="submittime" label="Submit time" :width="180"></el-table-column>
      <el-table-column prop="judger" label="Judger"></el-table-column>
    </el-table>
  </el-card>
</template>


<style scope>
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


<script>
export default {
  name: "statue",
  methods: {
    tableRowClassName({ row, rowIndex }) {
      if (row.result == "Pendding") return "info-row";
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
      if (type == "Pendding") return "info";
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
      if (type == "Pendding") return true;
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
    timer: function() {
      this.$http.get("http://localhost:8000/judgestatus/").then(response => {
        for (var i = 0; i < response.data.length; i++) {
          response.data[i]["time"] += "MS";
          response.data[i]["memory"] += "MB";
          response.data[i]["length"] += "B";
          response.data[i]["submittime"] =
            response.data[i]["submittime"].split("T")[0] +
            " " +
            response.data[i]["submittime"].split("T")[1].split(".")[0];

          if (response.data[i]["result"] == "-1") {
            response.data[i]["result"] = "Pendding";
            this.penddinglist.push(response.data[i]["id"]);
          }

          if (response.data[i]["result"] == "-2") {
            this.penddinglist.push(response.data[i]["id"]);
            response.data[i]["result"] = "Judging";
          }

          if (response.data[i]["result"] == "-3")
            response.data[i]["result"] = "Wrong Answer";

          if (response.data[i]["result"] == "-4")
            response.data[i]["result"] = "Compile Error";

          if (response.data[i]["result"] == "-5")
            response.data[i]["result"] = "Presentation Error";

          if (response.data[i]["result"] == "-6") {
            this.penddinglist.push(response.data[i]["id"]);
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
            response.data[i]["result"] = "Runtime Error";

          if (response.data[i]["result"] == "5")
            response.data[i]["result"] = "System Error";
        }
        this.tableData = response.data;
      });
    }
  },
  data() {
    return {
      tableData: [],
      penddinglist: []
    };
  },
  destroyed() {
    clearInterval(this.$store.state.timer);
  },
  created() {
    //创建一个全局定时器，定时刷新状态
    this.timer();
    this.$store.state.timer = setInterval(this.timer, 1000);
  }
};
</script>

