<template>
  <el-row>
    <el-dialog :visible.sync="dialogVisible" width="80%" :append-to-body="true">
      <el-alert
        title="编译结果"
        :type="compilemsg=='编译成功！'?'success':'warning'"
        :description="compilemsg"
        :closable="false"
        show-icon
        :show-close="false"
      ></el-alert>
      <el-alert title="你的代码：" type="info" :closable="false">
        <el-button
          size="mini"
          v-clipboard:copy="code"
          v-clipboard:success="onCopy"
          v-clipboard:error="onError"
        >Copy</el-button>
      </el-alert>
      <codemirror v-model="code" :options="cmOptions"></codemirror>

      <el-alert
        :key="index"
        v-for="(data,index) in dialogdata"
        :title="index+1 +': '+data.caseresult + ' on test ' + data.casetitle"
        :type="data.caseresult=='Accepted'?'success':(data.caseresult=='Wrong Answer'?'error':'warning')"
        :closable="false"
        v-show="data.casedata!=''"
      >
        <br>
        <h5
          style="white-space:pre;margin-left:15px;"
          v-if="data.casedata!=''"
        >{{'Time: '+ data.casetime + 'MS'+' Memory: '+data.casememory+'MB'}}</h5>
        <h5 style="white-space:pre;margin-left:15px;" v-if="data.casedata!=''">Test Input:</h5>
        <div
          style="white-space:pre;margin-left:15px;word-wrap:break-word;word-break: normal;"
          v-if="data.casedata!=''"
        >{{data.casedata+'\n'}}</div>

        <h5 style="white-space:pre;margin-left:15px;" v-if="data.casedata!=''">Your Output:</h5>
        <div
          style="white-space:pre;margin-left:15px;word-wrap:break-word;word-break: normal;"
          v-if="data.casedata!=''"
        >{{data.caseuseroutput+'\n'}}</div>

        <h5 style="white-space:pre;margin-left:15px;" v-if="data.casedata!=''">Expected Output:</h5>
        <div
          style="white-space:pre;margin-left:15px;word-wrap:break-word;word-break: normal;"
          v-if="data.casedata!=''"
        >{{data.caseoutputdata+'\n'}}</div>
      </el-alert>
    </el-dialog>
    <el-table
      :default-sort="{prop: 'id', order: 'descending'}"
      :data="tableData"
      style="width: 100%"
      :row-class-name="tableRowClassName"
      @row-click="rowClick"
      size="mini"
    >
      <el-table-column prop="id" label="ID" :width="50"></el-table-column>
      <el-table-column prop="result" label="Status" :width="150">
        <template slot-scope="scope">
          <el-tag size="mini" :type="statuetype(scope.row.result)" disable-transitions hit>
            {{ scope.row.result }}
            <i class="el-icon-loading" v-show="statuejudge(scope.row.result)"></i>
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="submittime" align="right">
        <template slot="header" slot-scope="scrop">
          <el-button size="mini" @click="setstatus(false)" type="primary">刷新</el-button>
        </template>
      </el-table-column>
    </el-table>
  </el-row>
</template>


<style scope>
.el-table .warning-row {
  background: #fffed4;
}

.el-table .success-row {
  background: #e6ffdf;
}

.el-table .info-row {
  background: #fffff7;
}

.el-table .judging-row {
  background: #f3ffff;
}

.el-table .danger-row {
  background: #ffe6e6;
}

.el-tag {
  text-align: center;
  font-weight: bold;
}
</style>


<script>
import moment from "moment";
import { codemirror } from "vue-codemirror";
require("codemirror/lib/codemirror.css");
require("codemirror/theme/base16-light.css");
require("codemirror/mode/clike/clike");

export default {
  name: "statuemini",
  components: {
    codemirror
  },
  methods: {
    onCopy(e) {
      this.$message.success("复制成功！");
    },
    // 复制失败
    onError(e) {
      this.$message.error("复制失败：" + e);
    },
    rowClick(row, col, e) {
      if (row.message + "" == "0") this.compilemsg = "编译成功！";
      else this.compilemsg = row.message;

      this.dialogdata = [];
      this.code = "";

      this.$axios
        .get("/judgestatuscode/" + row.id + "/")
        .then(response => {
          this.code = response.data.code;

          this.$axios.get("/casestatus/?statusid=" + row.id).then(res => {
            for (var i = 0; i < res.data.length; i++) {
              this.dialogdata.push({
                caseresult: res.data[i]["result"],
                casedata: res.data[i]["casedata"],
                casetime: res.data[i]["time"],
                casememory: res.data[i]["memory"],
                casetitle: res.data[i]["testcase"],
                caseuseroutput: res.data[i]["useroutput"],
                caseoutputdata: res.data[i]["outputdata"]
              });
            }
          });
        })
        .catch(error => {
          this.code = "无权限查看！" + error;
        });

      this.dialogVisible = true;
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
    setstatus(problem, username) {
      this.tableData=[]
      //console.log(problem)
      if(problem==-1){
        return //用于清零
      }
      if (this.$route.params.contestID) {
        var contest = this.$route.params.contestID;
        if (problem != false) this.problem = problem;
      } else {
        this.problem = this.$route.query.problemID;
        var contest = "";
      }

      if (!username) var user = localStorage.username;
      else var user = username;
      if (user == "") user = "|)#";

      this.$axios
        .get(
          "/judgestatus/?user=" +
            user +
            "&problem=" +
            this.problem +
            "&contest=" +
            contest
        )
        .then(response => {
          for (var i = 0; i < response.data.length; i++) {
            var testcase = response.data[i]["testcase"];

            response.data[i]["submittime"] = moment(
              response.data[i]["submittime"]
            ).format("YYYY-MM-DD");

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
      cmOptions: {
        tabSize: 4,
        mode: "text/x-c++src",
        theme: "base16-light",
        lineNumbers: true,
        readOnly: true
      },
      tableData: [],
      username: "",
      showall: false,
      dialogVisible: false,
      code: "",
      compilemsg: "",
      dialogdata: [],

      problem: -1
    };
  },
  created() {
    if (this.$route.params.contestID) return;
    this.setstatus(false);
  }
};
</script>

