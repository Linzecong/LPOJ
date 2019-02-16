<template>
  <el-card shadow="always" id="card">
    <el-table  :default-sort = "{prop: 'id', order: 'descending'}" :data="tableData" style="width: 100%" :row-class-name="tableRowClassName">
      <el-table-column prop="id" label="ID" :width="100"></el-table-column>
      <el-table-column prop="user" label="User"></el-table-column>
      <el-table-column prop="problem" label="Problem"></el-table-column>
      <el-table-column prop="result" label="Status" :width="250">
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
    <el-pagination
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
          :current-page="currentpage"
          :page-sizes="[10, 20, 30, 50]"
          :page-size="pagesize"
          layout="total, sizes, prev, pager, next, jumper"
          :total="totalstatus"
        ></el-pagination>
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
    handleSizeChange(val) {
      this.pagesize=val;
        this.$http.get("http://" +
            this.$ip +
            ":" +
            this.$port +
            "/judgestatus/?limit=" +
            this.pagesize +
            "&offset=" +
            (this.currentpage - 1) * this.pagesize).then(response => {
        for (var i = 0; i < response.data.results.length; i++) {
          var testcase = response.data.results[i]["testcase"];
          response.data.results[i]["time"] += "MS";
          response.data.results[i]["memory"] += "MB";
          response.data.results[i]["length"] += "B";
          response.data.results[i]["submittime"] =
            response.data.results[i]["submittime"].split("T")[0] +
            " " +
            response.data.results[i]["submittime"].split("T")[1].split(".")[0];

          if (response.data.results[i]["result"] == "-1") {
            response.data.results[i]["result"] = "Pending";
          }

          if (response.data.results[i]["result"] == "-2") {
            response.data.results[i]["result"] = "Judging";
          }

          if (response.data.results[i]["result"] == "-3")
            response.data.results[i]["result"] = "Wrong Answer on test " + testcase;

          if (response.data.results[i]["result"] == "-4")
            response.data.results[i]["result"] = "Compile Error";

          if (response.data.results[i]["result"] == "-5")
            response.data.results[i]["result"] = "Presentation Error on test " + testcase;

          if (response.data.results[i]["result"] == "-6") {
            response.data.results[i]["result"] = "Waiting";
          }

          if (response.data.results[i]["result"] == "0")
            response.data.results[i]["result"] = "Accepted";

          if (response.data.results[i]["result"] == "1")
            response.data.results[i]["result"] = "Time Limit Exceeded on test " + testcase;

          if (response.data.results[i]["result"] == "2")
            response.data.results[i]["result"] = "Time Limit Exceeded on test " + testcase;

          if (response.data.results[i]["result"] == "3")
            response.data.results[i]["result"] = "Memory Limit Exceeded on test " + testcase;

          if (response.data.results[i]["result"] == "4")
            response.data.results[i]["result"] = "Runtime Error on test " + testcase;

          if (response.data.results[i]["result"] == "5")
            response.data.results[i]["result"] = "System Error";
        }
        this.tableData = response.data.results;
        this.totalstatus = response.data.count;
      });
      },
      handleCurrentChange(val) {
        this.currentpage=val;
        this.$http.get("http://" +
            this.$ip +
            ":" +
            this.$port +
            "/judgestatus/?limit=" +
            this.pagesize +
            "&offset=" +
            (this.currentpage - 1) * this.pagesize).then(response => {
        for (var i = 0; i < response.data.results.length; i++) {
          var testcase = response.data.results[i]["testcase"];
          response.data.results[i]["time"] += "MS";
          response.data.results[i]["memory"] += "MB";
          response.data.results[i]["length"] += "B";
          response.data.results[i]["submittime"] =
            response.data.results[i]["submittime"].split("T")[0] +
            " " +
            response.data.results[i]["submittime"].split("T")[1].split(".")[0];

          if (response.data.results[i]["result"] == "-1") {
            response.data.results[i]["result"] = "Pending";
          }

          if (response.data.results[i]["result"] == "-2") {
            response.data.results[i]["result"] = "Judging";
          }

          if (response.data.results[i]["result"] == "-3")
            response.data.results[i]["result"] = "Wrong Answer on test " + testcase;

          if (response.data.results[i]["result"] == "-4")
            response.data.results[i]["result"] = "Compile Error";

          if (response.data.results[i]["result"] == "-5")
            response.data.results[i]["result"] = "Presentation Error on test " + testcase;

          if (response.data.results[i]["result"] == "-6") {
            response.data.results[i]["result"] = "Waiting";
          }

          if (response.data.results[i]["result"] == "0")
            response.data.results[i]["result"] = "Accepted";

          if (response.data.results[i]["result"] == "1")
            response.data.results[i]["result"] = "Time Limit Exceeded on test " + testcase;

          if (response.data.results[i]["result"] == "2")
            response.data.results[i]["result"] = "Time Limit Exceeded on test " + testcase;

          if (response.data.results[i]["result"] == "3")
            response.data.results[i]["result"] = "Memory Limit Exceeded on test " + testcase;

          if (response.data.results[i]["result"] == "4")
            response.data.results[i]["result"] = "Runtime Error on test " + testcase;

          if (response.data.results[i]["result"] == "5")
            response.data.results[i]["result"] = "System Error";
        }
        this.tableData = response.data.results;
        this.totalstatus = response.data.count;
      });
      },
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
    timer: function() {
      this.$http.get("http://" +
            this.$ip +
            ":" +
            this.$port +
            "/judgestatus/?limit=" +
            this.pagesize +
            "&offset=" +
            (this.currentpage - 1) * this.pagesize).then(response => {
        for (var i = 0; i < response.data.results.length; i++) {
          var testcase = response.data.results[i]["testcase"];
          response.data.results[i]["time"] += "MS";
          response.data.results[i]["memory"] += "MB";
          response.data.results[i]["length"] += "B";
          response.data.results[i]["submittime"] =
            response.data.results[i]["submittime"].split("T")[0] +
            " " +
            response.data.results[i]["submittime"].split("T")[1].split(".")[0];

          if (response.data.results[i]["result"] == "-1") {
            response.data.results[i]["result"] = "Pending";
          }

          if (response.data.results[i]["result"] == "-2") {
            response.data.results[i]["result"] = "Judging";
          }

          if (response.data.results[i]["result"] == "-3")
            response.data.results[i]["result"] = "Wrong Answer on test " + testcase;

          if (response.data.results[i]["result"] == "-4")
            response.data.results[i]["result"] = "Compile Error";

          if (response.data.results[i]["result"] == "-5")
            response.data.results[i]["result"] = "Presentation Error on test " + testcase;

          if (response.data.results[i]["result"] == "-6") {
            response.data.results[i]["result"] = "Waiting";
          }

          if (response.data.results[i]["result"] == "0")
            response.data.results[i]["result"] = "Accepted";

          if (response.data.results[i]["result"] == "1")
            response.data.results[i]["result"] = "Time Limit Exceeded on test " + testcase;

          if (response.data.results[i]["result"] == "2")
            response.data.results[i]["result"] = "Time Limit Exceeded on test " + testcase;

          if (response.data.results[i]["result"] == "3")
            response.data.results[i]["result"] = "Memory Limit Exceeded on test " + testcase;

          if (response.data.results[i]["result"] == "4")
            response.data.results[i]["result"] = "Runtime Error on test " + testcase;

          if (response.data.results[i]["result"] == "5")
            response.data.results[i]["result"] = "System Error";
        }
        this.tableData = response.data.results;
        this.totalstatus = response.data.count;
      });
    }
  },
  data() {
    return {
      tableData: [],
      currentpage: 1,
      pagesize: 10,
      totalstatus: 10,
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

