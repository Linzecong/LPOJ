<template>
  <el-tabs type="card" tab-position="left" @tab-click="problemtabClick">
    <center v-show="!begin">
      <h1>比赛未开始</h1>
    </center>
    <el-tab-pane v-for="(name,index) in problemtitles" :key="index">
      <span slot="label" style="float:left;">
        <i class="el-icon-date"></i>
        Problem {{index | toChar}}:
        {{name}}
      </span>

      <el-col :span="24" v-show="begin">
        <el-row>
          <el-card shadow="always">
            <el-row :gutter="18" id="title">
              {{title}}
              <el-tag
                size="medium"
                disable-transitions
                hit
                style="float:right;margin-right:20px;"
                type="success"
              >{{ time }}</el-tag>
              <el-tag
                size="medium"
                disable-transitions
                hit
                style="float:right;margin-right:20px;"
                type="primary"
              >{{ memory }}</el-tag>
            </el-row>
            <br>
            <el-row :gutter="18" id="des">Description</el-row>
            <el-row :gutter="18" id="detail">
              <div style="margin-right:50px;">
                <el-input type="textarea" v-model="des" autosize readonly></el-input>
              </div>
            </el-row>
            <el-row :gutter="18" id="des">Input</el-row>
            <el-row :gutter="18" id="detail">
              <div style="margin-right:50px;">
                <el-input type="textarea" v-model="input" autosize readonly></el-input>
              </div>
            </el-row>
            <el-row :gutter="18" id="des">Output</el-row>
            <el-row :gutter="18" id="detail">
              <div style="margin-right:50px;">
                <el-input type="textarea" v-model="output" autosize readonly></el-input>
              </div>
            </el-row>

            <el-row :gutter="18" style="left:10px">
              <el-row :gutter="18" v-for="(item,index) in sinput.length" :key="index">
                <el-col :span="11" id="text">
                  <el-row :gutter="18" id="des" style="margin-bottom: 0px;">Sample Input {{item}}</el-row>
                  <el-row :gutter="18" id="data" style="margin-bottom: 0px;">{{sinput[index]}}</el-row>
                </el-col>
                <el-col :span="11" id="text">
                  <el-row :gutter="18" id="des" style="margin-bottom: 0px;">Sample Output {{item}}</el-row>
                  <el-row :gutter="18" id="data" style="margin-bottom: 0px;">{{soutput[index]}}</el-row>
                </el-col>
              </el-row>
            </el-row>

            <el-row :gutter="18" id="des">Source</el-row>
            <el-row :gutter="18" id="detail">
              <div style="margin-right:50px;">{{source}}</div>
            </el-row>
            <el-row :gutter="18" id="des">Hint</el-row>
            <el-row :gutter="18" id="detail">
              <div style="margin-right:50px;">
                <el-input type="textarea" v-model="hint" autosize readonly></el-input>
              </div>
            </el-row>
          </el-card>
        </el-row>
        <el-row>
          <el-card shadow="always">
            <el-row :gutter="15">
              <el-col :span="3">
                <div id="des" style="padding: 5px 10px;">Language:</div>
              </el-col>
              <el-col :span="3">
                <el-select v-model="language" placeholder="请选择">
                  <el-option key="C++" label="C++" value="C++"></el-option>
                  <el-option key="C" label="C" value="C"></el-option>
                </el-select>
              </el-col>
              <el-col :span="3">
                <el-button
                  type="primary"
                  @click="submit"
                  style="font-weight:bold;margin-left:10px;"
                >Submit</el-button>
              </el-col>

              <el-col :span="15">
                <el-button
                  round
                  :type="judgetype"
                  :loading="loadingshow"
                  style="font-weight:bold;margin-left:10px;"
                >{{submitbuttontext}}</el-button>
              </el-col>
            </el-row>
            <el-row :gutter="15">
              <codemirror  ref="myCm"  v-model="code" :options="cmOptions" class="code"></codemirror>
              <!-- <el-input
                type="textarea"
                :autosize="{ minRows: 10, maxRows: 70}"
                placeholder="Please type your code here."
                v-model="code"
              ></el-input> -->

            </el-row>
          </el-card>
        </el-row>
      </el-col>
    </el-tab-pane>
  </el-tabs>
</template>

<script>
import { codemirror } from 'vue-codemirror'
require('codemirror/lib/codemirror.css')
require('codemirror/theme/duotone-light.css')
require('codemirror/mode/clike/clike')
require('codemirror/mode/vue/vue')
require('codemirror/addon/hint/show-hint.js')
require('codemirror/addon/hint/show-hint.css')
require('codemirror/addon/hint/anyword-hint.js')

export default {
  name: "contestproblem",
  components:{
	  codemirror
  },
  data() {
    return {
      cmOptions:{
        tabSize:4,
        mode:'text/x-c++src',
        theme:'duotone-light',
        lineNumbers:true,
        lineWrapping:true,
        showCursorWhenSelecting:true,
        line:true,
        extraKeys: {"Ctrl": "autocomplete"},
      },
      begintime: "",
      currenttime: "",
      problemtitles: [],
      problemids: [],
      begin: false,

      title: "404",
      des: "404",
      input: "404",
      output: "404",
      sinput: ["404", "404"],
      soutput: ["404", "404"],
      author: "404",
      addtime: "404",
      oj: "404",
      source: "404",
      time: "404",
      memory: "404",
      hint: "404",
      tagnames: ["404", "404"],
      activeNames: ["4", "5"],
      level: "Easy",
      code: "",
      language: "",

      submitbuttontext: "提交后请勿重复刷新",
      judgetype: "primary",
      loadingshow: false,
      submitid: -1,

      currentproblem: -1,
      currentcontest: this.$route.params.contestID,
      currentrank: -1
    };
  },
  filters: {
    toChar(val) {
      var A = "A";
      return String.fromCharCode(val + A.charCodeAt());
    }
  },
  methods: {
    problemtabClick(tab) {
      clearInterval(this.$store.state.submittimer);
      this.submitbuttontext = "提交后请勿重复刷新";
      this.judgetype = "primary";
      this.loadingshow = false;
      this.submitid = -1;
      this.code = "";
      this.language = "";
      this.currentproblem = this.problemids[tab.index];
      this.title = this.problemtitles[tab.index];
      this.currentrank = tab.index;
      this.$axios
        .get(
          "/api/problem/" +
            this.currentproblem +
            "/"
        )
        .then(response => {
          this.des = response.data.des;
          this.input = response.data.input;
          this.output = response.data.output;
          this.sinput = response.data.sinput.split("|#)"); //分隔符
          this.soutput = response.data.soutput.split("|#)");
          this.author = response.data.author;
          this.source = response.data.source;
          this.time = response.data.time + "MS";
          this.memory = response.data.memory + "MB";
          this.hint = response.data.hint;
        });
    },
    getproblem(id) {
      clearInterval(this.$store.state.submittimer);
      this.submitbuttontext = "提交后请勿重复刷新";
      this.judgetype = "primary";
      this.loadingshow = false;
      this.submitid = -1;
      this.code = "";
      this.language = "";

      this.$axios
        .get(
          "/api/contestinfo/" + id + "/"
        )
        .then(response => {
          this.begintime = response.data.begintime;
          this.$axios
            .get("http://quan.suning.com/getSysTime.do")
            .then(response2 => {
              this.currenttime = response2.data.sysTime2;

              var d1 = new Date(Date.parse(this.currenttime));
              var d2 = new Date(Date.parse(this.begintime));

              console.log(d1);
              console.log(d2);

              var left = parseInt((d1.getTime() - d2.getTime()) / 1000);

              if (left < 0) {
                this.$message.error("比赛未开始！");
                this.begin = false;
                return;
              }

              this.begin = true;

              this.problemtitles = [];
              this.problemids = [];
              this.$axios
                .get(
                  "/api/contestproblem/?contestid=" +
                    id
                )
                .then(response3 => {
                  for (var i = 0; i < response3.data.length; i++) {
                    this.problemtitles.push(response3.data[i].problemtitle);
                    this.problemids.push(response3.data[i].problemid);
                  }
                  this.$store.state.contestproblemcount = this.problemids.length;
                  this.currentproblem = this.problemids[0];
                  this.currentrank = 0;
                  this.title = this.problemtitles[0];
                  this.$axios
                    .get(
                      "/api/problem/" +
                        this.currentproblem +
                        "/"
                    )
                    .then(response => {
                      this.des = response.data.des;
                      this.input = response.data.input;
                      this.output = response.data.output;
                      this.sinput = response.data.sinput.split("|#)"); //分隔符
                      this.soutput = response.data.soutput.split("|#)");
                      this.author = response.data.author;
                      this.source = response.data.source;
                      this.time = response.data.time + "MS";
                      this.memory = response.data.memory + "MB";
                      this.hint = response.data.hint;
                    });
                });
            });
        });
    },
    submit: function() {
      if (this.hint == "404") {
        this.$message.error("非法操作！");
        return;
      }
      if (this.$store.state.contestisend == true) {
        this.$message.error("比赛已结束");
        return;
      }
      if (!sessionStorage.username) {
        this.$message.error("请先登录！");
        return;
      }
      if (!this.code) {
        this.$message.error("请输入代码！");
        return;
      }
      if (!this.language) {
        this.$message.error("请选择语言！");
        return;
      }
      this.$confirm("确定提交该题吗？ 题目：" + this.title, "提交确认", {
        confirmButtonText: "确定",
        cancelButtonText: "取消",
        type: "warning"
      }).then(() => {
        this.$message({
          type: "success",
          message: "提交中..."
        });

        this.$axios
          .get(
            "/api/contestrank/?contestid=" +
              parseInt(this.currentcontest) +
              "&username=" +
              sessionStorage.username
          )
          .then(response5 => {
            if (response5.data.length > 0) {
              this.$axios
                .post(
                  "/api/judgestatusput/",
                  {
                    user: sessionStorage.username,
                    oj: "LPOJ",
                    problem: this.currentproblem,
                    result: -1,
                    time: 0,
                    memory: 0,
                    length: this.code.length,
                    language: this.language,
                    judger: "waiting for judger",
                    contest: this.currentcontest,
                    contestproblem: this.currentrank,
                    code: this.code,
                    testcase: 0,
                    message: "0"
                  }
                )
                .then(response => {
                  var date1 = new Date(Date.parse(response.data.submittime));

                  this.$axios
                    .post(
                      "/api/contestboard/",
                      {
                        username: sessionStorage.username,
                        user: sessionStorage.name,
                        type: -1,
                        submitid: response.data.id,
                        contestid: parseInt(this.currentcontest),
                        problemrank: this.currentrank,
                        submittime: date1.getTime()
                      }
                    )
                    .then(response2 => {
                      this.$message({
                        message: "提交成功！",
                        type: "success"
                      });
                      clearInterval(this.$store.state.submittimer);
                      this.submitid = response.data.id;
                      this.submitbuttontext = "Pending";
                      this.judgetype = "info";
                      this.loadingshow = true;
                      //创建一个全局定时器，定时刷新状态
                      this.$store.state.submittimer = setInterval(
                        this.timer,
                        1000
                      );
                    });
                })
                .catch(error => {
                  this.$message.error("服务器错误！" + "(" + error + ")");
                });
            } else {
              var str = "";
              for (var i = 0; i < this.problemids.length - 1; i++)
                str = str + "0|";
              str = str + "0";

              this.$axios
                .post(
                  "/api/contestrank/",
                  {
                    username: sessionStorage.username,
                    user: sessionStorage.name,
                    contestid: parseInt(this.currentcontest),
                    statue: str
                  }
                )
                .then(response8 => {
                  this.$axios
                    .post(
                      "/api/judgestatusput/",
                      {
                        user: sessionStorage.username,
                        oj: "LPOJ",
                        problem: this.currentproblem,
                        result: -1,
                        time: 0,
                        memory: 0,
                        length: this.code.length,
                        language: this.language,
                        judger: "waiting for judger",
                        contest: this.currentcontest,
                        contestproblem: this.currentrank,
                        code: this.code,
                        testcase: 0,
                        message: "0"
                      }
                    )
                    .then(response => {
                      var date1 = new Date(
                        Date.parse(response.data.submittime)
                      );

                      this.$axios
                        .post(
                          "/api/contestboard/",
                          {
                            username: sessionStorage.username,
                            user: sessionStorage.name,
                            type: -1,
                            submitid: response.data.id,
                            contestid: parseInt(this.currentcontest),
                            problemrank: this.currentrank,
                            submittime: date1.getTime()
                          }
                        )
                        .then(response2 => {
                          this.$message({
                            message: "提交成功！",
                            type: "success"
                          });
                          clearInterval(this.$store.state.submittimer);
                          this.submitid = response.data.id;
                          this.submitbuttontext = "Pending";
                          this.judgetype = "info";
                          this.loadingshow = true;
                          //创建一个全局定时器，定时刷新状态
                          this.$store.state.submittimer = setInterval(
                            this.timer,
                            1000
                          );
                        });
                    })
                    .catch(error => {
                      this.$message.error("服务器错误！" + "(" + error + ")");
                    });
                })
                .catch(error => {
                  this.$message.error("服务器错误！" + "(" + error + ")");
                });
            }
          })
          .catch(error => {
            this.$message.error("服务器错误！" + "(" + error + ")");
          });
      });
    },
    timer: function() {
      if (this.submitbuttontext == "提交后请勿重复刷新") return;
      this.$axios
        .get(
          "/api/judgestatus/" +
            this.submitid +
            "/"
        )
        .then(response => {
          this.loadingshow = false;
          var testcase = response.data["testcase"];
          if (response.data["result"] == "-1") {
            response.data["result"] = "Pending";
            this.loadingshow = true;
            this.judgetype = "info";
          }

          if (response.data["result"] == "-2") {
            response.data["result"] = "Judging";
            this.loadingshow = true;
            this.judgetype = "";
          }

          if (response.data["result"] == "-3") {
            response.data["result"] = "Wrong Answer on test " + testcase;
            this.judgetype = "danger";
          }

          if (response.data["result"] == "-4") {
            response.data["result"] = "Compile Error";
            this.judgetype = "warning";
          }

          if (response.data["result"] == "-5") {
            response.data["result"] = "Presentation Error on test " + testcase;
            this.judgetype = "warning";
          }

          if (response.data["result"] == "-6") {
            response.data["result"] = "Waiting";
            this.loadingshow = true;
            this.judgetype = "info";
          }

          if (response.data["result"] == "0") {
            response.data["result"] = "Accepted";
            this.judgetype = "success";
          }

          if (response.data["result"] == "1") {
            response.data["result"] = "Time Limit Exceeded on test " + testcase;
            this.judgetype = "warning";
          }

          if (response.data["result"] == "2") {
            response.data["result"] = "Time Limit Exceeded on test " + testcase;
            this.judgetype = "warning";
          }

          if (response.data["result"] == "3") {
            response.data["result"] =
              "Memory Limit Exceeded on test " + testcase;
            this.judgetype = "warning";
          }

          if (response.data["result"] == "4") {
            response.data["result"] = "Runtime Error on test " + testcase;
            this.judgetype = "warning";
          }

          if (response.data["result"] == "5") {
            response.data["result"] = "System Error";
            this.judgetype = "danger";
          }

          this.submitbuttontext = response.data["result"];
        });
    }
  },
  created() {
    this.getproblem(this.$route.params.contestID);
  },
  destroyed() {
    clearInterval(this.$store.state.submittimer);
  }
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
#tag {
  text-align: center;
  font-weight: bold;
  margin-right: 13px;
  margin-bottom: 13px;
}
#title {
  color: dimgrey;
  left: 10px;
  font-size: 20px;
}
#des {
  color: deepskyblue;
  font-weight: bold;
  left: 20px;
  font-size: 20px;
}
#detail {
  left: 30px;
  font-size: 16px;
}
#text {
  font-weight: normal;
  font-size: 15px;
  white-space: pre-wrap;
  margin-right: 40px;
}
#data {
  left: 30px;
  padding: 5px 10px;
  color: dimgray;
  background: #f8f8f9;
  border: 1px dashed #e9eaec;
}

.el-row {
  margin-bottom: 20px;
}
</style>
