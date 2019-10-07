<template>
  <el-tabs type="card" tab-position="left" @tab-click="problemtabClick">
    <center v-if="!begin">
      <h1>The Contest is Coming</h1>
    </center>
   
    <el-tab-pane v-for="(name,index) in problemtitles" :key="name" v-if="begin">
      <span slot="label" style="float:left;" :ref="'A'+index">
        <i class="el-icon-date"></i>
        Problem {{index | toChar}}:
        {{name}}
      </span>
      <el-col :span="24" v-loading="loading">
        <el-row>
          <el-card shadow="always">
            <el-row :gutter="18" id="title">
              {{currentrankE}}{{' '+title}}
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
              <div
                style="margin-right:50px;word-break:break-all;white-space:pre-line;"
                v-html="des"
                :key="des"
              ></div>
            </el-row>
            <el-row :gutter="18" id="des">Input</el-row>
            <el-row :gutter="18" id="detail">
              <div
                style="margin-right:50px;word-break:break-all;white-space:pre-line;"
                v-html="input"
              ></div>
            </el-row>
            <el-row :gutter="18" id="des">Output</el-row>
            <el-row :gutter="18" id="detail">
              <div
                style="margin-right:50px;word-break:break-all;white-space:pre-line;"
                v-html="output"
              ></div>
            </el-row>

            <el-row :gutter="18" style="left:10px">
              <el-row :gutter="18" v-for="(item,index) in sinput.length" :key="index">
                <el-col :span="11" id="text">
                  <el-row :gutter="18" id="des" style="margin-bottom: 0px;">Sample Input {{item}}<el-button
                      size="mini"
                      v-clipboard:copy="sinput[index]"
                      v-clipboard:success="onCopy"
                      v-clipboard:error="onError"
                      style="margin-left:8px;float:top;"
                    >Copy</el-button>
                  </el-row>
                  <el-row :gutter="18" id="data" style="margin-bottom: 0px;">{{sinput[index]}}</el-row>
                </el-col>
                <el-col :span="11" id="text">
                  <el-row :gutter="18" id="des" style="margin-bottom: 0px;">Sample Output {{item}}</el-row>
                  <el-row :gutter="18" id="data" style="margin-bottom: 0px;">{{soutput[index]}}</el-row>
                </el-col>
              </el-row>
            </el-row>
            <el-row :gutter="18" id="des">Hint</el-row>
            <el-row :gutter="18" id="detail">
              <div
                style="margin-right:50px;word-break:break-all;white-space:pre-line;"
                v-html="hint"
              ></div>
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
                  <el-option key="Java" label="Java" value="Java"></el-option>
                  <el-option key="Python3" label="Python3" value="Python3"></el-option>
                  <el-option key="Swift5.1" label="Swift5.1" value="Swift5.1"></el-option>
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
              <el-col :span="17">
                <codemirror ref="myCm" v-model="code" :options="cmOptions" class="code"></codemirror>
              </el-col>
              <el-col :span="7">
                <statusmini :ref="'Statusmini'+index"></statusmini>
              </el-col>
            </el-row>
          </el-card>
        </el-row>
      </el-col>
    </el-tab-pane>

  </el-tabs>
</template>

<script>
import { codemirror } from "vue-codemirror";
import statusmini from "@/components/utils/statusmini";
import moment from "moment";
require("codemirror/lib/codemirror.css");
require("codemirror/theme/base16-light.css");
require("codemirror/mode/clike/clike");

export default {
  name: "contestproblem",
  components: {
    codemirror,
    statusmini
  },
  data() {
    return {
      cmOptions: {
        tabSize: 4,
        mode: "text/x-c++src",
        theme: "base16-light",
        lineNumbers: true,
        extraKeys: { Ctrl: "autocomplete" },
        viewportMargin: Infinity,
        lineWrapping: true
      },
      begintime: "",
      currenttime: "",
      problemtitles: [],
      problemids: [],
      begin: false,

      title: "",
      des: "",
      input: "",
      output: "",
      sinput: ["", ""],
      soutput: ["", ""],
      author: "",
      addtime: "",
      oj: "",
      source: "",
      time: "",
      memory: "",
      hint: "",
      tagnames: ["", ""],
      activeNames: ["4", "5"],
      level: "Easy",
      code: "",
      language: "C++",
      proid:"0",

      submitbuttontext: "提交后请勿重复刷新/支持将文件拖入代码框",
      judgetype: "primary",
      loadingshow: false,
      submitid: -1,

      currentproblem: -1,
      currentcontest: this.$route.params.contestID,
      currentrank: -1,
      currentrankE: "A",
      loading: false
    };
  },
  filters: {
    toChar(val) {
      var A = "A";
      val = parseInt(val);
      return String.fromCharCode(val + A.charCodeAt());
    }
  },
  watch: {
    des: function() {
      console.log("data changed");
      this.$nextTick().then(() => {
        this.reRender();
      });
    }
  },
  methods: {
    reRender() {
      if (window.MathJax) {
        console.log("rendering mathjax");
        MathJax.Hub.Config({
            tex2jax: {
            inlineMath: [["$", "$"], ["\\(", "\\)"]],
            displayMath: [["$$", "$$"], ["\\[", "\\]"]]
            }
        });
        window.MathJax.Hub.Queue(["Typeset", window.MathJax.Hub], () =>
          console.log("done")
        );
      }
    },
    toCharM(val) {
      var A = "A";
      val = parseInt(val);
      return String.fromCharCode(val + A.charCodeAt());
    },
    onCopy(e) {
      this.$message.success("复制成功！");
    },
    // 复制失败
    onError(e) {
      this.$message.error("复制失败：" + e);
    },
    problemtabClick(tab) {
      this.loading = true;
      clearInterval(this.$store.state.submittimer);
      this.submitbuttontext = "提交后请勿重复刷新/支持将文件拖入代码框";
      this.judgetype = "primary";
      this.loadingshow = false;
      this.submitid = -1;
      this.code = "";
      this.language = "C++";
      this.currentproblem = this.problemids[tab.index];
      this.title = this.problemtitles[tab.index];
      this.currentrank = tab.index;
      this.currentrankE = this.toCharM(tab.index);
      this.$refs["Statusmini" + tab.index][0].setstatus(this.currentproblem,sessionStorage.username,this.$route.params.contestID);
      this.$axios
        .get("/problem/" + this.currentproblem + "/")
        .then(response => {
          this.oj = response.data.oj;
          this.des = response.data.des;
          this.input = response.data.input;
          this.output = response.data.output;
          this.sinput = response.data.sinput.split("|#)"); //分隔符
          this.soutput = response.data.soutput.split("|#)");
          this.author = response.data.author;
          this.source = response.data.source;
          if(this.oj!="LPOJ"){
            this.proid = this.source
          }
          this.time = response.data.time + "MS";
          this.memory = response.data.memory + "MB";
          this.hint = response.data.hint;
          this.loading = false;
        });
      if(sessionStorage.username!=""){
        this.$axios
        .get(
          "/contestboard/?contestid=" +
            this.currentcontest +
            "&username=" +
            sessionStorage.username +
            "&type=1"
        )
        .then(response => {
          for (var ii = 0; ii < this.$store.state.contestproblemcount; ii++)
            this.$refs["A" + ii][0].style["color"] = "black";
          for (var i = 0; i < response.data.length; i++) {
            this.$refs["A" + response.data[i].problemrank][0].style["color"] =
              "#67C23A";    
          }
          this.$refs["A" + tab.index][0].style["color"] = "#409EFF";    
        });
      }
      
    },
    getproblem(id) {
      this.loading = true;
      clearInterval(this.$store.state.submittimer);
      this.submitbuttontext = "提交后请勿重复刷新/支持将文件拖入代码框";
      this.judgetype = "primary";
      this.loadingshow = false;
      this.submitid = -1;
      this.code = "";
      this.language = "C++";

      this.$axios.get("/contestinfo/" + id + "/").then(response => {
        this.begintime = response.data.begintime;
        this.$axios.get("/currenttime/").then(response2 => {
          this.currenttime = response2.data;

          var d1 = new Date(Date.parse(this.currenttime));
          var d2 = new Date(Date.parse(this.begintime));

          var left = parseInt((d1.getTime() - d2.getTime()) / 1000);

          if (left < 0&&(sessionStorage.type==1||sessionStorage.type=="")) {
            this.$message.error("比赛未开始！");
            this.begin = false;
            return;
          }

          this.begin = true;

          this.problemtitles = [];
          this.problemids = [];
          this.$axios
            .get("/contestproblem/?contestid=" + id)
            .then(response3 => {
              for (var i = 0; i < response3.data.length; i++) {
                this.problemtitles.push(response3.data[i].problemtitle);
                this.problemids.push(response3.data[i].problemid);
              }
              this.$store.state.contestproblemcount = this.problemids.length;
              this.currentproblem = this.problemids[0];

              this.currentrank = 0;
              this.currentrankE = "A";
              this.title = this.problemtitles[0];
              this.$axios
                .get("/problem/" + this.currentproblem + "/")
                .then(response => {
                  this.oj = response.data.oj;
                  this.des = response.data.des;
                  this.input = response.data.input;
                  this.output = response.data.output;
                  this.sinput = response.data.sinput.split("|#)"); //分隔符
                  this.soutput = response.data.soutput.split("|#)");
                  this.author = response.data.author;
                  this.source = response.data.source;
                  if(this.oj!="LPOJ"){
                    this.proid = this.source
                  }
                  this.time = response.data.time + "MS";
                  this.memory = response.data.memory + "MB";
                  this.hint = response.data.hint;
                  this.$refs["Statusmini0"][0].setstatus(this.currentproblem,sessionStorage.username,this.$route.params.contestID);
                  this.loading = false;
                });
            });
        });
      });
    },
    submit: function() {
      if (this.hint == "") {
        this.$message.error("非法操作！");
        return;
      }
      // if (this.$store.state.contestisend == true) {
      //   this.$message.error("比赛已结束");
      //   return;
      // }
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

        this.$axios.get("/currenttime/").then(response2 => {
          var curtime = response2.data;

          if (this.$store.state.contestisend == true) {
            this.$axios
              .post("/judgestatusput/", {
                user: sessionStorage.username,
                oj: this.oj,
                problem: this.currentproblem,
                result: -1,
                time: 0,
                memory: 0,
                length: this.code.length,
                language: this.language,
                submittime: curtime,
                judger: "waiting for judger",
                contest: 0,
                contestproblem: -1,
                code: this.code,
                testcase: 0,
                message: this.oj == "LPOJ" ? "0" : this.proid + "",
                problemtitle: "比赛 " + this.currentcontest + this.currentrankE,
                rating: parseInt(sessionStorage.rating)
              })
              .then(response => {
                this.$message({
                  message:
                    "提交成功！比赛已结束，请在菜单栏Status查看具体状态...",
                  type: "success"
                });
                clearInterval(this.$store.state.submittimer);
                this.submitid = response.data.id;
                this.submitbuttontext = "Pending";
                this.judgetype = "info";
                this.loadingshow = true;

                this.$store.state.submittimer = setInterval(this.timer, 1000);
              })
              .catch(error => {
                this.$message.error(
                  "服务器错误！" +
                    "(" +
                    JSON.stringify(error.response.data) +
                    ")"
                );
              });
          } else {
            var date1 = moment(curtime).toDate()
            //var date1 = new Date(Date.parse(curtime)+ ' UTC +8'); 
                      this.$axios
                        .post("/judgestatusput/", {
                          user: sessionStorage.username,
                          oj: this.oj,
                          problem: this.currentproblem,
                          result: -1,
                          time: 0,
                          memory: 0,
                          length: this.code.length,
                          language: this.language,
                          submittime: curtime,
                          judger: "waiting for judger",
                          contest: this.currentcontest,
                          contestproblem: this.currentrank,
                          code: this.code,
                          testcase: 0,
                    message: this.oj == "LPOJ" ? "0" : this.proid + "",
                          problemtitle:
                            "比赛 " + this.currentcontest + this.currentrankE,
                          rating: parseInt(sessionStorage.rating)
                        })
                        .then(response => {
                              this.$message({
                                message: "提交成功！",
                                type: "success"
                              });
                              this.$axios
                        .post("/contestboard/", {
                          username: sessionStorage.username,
                          user: sessionStorage.name,
                          type: -1,
                          submitid: response.data.id,
                          contestid: parseInt(this.currentcontest),
                          problemrank: this.currentrank,
                          submittime: date1.getTime(),
                          rating: parseInt(sessionStorage.rating)
                        })
                        .then(response2 => {
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
                            }).catch(error => {
                          this.$message.error(
                            "服务器错误！" +
                              "(" +
                              JSON.stringify(error.response.data) +
                              ")"
                          );
                        });
                        })
                        .catch(error => {
                          this.$message.error(
                            "服务器错误！" +
                              "(" +
                              JSON.stringify(error.response.data) +
                              ")"
                          );
                        });
          }
        });
      });
    },
    timer: function() {
      if (this.submitbuttontext == "提交后请勿重复刷新/支持将文件拖入代码框")
        return;
      this.$axios.get("/judgestatus/" + this.submitid + "/").then(response => {
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
          if (testcase == "?") response.data["result"] = "Wrong Answer";
          clearInterval(this.$store.state.submittimer);
        }

        if (response.data["result"] == "-4") {
          response.data["result"] = "Compile Error";
          this.judgetype = "warning";
          clearInterval(this.$store.state.submittimer);
        }

        if (response.data["result"] == "-5") {
          response.data["result"] = "Presentation Error on test " + testcase;
          this.judgetype = "warning";
          if (testcase == "?") response.data["result"] = "Presentation Error";
          clearInterval(this.$store.state.submittimer);
        }

        if (response.data["result"] == "-6") {
          response.data["result"] = "Waiting";
          this.loadingshow = true;
          this.judgetype = "info";
        }

        if (response.data["result"] == "0") {
          response.data["result"] = "Accepted";
          this.judgetype = "success";
          clearInterval(this.$store.state.submittimer);
        }

        if (response.data["result"] == "1") {
          response.data["result"] = "Time Limit Exceeded on test " + testcase;
          this.judgetype = "warning";
          if (testcase == "?") response.data["result"] = "Time Limit Exceeded";
          clearInterval(this.$store.state.submittimer);
        }

        if (response.data["result"] == "2") {
          response.data["result"] = "Time Limit Exceeded on test " + testcase;
          this.judgetype = "warning";
          if (testcase == "?") response.data["result"] = "Time Limit Exceeded";
          clearInterval(this.$store.state.submittimer);
        }

        if (response.data["result"] == "3") {
          response.data["result"] = "Memory Limit Exceeded on test " + testcase;
          this.judgetype = "warning";
          if (testcase == "?")
            response.data["result"] = "Memory Limit Exceeded";
          clearInterval(this.$store.state.submittimer);
        }

        if (response.data["result"] == "4") {
          response.data["result"] = "Runtime Error on test " + testcase;
          this.judgetype = "warning";
          if (testcase == "?") response.data["result"] = "Runtime Error";
          clearInterval(this.$store.state.submittimer);
        }

        if (response.data["result"] == "5") {
          response.data["result"] = "System Error";
          this.judgetype = "danger";
          clearInterval(this.$store.state.submittimer);
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
