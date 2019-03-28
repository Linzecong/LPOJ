<template>
  <el-card shadow="always" id="card">
    <el-dialog :visible.sync="dialogVisible" width="80%">
      <el-alert
        title="编译结果"
        :type="compilemsg=='编译成功！'?'success':'warning'"
        :description="compilemsg"
        :closable="false"
        show-icon
        :show-close="false"
      ></el-alert>
      <el-alert title="你的代码：" type="info" :closable="false"><el-button size="mini"
        v-clipboard:copy="code"
        v-clipboard:success="onCopy"
        v-clipboard:error="onError">Copy</el-button></el-alert>

      <codemirror id="mycode" v-model="code" :options="cmOptions"></codemirror>

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
        <h5
          style="white-space:pre;margin-left:15px;"
          v-if="data.casedata!=''"
        >Test Input:</h5>
        <div
          style="white-space:pre;margin-left:15px;word-wrap:break-word;word-break: normal;"
          v-if="data.casedata!=''"
        >{{data.casedata+'\n'}}</div>

        <h5
          style="white-space:pre;margin-left:15px;"
          v-if="data.casedata!=''"
        >Your Output:</h5>
        <div
          style="white-space:pre;margin-left:15px;word-wrap:break-word;word-break: normal;"
          v-if="data.casedata!=''"
        >{{data.caseuseroutput+'\n'}}</div>

       <h5
          style="white-space:pre;margin-left:15px;"
          v-if="data.casedata!=''"
        >Expected Output:</h5>
        <div
          style="white-space:pre;margin-left:15px;word-wrap:break-word;word-break: normal;"
          v-if="data.casedata!=''"
        >{{data.caseoutputdata+'\n'}}</div>

      </el-alert>
    </el-dialog>

    <el-switch
      style="float: right;margin:10px;"
      v-model="showall"
      active-text="Show Mine"
      inactive-text="Show All"
      @change="statuechange"
    ></el-switch>
    <el-pagination
      @size-change="handleSizeChange"
      @current-change="handleCurrentChange"
      :current-page="currentpage"
      :page-sizes="[10, 20, 30, 50]"
      :page-size="pagesize"
      layout="total, sizes, prev, pager, next, jumper"
      :total="totalstatus"
    ></el-pagination>
   
    <el-table
      :default-sort="{prop: 'id', order: 'descending'}"
      :data="tableData"
      style="width: 100%"
      :row-class-name="tableRowClassName"
      @row-click="rowClick"
      size="small"
    >
      <el-table-column prop="id" label="ID" :width="100"></el-table-column>
      <el-table-column prop="user" label="User"></el-table-column>
      <el-table-column prop="problem" label="Problem"></el-table-column>
      <el-table-column prop="result" label="Status" :width="300">
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
    <center>
    <el-pagination
      @size-change="handleSizeChange"
      @current-change="handleCurrentChange"
      :current-page="currentpage"
      :page-sizes="[10, 20, 30, 50]"
      :page-size="pagesize"
      layout="total, sizes, prev, pager, next, jumper"
      :total="totalstatus"
    ></el-pagination>
    </center>
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
import moment from "moment";
import { codemirror } from "vue-codemirror";
require("codemirror/lib/codemirror.css");
require("codemirror/theme/base16-light.css");
require("codemirror/mode/clike/clike");

export default {
  name: "statue",
  components: {
    codemirror
  },
  methods: {
    onCopy(e){
       this.$message.success("复制成功！");
    },
    // 复制失败
    onError(e){
      this.$message.error("复制失败："+e);
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
    handleSizeChange(val) {
      if (!this.username) this.username = this.$route.query.username;
      this.contest = this.$route.params.contestID;
      if (!this.contest) this.contest = "";
      if (!this.username) this.username = "";
      this.pagesize = val;
      this.$axios
        .get(
          "/judgestatus/?user=" +
            this.username +
            "&limit=" +
            this.pagesize +
            "&offset=" +
            (this.currentpage - 1) * this.pagesize +
            "&contest=" +
            this.contest
        )
        .then(response => {
          for (var i = 0; i < response.data.results.length; i++) {
            var testcase = response.data.results[i]["testcase"];
            response.data.results[i]["time"] += "MS";
            response.data.results[i]["memory"] += "MB";
            response.data.results[i]["length"] += "B";
            response.data.results[i]["submittime"] = moment(
              response.data.results[i]["submittime"]
            ).format("YYYY-MM-DD HH:mm:ss");

            if (response.data.results[i]["result"] == "-1") {
              response.data.results[i]["result"] = "Pending";
            }

            if (response.data.results[i]["result"] == "-2") {
              response.data.results[i]["result"] = "Judging";
            }

            if (response.data.results[i]["result"] == "-3")
              response.data.results[i]["result"] =
                "Wrong Answer on test " + testcase;

            if (response.data.results[i]["result"] == "-4")
              response.data.results[i]["result"] = "Compile Error";

            if (response.data.results[i]["result"] == "-5")
              response.data.results[i]["result"] =
                "Presentation Error on test " + testcase;

            if (response.data.results[i]["result"] == "-6") {
              response.data.results[i]["result"] = "Waiting";
            }

            if (response.data.results[i]["result"] == "0")
              response.data.results[i]["result"] = "Accepted";

            if (response.data.results[i]["result"] == "1")
              response.data.results[i]["result"] =
                "Time Limit Exceeded on test " + testcase;

            if (response.data.results[i]["result"] == "2")
              response.data.results[i]["result"] =
                "Time Limit Exceeded on test " + testcase;

            if (response.data.results[i]["result"] == "3")
              response.data.results[i]["result"] =
                "Memory Limit Exceeded on test " + testcase;

            if (response.data.results[i]["result"] == "4")
              response.data.results[i]["result"] =
                "Runtime Error on test " + testcase;

            if (response.data.results[i]["result"] == "5")
              response.data.results[i]["result"] = "System Error";
          }
          this.tableData = response.data.results;
          this.totalstatus = response.data.count;
        });
    },
    handleCurrentChange(val) {
      if (!this.username) this.username = this.$route.query.username;
      this.contest = this.$route.params.contestID;
      if (!this.contest) this.contest = "";
      if (!this.username) this.username = "";
      this.currentpage = val;
      this.$axios
        .get(
          "/judgestatus/?user=" +
            this.username +
            "&limit=" +
            this.pagesize +
            "&offset=" +
            (this.currentpage - 1) * this.pagesize +
            "&contest=" +
            this.contest
        )
        .then(response => {
          for (var i = 0; i < response.data.results.length; i++) {
            var testcase = response.data.results[i]["testcase"];
            response.data.results[i]["time"] += "MS";
            response.data.results[i]["memory"] += "MB";
            response.data.results[i]["length"] += "B";
            response.data.results[i]["submittime"] = moment(
              response.data.results[i]["submittime"]
            ).format("YYYY-MM-DD HH:mm:ss");

            if (response.data.results[i]["result"] == "-1") {
              response.data.results[i]["result"] = "Pending";
            }

            if (response.data.results[i]["result"] == "-2") {
              response.data.results[i]["result"] = "Judging";
            }

            if (response.data.results[i]["result"] == "-3")
              response.data.results[i]["result"] =
                "Wrong Answer on test " + testcase;

            if (response.data.results[i]["result"] == "-4")
              response.data.results[i]["result"] = "Compile Error";

            if (response.data.results[i]["result"] == "-5")
              response.data.results[i]["result"] =
                "Presentation Error on test " + testcase;

            if (response.data.results[i]["result"] == "-6") {
              response.data.results[i]["result"] = "Waiting";
            }

            if (response.data.results[i]["result"] == "0")
              response.data.results[i]["result"] = "Accepted";

            if (response.data.results[i]["result"] == "1")
              response.data.results[i]["result"] =
                "Time Limit Exceeded on test " + testcase;

            if (response.data.results[i]["result"] == "2")
              response.data.results[i]["result"] =
                "Time Limit Exceeded on test " + testcase;

            if (response.data.results[i]["result"] == "3")
              response.data.results[i]["result"] =
                "Memory Limit Exceeded on test " + testcase;

            if (response.data.results[i]["result"] == "4")
              response.data.results[i]["result"] =
                "Runtime Error on test " + testcase;

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
      if (!this.username) this.username = this.$route.query.username;
      this.contest = this.$route.params.contestID;
      if (!this.contest) this.contest = "";
      if (!this.username) this.username = "";

      if (this.username == localStorage.username && localStorage.username)
        this.showall = true;
      else this.showall = false;

      this.$axios
        .get(
          "/judgestatus/?user=" +
            this.username +
            "&limit=" +
            this.pagesize +
            "&offset=" +
            (this.currentpage - 1) * this.pagesize +
            "&contest=" +
            this.contest
        )
        .then(response => {
          for (var i = 0; i < response.data.results.length; i++) {
            var testcase = response.data.results[i]["testcase"];
            response.data.results[i]["time"] += "MS";
            response.data.results[i]["memory"] += "MB";
            response.data.results[i]["length"] += "B";
            response.data.results[i]["submittime"] = moment(
              response.data.results[i]["submittime"]
            ).format("YYYY-MM-DD HH:mm:ss");

            if (response.data.results[i]["result"] == "-1") {
              response.data.results[i]["result"] = "Pending";
            }

            if (response.data.results[i]["result"] == "-2") {
              response.data.results[i]["result"] = "Judging";
            }

            if (response.data.results[i]["result"] == "-3")
              response.data.results[i]["result"] =
                "Wrong Answer on test " + testcase;

            if (response.data.results[i]["result"] == "-4")
              response.data.results[i]["result"] = "Compile Error";

            if (response.data.results[i]["result"] == "-5")
              response.data.results[i]["result"] =
                "Presentation Error on test " + testcase;

            if (response.data.results[i]["result"] == "-6") {
              response.data.results[i]["result"] = "Waiting";
            }

            if (response.data.results[i]["result"] == "0")
              response.data.results[i]["result"] = "Accepted";

            if (response.data.results[i]["result"] == "1")
              response.data.results[i]["result"] =
                "Time Limit Exceeded on test " + testcase;

            if (response.data.results[i]["result"] == "2")
              response.data.results[i]["result"] =
                "Time Limit Exceeded on test " + testcase;

            if (response.data.results[i]["result"] == "3")
              response.data.results[i]["result"] =
                "Memory Limit Exceeded on test " + testcase;

            if (response.data.results[i]["result"] == "4")
              response.data.results[i]["result"] =
                "Runtime Error on test " + testcase;

            if (response.data.results[i]["result"] == "5")
              response.data.results[i]["result"] = "System Error";
          }
          this.tableData = response.data.results;
          this.totalstatus = response.data.count;
        });
    },
    setusername(name) {
      this.$route.query.username = "";
      this.username = name;
    },
    statuechange(val) {
      if (val == true) {
        if (!localStorage.username) {
          this.showall = false;
          this.$message.error("请先登录！");
        } else this.setusername(localStorage.username);
      } else {
        this.setusername("");
      }
    },
    creattimer(){
      this.$store.state.timer = setInterval(this.timer, 3000);
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
      currentpage: 1,
      pagesize: 30,
      totalstatus: 10,
      username: "",
      contest: "",
      showall: false,
      dialogVisible: false,
      code: "",
      compilemsg: "",
      dialogdata: []
    };
  },
  destroyed() {
    clearInterval(this.$store.state.timer);
  },
  created() {
    //创建一个全局定时器，定时刷新状态

    this.timer();
    this.$store.state.timer = setInterval(this.timer, 3000);
  }
};
</script>

