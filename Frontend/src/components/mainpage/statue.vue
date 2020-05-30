<template>
  <el-card shadow="always"
           id="card">
    <el-dialog :visible.sync="dialogVisible"
               width="80%">
      <el-alert title="Program Message:"
                :type="compilemsg=='编译成功！'?'success':'warning'"
                :description="compilemsg"
                :closable="false"
                show-icon
                :show-close="false"></el-alert>
      <el-alert title="Code："
                type="info"
                :closable="false">
        <el-button size="mini"
                   v-clipboard:copy="code"
                   v-clipboard:success="onCopy"
                   v-clipboard:error="onError">Copy</el-button>
        <el-button size="mini"
                   @click="downloadFile(curid,code)">Download</el-button>
        <el-button v-if="isadmin"
                   type="danger"
                   size="mini"
                   @click="deletestatus(curid)">Delete</el-button>
      </el-alert>

      <codemirror id="mycode"
                  v-model="code"
                  :options="cmOptions"></codemirror>
      <el-collapse>
        <el-collapse-item :key="index"
                          v-for="(data,index) in dialogdata"
                          v-if="data.casedata!=''"
                          :class="data.caseresult=='Accepted'?'el-collapse-success':(data.caseresult=='Wrong Answer'?'el-collapse-error':'el-collapse-warning')">
          <template slot="title">
            <el-alert :show-icon="true"
                      :type="data.caseresult=='Accepted'?'success':(data.caseresult=='Wrong Answer'?'error':'warning')"
                      :closable="false"
                      v-show="data.casedata!=''">
              <template slot="title">
                <b>{{' '+data.caseresult + ' on test ' + data.casetitle}}</b>
              </template>
            </el-alert>
          </template>
          <el-alert :title="''"
                    :type="data.caseresult=='Accepted'?'success':(data.caseresult=='Wrong Answer'?'error':'warning')"
                    :closable="false"
                    v-show="data.casedata!=''">
            <h5 style="white-space:pre;margin-left:15px;"
                v-if="data.casedata!=''">{{'Time: '+ data.casetime + 'MS'+' Memory: '+data.casememory+'MB'}}</h5>
            <h5 style="white-space:pre;margin-left:15px;"
                v-if="data.casedata!=''">Test Input:</h5>
            <div style="white-space:pre;margin-left:15px;word-wrap:break-word;word-break: normal;"
                 v-if="data.casedata!=''">{{data.casedata+'\n'}}</div>

            <h5 style="white-space:pre;margin-left:15px;"
                v-if="data.casedata!=''">Your Output:</h5>
            <div style="white-space:pre;margin-left:15px;word-wrap:break-word;word-break: normal;"
                 v-if="data.casedata!=''">{{data.caseuseroutput+'\n'}}</div>

            <h5 style="white-space:pre;margin-left:15px;"
                v-if="data.casedata!=''">Expected Output:</h5>
            <div style="white-space:pre;margin-left:15px;word-wrap:break-word;word-break: normal;"
                 v-if="data.casedata!=''">{{data.caseoutputdata+'\n'}}</div>
          </el-alert>
        </el-collapse-item>
      </el-collapse>
    </el-dialog>

    <el-dialog :visible.sync="searchdialogVisible">
      <el-form :model="searchform"
               label-position="right"
               @keyup.native.enter="searchstatus">
        <el-form-item label="User:">
          <el-input v-model="searchform.user"
                    placeholder="User..."></el-input>
        </el-form-item>
        <el-form-item label="Problem Number：">
          <el-input v-model="searchform.problem"
                    placeholder="Problem Number...or ABCDE"></el-input>
        </el-form-item>
        <el-form-item label="Language：">
          <el-select v-model="searchform.language"
                     placeholder="Choose...">
            <languageselect></languageselect>
          </el-select>
        </el-form-item>
        <el-form-item label="Result：">
          <el-select v-model="searchform.result"
                     placeholder="Choose...">
            <el-option key="0"
                       label="Accepted"
                       value="0"></el-option>
            <el-option key="1"
                       label="Wrong Answer"
                       value="-3"></el-option>
            <el-option key="2"
                       label="Waiting"
                       value="-6"></el-option>
            <el-option key="3"
                       label="Presentation Error"
                       value="-5"></el-option>
            <el-option key="4"
                       label="Compile Error"
                       value="-4"></el-option>
            <el-option key="5"
                       label="Pending"
                       value="-1"></el-option>
            <el-option key="6"
                       label="Judging"
                       value="-2"></el-option>
            <el-option key="7"
                       label="Time Limit Exceeded 1"
                       value="1"></el-option>
            <el-option key="8"
                       label="Time Limit Exceeded 2"
                       value="2"></el-option>
            <el-option key="9"
                       label="Memory Limit Exceeded"
                       value="3"></el-option>
            <el-option key="10"
                       label="Runtime Error"
                       value="4"></el-option>
            <el-option key="11"
                       label="System Error"
                       value="5"></el-option>
          </el-select>
        </el-form-item>
      </el-form>
      <div slot="footer"
           class="dialog-footer">
        <el-button @click="searchdialogVisible = false">Cancel</el-button>
        <el-button type="primary"
                   @click="searchstatus">OK</el-button>
      </div>
    </el-dialog>

    <el-switch style="float: right;margin:10px;"
               v-model="showall"
               active-text="Show Mine"
               inactive-text="Show All"
               @change="statuechange"></el-switch>
    <el-button type="primary"
               @click="resetsearch"
               style="float: right;margin-top:6px;margin-right:10px;"
               size="mini">Refresh</el-button>
    <el-button type="primary"
               @click="searchdialogVisible = true"
               style="float: right;margin-top:6px;margin-right:15px;"
               size="mini">Filter</el-button>

    <el-pagination @size-change="handleSizeChange"
                   @current-change="handleCurrentChange"
                   :current-page="currentpage"
                   :page-sizes="[10, 20, 30, 50]"
                   :page-size="pagesize"
                   layout="total, sizes, prev, pager, next, jumper"
                   :total="totalstatus"></el-pagination>

    <el-table :default-sort="{prop: 'id', order: 'descending'}"
              :data="tableData"
              style="width: 100%"
              :row-style="ratingcolor"
              @row-click="rowClick"
              size="small"
              v-loading="loading">
      <el-table-column prop="id"
                       label="ID"
                       :width="70"></el-table-column>
      <el-table-column prop="user"
                       label="User"
                       :width="140"></el-table-column>
      <el-table-column prop="problemtitle"
                       label="Problem"
                       :width="320">
        <template slot-scope="scope">
          <font color="#409EFF">
            <b style="cursor:pointer;">{{ scope.row.problemtitle }}</b>
          </font>
        </template>
      </el-table-column>
      <el-table-column prop="result"
                       label="Status"
                       :width="285">
        <template slot-scope="scope">
          <el-tag size="medium"
                  :type="statuetype(scope.row.result)"
                  disable-transitions
                  hit>
            {{ scope.row.result }}
            <i class="el-icon-loading"
               v-show="statuejudge(scope.row.result)"></i>
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="time"
                       label="Time"></el-table-column>
      <el-table-column prop="memory"
                       label="Memory"></el-table-column>
      <el-table-column prop="length"
                       label="Length"></el-table-column>
      <el-table-column prop="language"
                       label="Language"></el-table-column>
      <el-table-column prop="submittime"
                       label="Submit time"

                       :width="180"></el-table-column>
      <el-table-column prop="judger"
                       label="Judger"></el-table-column>
    </el-table>
    <center>
      <el-pagination @size-change="handleSizeChange"
                     @current-change="handleCurrentChange"
                     :current-page="currentpage"
                     :page-sizes="[10, 20, 30, 50]"
                     :page-size="pagesize"
                     layout="total, sizes, prev, pager, next, jumper"
                     :total="totalstatus"></el-pagination>
    </center>
  </el-card>
</template>


<style scope>
.el-tag {
  text-align: center;
  font-weight: bold;
}


.el-collapse-item__header{
  background-color: unset;
  line-height: unset;
}

.el-collapse-error{
  background-color:#FEF0F0; 
}

.el-collapse-success{
  background-color:#F0F9EB; 
}

.el-collapse-warning{
  background-color:#FDF6EC; 
}

.el-collapse-item__content{
  padding: 0;
}

.CodeMirror{
  /* font-size: 18px; */
}
</style>

<script>
import moment from "moment";
import { codemirror } from "vue-codemirror";
import "codemirror/addon/scroll/simplescrollbars.js"
require("codemirror/addon/scroll/simplescrollbars.css")
require("codemirror/lib/codemirror.css");
require("codemirror/theme/base16-light.css");
require("codemirror/mode/clike/clike");
import languageselect from "@/components/utils/languageselect";
export default {
  name: "statue",
  components: {
    codemirror,
    languageselect
  },
  methods: {
    deletestatus (id) {
      this.$axios
        .delete("/judgestatus/" + id + "/").then(response => {
          this.$message.success("成功！")
        })
        .catch(error => {
          this.$message.error("失败！" + error)
        });
    },
    onCopy (e) {
      this.$message.success("复制成功！");
    },
    // 复制失败
    onError (e) {
      this.$message.error("复制失败：" + e);
    },

    rowClick (row, col, e) {
      // console.log(col);

      if (col.label == "Problem") {
        if (this.contest != "0")
          return
        this.$router.push({
          name: "problemdetail",
          query: { problemID: row.problem }
        });
        return;
      }

      if (col.label == "User") {
        this.$router.push({
          name: "user",
          query: { username: row.user }
        });
        return;
      }



      this.dialogdata = [];
      this.code = "";

      this.$axios
        .get("/judgestatuscode/" + row.id + "/")
        .then(response => {
          this.code = response.data.code;
          this.curid = row.id;
          if (response.data.language == "Python2") this.curlang = 'py'
          if (response.data.language == "Python3") this.curlang = 'py'
          if (response.data.language == "C++") this.curlang = 'cpp'
          if (response.data.language == "C") this.curlang = 'c'
          if (response.data.language == "Java") this.curlang = 'java'
          if (response.data.language == "Swift5.1") this.curlang = 'swift'

          this.compilemsg = "编译成功！"
          if (row.result != "Accepted")
            this.compilemsg = row.result
          if (response.data.message + "" != "0") this.compilemsg = response.data.message

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
    searchstatus () {
      this.currentpage = 1;
      this.searchdialogVisible = false;
      this.setusername(this.searchform.user);
      this.getstatusdata();
    },
    resetsearch () {
      this.currentpage = 1;
      this.searchform.user = "";
      this.setusername(this.searchform.user);
      this.searchform.problem = "";
      this.searchform.language = "";
      this.searchform.result = "";
      this.creattimer();
    },
    handleSizeChange (val) {
      if (!this.username) this.username = this.$route.query.username;
      this.contest = this.$route.params.contestID;
      if (!this.contest) this.contest = "0";
      if (!this.username) this.username = "";
      this.pagesize = val;
      this.getstatusdata();
    },
    handleCurrentChange (val) {
      if (!this.username) this.username = this.$route.query.username;
      this.contest = this.$route.params.contestID;
      if (!this.contest) this.contest = "0";
      if (!this.username) this.username = "";
      this.currentpage = val;
      this.getstatusdata();
    },
    ratingcolor ({ row, rowIndex }) {
      var back = "";
      if (row.result == "Accepted")
        back = "background:#e6ffdf;font-weight: bold;";

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

    statuetype: function (type) {
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
    statuejudge: function (type) {
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
    timer: function () {
      if (!this.username) this.username = this.$route.query.username;
      this.contest = this.$route.params.contestID;
      if (!this.contest) this.contest = "0";
      if (!this.username) this.username = "";

      if (this.username == sessionStorage.username && sessionStorage.username)
        this.showall = true;
      else this.showall = false;
      this.getstatusdata();
    },

    getstatusdata () {
      this.loading = true;
      var url = ""
      if (this.contest != 0)
        url = "/judgestatus/?user=" +
          this.username +
          "&limit=" +
          this.pagesize +
          "&offset=" +
          (this.currentpage - 1) * this.pagesize +
          "&problemtitle=" +
          this.searchform.problem +
          "&language=" +
          this.searchform.language +
          "&result=" +
          this.searchform.result +
          "&contest=" +
          this.contest
      else
        url = "/judgestatus/?user=" +
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

      this.$axios
        .get(url)
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

    setusername (name) {
      this.$route.query.username = "";
      this.username = name;
    },
    statuechange (val) {
      if (val == true) {
        if (!sessionStorage.username) {
          this.showall = false;
          this.$message.error("请先登录！");
        } else this.setusername(sessionStorage.username);
      } else {
        this.setusername("");
      }
    },
    creattimer () {
      clearInterval(this.$store.state.timer);
      this.timer();
      //this.$store.state.timer = setInterval(this.timer, 60000); 取消自动刷新
    },
    downloadFile (codeid, content) {
      var aLink = document.createElement("a");
      var blob = new Blob([content], { type: "data:text/plain" });
      var downloadElement = document.createElement("a");
      var href = window.URL.createObjectURL(blob); //创建下载的链接
      downloadElement.href = href;
      downloadElement.download = codeid + '.' + this.curlang; //下载后文件名
      document.body.appendChild(downloadElement);
      downloadElement.click(); //点击下载
      document.body.removeChild(downloadElement); //下载完成移除元素
      window.URL.revokeObjectURL(href); //释放掉blob对象
    }
  },
  data () {
    return {
      cmOptions: {
        tabSize: 4,
        mode: "text/x-c++src",
        theme: "base16-light",
        lineNumbers: true,
        readOnly: true,
        cursorBlinkRate:-1,//负数，保留指针但是不显示
        viewportMargin: Infinity,
        lineWrapping: true,
        scrollbarStyle:"simple",
      },
      isadmin: false,
      curid: 0,
      curlang: 'cpp',
      tableData: [],
      currentpage: 1,
      pagesize: 30,
      totalstatus: 10,
      username: "",
      contest: "0",
      showall: false,
      dialogVisible: false,
      searchdialogVisible: false,
      code: "",
      compilemsg: "无权限查看！",
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
  destroyed () {
    clearInterval(this.$store.state.timer);
  },
  created () {
    //创建一个全局定时器，定时刷新状态
    this.isadmin = sessionStorage.type == 2 || sessionStorage.type == 3;
    this.timer();
    //this.$store.state.timer = setInterval(this.timer, 60000);取消自动刷新
  }
};
</script>

