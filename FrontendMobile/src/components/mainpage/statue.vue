<template>
  <mu-container>
    <mu-card>
      <mu-dialog transition="scale" :open.sync="dialogVisible" scrollable>
        <!-- <mu-appbar color="primary" title="Submit Detail">
          <mu-button slot="left" icon @click="dialogVisible = false">
            <mu-icon value="close"></mu-icon>
          </mu-button>
          <mu-button slot="right" flat @click="dialogVisible = false">Close</mu-button>
        </mu-appbar> -->


          <mu-alert :color="compilemsg=='编译成功！'?'success':'warning'" delete @delete="dialogVisible = false">
            <b>{{compilemsg}}</b>
          </mu-alert>

          <br />

          <mu-button
            full-width
            color="success"
            v-clipboard:copy="code"
            v-clipboard:success="onCopy"
            v-clipboard:error="onError"
          >Copy Code</mu-button>

          <br />
          <br />
          <codemirror style="font-size:11px;" v-model="code" :options="cmOptions"></codemirror>

          <br />

          
            <mu-expansion-panel
              :key="index"
              v-for="(data,index) in dialogdata"
              v-if="data.casedata!=''"
              style="margin-bottom:15px;"
            >
              <template slot="header">
                
                  <font :color="data.caseresult=='Accepted'?'success':(data.caseresult=='Wrong Answer'?'error':'warning')"><b>{{' '+data.caseresult + ' on test ' + data.casetitle}}</b></font>
             
              </template>

              <div
                
                v-show="data.casedata!=''"
              >
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

                <h5
                  style="white-space:pre;margin-left:15px;"
                  v-if="data.casedata!=''"
                >Expected Output:</h5>
                <div
                  style="white-space:pre;margin-left:15px;word-wrap:break-word;word-break: normal;"
                  v-if="data.casedata!=''"
                >{{data.caseoutputdata+'\n'}}</div>
              </div>
            </mu-expansion-panel>
          

      </mu-dialog>

      <mu-data-table
        :data="tableData"
        :hover="false"
        :rowStyle="ratingcolor"
        :loading="loading"
        :columns="columns"
      >
        <template slot="expand" slot-scope="prop">
          <mu-container>
            <mu-flex justify-content="center">
              <mu-button
                @click="rowClick(prop.row,prop.row,prop.row)"
                full-width
                style="margin: 8px;"
                :color="statuetype(prop.row.result)"
              >{{ prop.row.result }}</mu-button>
            </mu-flex>

            <br />

            <mu-flex justify-content="center">
              <mu-chip style="margin: 8px;" color="primary">{{ prop.row.time }}</mu-chip>

              <mu-chip style="margin: 8px;" color="secondary">{{ prop.row.memory }}</mu-chip>

              <mu-chip style="margin: 8px;" color="warning">{{ prop.row.language }}</mu-chip>
              <mu-chip style="margin: 8px;" color="success">{{ prop.row['length'] }}</mu-chip>
            </mu-flex>

            <mu-flex justify-content="center">
              <mu-button
                @click="rowClick(prop.row,prop.row,prop.row)"
                style="margin: 8px;"
                color="info"
              >{{ prop.row.submittime }}</mu-button>
            </mu-flex>

            <br />

            <mu-button v-if="contest==''" full-width color="success" @click="problemclick(prop.row.problem)">Try IT!</mu-button>

            <br v-if="contest==''" />
            <br v-if="contest==''" />
          </mu-container>
        </template>

        <template slot-scope="scope">
          <td>{{scope.row.id}}</td>
          <td>{{scope.row.user}}</td>
          <td>{{scope.row.problemtitle}}</td>
        </template>
      </mu-data-table>
    </mu-card>
    <br />
    <mu-flex justify-content="center">
      <mu-pagination
        raised
        :page-count="5"
        :total="totalstatus"
        :current.sync="currentpage"
        @change="handleCurrentChange"
      ></mu-pagination>
    </mu-flex>
  </mu-container>
</template>


<style scope>
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
    onCopy(e) {
      this.$toast.success("复制成功！");
    },
    // 复制失败
    onError(e) {
      this.$toast.error("复制失败：" + e);
    },
    problemclick: function(problem) {
      this.$router.push({
        name: "problemdetail",
        query: { problemID: problem }
      });
    },

    rowClick(index, row, e) {
      if (row.message + "" == "0" || row.result == "Accepted")
        this.compilemsg = "编译成功！";
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
    searchstatus() {
      this.currentpage = 1;
      this.searchdialogVisible = false;
      this.setusername(this.searchform.user);
      this.getstatusdata();
    },
    resetsearch() {
      this.currentpage = 1;
      this.searchform.user = "";
      this.setusername(this.searchform.user);
      this.searchform.problem = "";
      this.searchform.language = "";
      this.searchform.result = "";
      this.timer();
      this.creattimer();
    },
    handleCurrentChange(val) {
      if (!this.username) this.username = this.$route.query.username;
      this.contest = this.$route.params.contestID;
      if (!this.contest) this.contest = "";
      if (!this.username) this.username = "";
      this.currentpage = val;
      this.getstatusdata();
    },
    ratingcolor(rowIndex, row) {
      var back = "";
      if (row.result == "Accepted")
        back = "background:#e8f5e9;font-weight: bold;";
      if (row.result.indexOf("Wrong Answer") >= 0)
        back = "background:#ffebee;font-weight: bold;";

      if (row.result.indexOf("Error") >= 0)
        back = "background:#fff3e0;font-weight: bold;";

      if (row.result.indexOf("Limit") >= 0)
        back = "background:#fff3e0;font-weight: bold;";

      if (row.rating >= 3000) return "color:red;" + back;
      if (row.rating >= 2600) return "color:#BB5E00;" + back;
      if (row.rating >= 2200) return "color:#E6A23C;" + back;
      if (row.rating >= 2050) return "color:#930093;" + back;
      if (row.rating >= 1900) return "color:#0000AA;" + back;
      if (row.rating >= 1700) return "color:#007799;" + back;
      if (row.rating >= 1500) return "color:#227700;" + back;
      if (row.rating >= 1350) return "color:#67C23A;" + back;
      if (row.rating >= 1200) return "color:#909399;" + back;
      return "color:#303133;" + back;
    },

    statuetype: function(type) {
      if (type == "Pending") return "info";
      if (type == "Judging") return "";
      if (type == "Wrong Answer") return "error";
      if (type == "Compile Error") return "warning";
      if (type == "Presentation Error") return "warning";
      if (type == "Waiting") return "info";
      if (type == "Accepted") return "success";
      if (type == "Time Limit Exceeded") return "warning";
      if (type == "Time Limit Exceeded") return "warning";
      if (type == "Memory Limit Exceeded") return "warning";
      if (type == "Runtime Error") return "warning";
      if (type == "System Error") return "error";

      return "error";
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

      if (this.username == sessionStorage.username && sessionStorage.username)
        this.showall = true;
      else this.showall = false;
      this.getstatusdata();
    },

    getstatusdata() {
      this.loading = true;
      this.$axios
        .get(
          "/judgestatus/?user=" +
            this.username +
            "&limit=" +
            this.pagesize +
            "&offset=" +
            (this.currentpage - 1) * this.pagesize +
            "&problem=" +
            this.searchform.problem +
            "&language=" +
            this.searchform.language +
            "&result=" +
            this.searchform.result +
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

            if (response.data.results[i]["result"] == "-3") {
              response.data.results[i]["result"] =
                "Wrong Answer on test " + testcase;
              if (testcase == "?")
                response.data.results[i]["result"] = "Wrong Answer";
            }

            if (response.data.results[i]["result"] == "-4")
              response.data.results[i]["result"] = "Compile Error";

            if (response.data.results[i]["result"] == "-5") {
              response.data.results[i]["result"] =
                "Presentation Error on test " + testcase;
              if (testcase == "?")
                response.data.results[i]["result"] = "Presentation Error";
            }

            if (response.data.results[i]["result"] == "-6") {
              response.data.results[i]["result"] = "Waiting";
            }

            if (response.data.results[i]["result"] == "0")
              response.data.results[i]["result"] = "Accepted";

            if (response.data.results[i]["result"] == "1") {
              response.data.results[i]["result"] =
                "Time Limit Exceeded on test " + testcase;
              if (testcase == "?")
                response.data.results[i]["result"] = "Time Limit Exceeded";
            }

            if (response.data.results[i]["result"] == "2") {
              response.data.results[i]["result"] =
                "Time Limit Exceeded on test " + testcase;
              if (testcase == "?")
                response.data.results[i]["result"] = "Time Limit Exceeded";
            }

            if (response.data.results[i]["result"] == "3") {
              response.data.results[i]["result"] =
                "Memory Limit Exceeded on test " + testcase;
              if (testcase == "?")
                response.data.results[i]["result"] = "Memory Limit Exceeded";
            }

            if (response.data.results[i]["result"] == "4") {
              response.data.results[i]["result"] =
                "Runtime Error on test " + testcase;
              if (testcase == "?")
                response.data.results[i]["result"] = "Runtime Error";
            }

            if (response.data.results[i]["result"] == "5")
              response.data.results[i]["result"] = "System Error";

            if (response.data.results[i]["problemtitle"] == "")
              response.data.results[i]["problemtitle"] =
                response.data.results[i]["problem"];
          }
          this.tableData = response.data.results;
          this.totalstatus = response.data.count;
          this.loading = false;
        });
    },

    setusername(name) {
      this.$route.query.username = "";
      this.username = name;
    },
    statuechange(val) {
      if (val == true) {
        if (!sessionStorage.username) {
          this.showall = false;
          this.$toast.error("请先登录！");
        } else this.setusername(sessionStorage.username);
      } else {
        this.setusername("");
      }
    },
    creattimer() {
      clearInterval(this.$store.state.timer);
      this.timer();
      this.$store.state.timer = setInterval(this.timer, 10000);
    }
  },
  data() {
    return {
      columns: [
        { title: "ID", name: "id", width: 85 },
        { title: "User", name: "user", width: 100 },
        { title: "Problem", name: "problemtitle" }
      ],
      cmOptions: {
        tabSize: 4,
        mode: "text/x-c++src",
        theme: "base16-light",
        lineNumbers: false,
        readOnly: true,
        viewportMargin: Infinity,
        lineWrapping: true
      },
      tableData: [],
      currentpage: 1,
      pagesize: 10,
      totalstatus: 10,
      username: "",
      contest: "",
      showall: false,
      dialogVisible: false,
      searchdialogVisible: false,
      code: "",
      compilemsg: "",
      dialogdata: [],
      loading: false,
      searchform: {
        user: "",
        result: "",
        problem: "",
        language: ""
      }
    };
  },
  destroyed() {
    clearInterval(this.$store.state.timer);
  },
  created() {
    //创建一个全局定时器，定时刷新状态

    this.timer();
    this.$store.state.timer = setInterval(this.timer, 10000);
  }
};
</script>

