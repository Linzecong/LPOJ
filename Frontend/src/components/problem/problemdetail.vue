<template>
  <el-row :gutter="15">
    <el-col :span="18">
      <el-row>
        <el-card shadow="always">
          <el-row :gutter="18" id="title">{{(this.oj=="LPOJ"?"LPOJ":"")+' - '+(this.oj=="LPOJ"?this.proid:"")+' '}}{{title}}</el-row>
          <br>
          <el-row :gutter="18" id="des">Description</el-row>
          <el-row :gutter="18" id="detail">
            <div style="margin-right:50px;word-break:break-all;white-space:pre-line;" v-html="des" :key="des"></div>
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

          <el-row :gutter="18" id="des">Source</el-row>
          <el-row :gutter="18" id="detail">
            <div style="margin-right:50px;">{{source}}</div>
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
          <el-row>
            <codemirror v-model="code" :options="cmOptions"></codemirror>
          </el-row>
        </el-card>
      </el-row>
    </el-col>

    <el-col :span="6">
      <el-row :gutter="15">
        <el-card shadow="always">
          <el-collapse v-model="activeNames">
            <el-collapse-item name="1" id="des">
              <template slot="title">
                <font color="deepskyblue" size="4">Creator:</font>
              </template>
              <div>{{author}}</div>
            </el-collapse-item>
            <el-collapse-item name="2" id="des">
              <template slot="title">
                <font color="deepskyblue" size="4">Date:</font>
              </template>
              <div>{{addtime}}</div>
            </el-collapse-item>
            <el-collapse-item name="3" id="des">
              <template slot="title">
                <font color="deepskyblue" size="4">OJ:</font>
              </template>
              <div>{{oj}}</div>
            </el-collapse-item>
            <el-collapse-item name="4" id="des">
              <template slot="title">
                <font color="deepskyblue" size="4">Time:</font>
              </template>
              <div>{{time}}</div>
            </el-collapse-item>
            <el-collapse-item name="5" id="des">
              <template slot="title">
                <font color="deepskyblue" size="4">Memory:</font>
              </template>
              <div>{{memory}}</div>
            </el-collapse-item>
            <el-collapse-item name="7" id="des">
              <template slot="title">
                <font color="deepskyblue" size="4">Level:</font>
              </template>
              <el-tag size="medium" :type="problemlevel(level)" disable-transitions hit>{{ level }}</el-tag>
            </el-collapse-item>
            <el-collapse-item name="6" id="des">
              <template slot="title">
                <font color="deepskyblue" size="4">Tags:</font>
              </template>
              <el-tag
                id="tag"
                v-for="(name,index) in tagnames"
                :key="index"
                size="medium"
                type="info"
                disable-transitions
                hit
              >{{ name }}</el-tag>
            </el-collapse-item>
          </el-collapse>
        </el-card>
      </el-row>
      <el-row :gutter="15">
        <prostatistice ref="prosta"></prostatistice>
      </el-row>
      <el-row :gutter="15">
        <el-card>
          <h3>提交记录</h3>
          <statusmini></statusmini>
        </el-card>
      </el-row>
    </el-col>
  </el-row>
</template>

<style scope>
.CodeMirror {
  height: 500px;
}
</style>
<script>
import moment from "moment";
import { codemirror } from "vue-codemirror";
import statusmini from "@/components/utils/statusmini";
import prostatistice from "@/components/utils/prostatistice";
require("codemirror/lib/codemirror.css");
require("codemirror/theme/base16-light.css");
require("codemirror/mode/clike/clike");

export default {
  name: "problemdetail",
  components: {
    codemirror,
    statusmini,
    prostatistice
  },
  data() {
    return {
      cmOptions: {
        tabSize: 4,
        mode: "text/x-c++src",
        theme: "base16-light",
        lineNumbers: true
      },
      title: "",
      des: "",
      input: "",
      output: "",
      sinput: ["", ""],
      soutput: ["", ""],
      author: "",
      addtime: "",
      oj: "",
      proid:"",
      source: "",
      time: "",
      memory: "",
      hint: "",
      tagnames: [],
      activeNames: ["1", "2", "3", "4", "5", "6"],
      level: "Easy",
      code: "",
      language: "C++",

      ac: 100,
      mle: 100,
      tle: 100,
      rte: 100,
      pe: 100,
      ce: 100,
      wa: 100,
      se: 100,
      submitbuttontext: "提交后请勿重复刷新/支持将文件拖入代码框",
      judgetype: "primary",
      loadingshow: false,
      submitid: -1
    };
  },
  watch: {
    des: function() {
      console.log('data changed');
      this.$nextTick().then(()=>{
        this.reRender();
      });
    }
  },
  created() {
    this.ID = this.$route.query.problemID;
    if (!this.ID) {
      this.$message.error("参数错误" + "(" + this.ID + ")");
      return;
    }
    var auth = 1;
    this.$axios
      .get("/problem/" + this.ID + "/")
      .then(response => {
        auth = response.data.auth;
        if ((auth == 2 || auth == 3) && (localStorage.type == 1||localStorage.type =="")) {
          this.title = "非法访问！";
          this.$message.error("服务器错误！" + "(" + "无权限" + ")");
          return;
        }
        this.proid = this.ID
        this.des = response.data.des;
        this.input = response.data.input;
        this.output = response.data.output;
        this.sinput = response.data.sinput.split("|#)"); //分隔符
        this.soutput = response.data.soutput.split("|#)");
        this.author = response.data.author;
        this.addtime = response.data["addtime"] = moment(
          response.data["addtime"]
        ).format("YYYY-MM-DD HH:mm:ss");

        this.oj = response.data.oj;
        this.source = response.data.source;
        this.time = response.data.time + "MS";
        this.memory = response.data.memory + "MB";
        this.hint = response.data.hint;

        if(this.oj!="LPOJ"){
          this.proid = this.source
        }

        this.$axios
          .get("/problemdata/" + this.ID + "/")
          .then(response => {
            if (response.data["level"] == "1") response.data["level"] = "Easy";
            if (response.data["level"] == "2")
              response.data["level"] = "Medium";
            if (response.data["level"] == "3") response.data["level"] = "Hard";
            if (response.data["level"] == "4")
              response.data["level"] = "VeryHard";
            if (response.data["level"] == "5")
              response.data["level"] = "ExtremelyHard";

            if (response.data["tag"] == null) response.data["tag"] = ["无"];
            else response.data["tag"] = response.data["tag"].split("|");

            if (response.data.submission == 0) {
              this.ac = 0;
              this.mle = 0;
              this.tle = 0;
              this.rte = 0;
              this.pe = 0;
              this.ce = 0;
              this.wa = 0;
              this.se = 0;
            } else {
              this.ac = parseFloat(
                ((response.data.ac * 100) / response.data.submission).toFixed(2)
              );
              this.mle = parseFloat(
                ((response.data.mle * 100) / response.data.submission).toFixed(
                  2
                )
              );
              this.tle = parseFloat(
                ((response.data.tle * 100) / response.data.submission).toFixed(
                  2
                )
              );
              this.rte = parseFloat(
                ((response.data.rte * 100) / response.data.submission).toFixed(
                  2
                )
              );
              this.pe = parseFloat(
                ((response.data.pe * 100) / response.data.submission).toFixed(2)
              );
              this.ce = parseFloat(
                ((response.data.ce * 100) / response.data.submission).toFixed(2)
              );
              this.wa = parseFloat(
                ((response.data.wa * 100) / response.data.submission).toFixed(2)
              );
              this.se = parseFloat(
                ((response.data.se * 100) / response.data.submission).toFixed(2)
              );
            }
            this.title = response.data.title;
            this.level = response.data.level;
            this.tagnames = response.data.tag;
            this.$refs.prosta.setdata(this.$data)
          })
          .catch(error => {
            this.$message.error("服务器错误！" + "(" + JSON.stringify(error.response.data) + ")");
          });
      })
      .catch(error => {
        this.title = "非法访问！";
        this.$message.error("服务器错误！" + "(" + JSON.stringify(error.response.data) + ")");
      });
  },
  methods: {
    reRender() {
      if(window.MathJax) {
        console.log('rendering mathjax');
        MathJax.Hub.Config({
            tex2jax: {
                inlineMath: [ ['$','$'], ["\\(","\\)"] ],
                displayMath: [ ['$$','$$'], ["\\[","\\]"] ]
            }
        });
        window.MathJax.Hub.Queue(["Typeset", window.MathJax.Hub], () => console.log('done'));
      }
    },
    onCopy(e) {
      this.$message.success("复制成功！");
    },
    // 复制失败
    onError(e) {
      this.$message.error("复制失败：" + e);
    },
    problemlevel: function(type) {
      if (type == "Easy") return "info";
      if (type == "Medium") return "success";
      if (type == "Hard") return "";
      if (type == "VeryHard") return "warning";
      if (type == "ExtremelyHard") return "danger";
    },
    submit: function() {
      if (this.addtime == "") {
        this.$message.error("非法操作！");
        return;
      }
      if (!localStorage.username) {
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
      this.$confirm("确定提交吗？", "提交", {
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
          this.$axios
            .post("/judgestatusput/", {
              user: localStorage.username,
              oj: this.oj,
              problem: this.ID,
              result: -1,
              time: 0,
              memory: 0,
              length: this.code.length,
              language: this.language,
              submittime: curtime,
              judger: "waiting for judger",
              contest: 0,
              code: this.code,
              testcase: 0,
              message: this.oj=="LPOJ"?"0":(this.proid+""),
              problemtitle: this.oj+" - " + this.proid + " " + this.title,
              rating: parseInt(localStorage.rating)
            })
            .then(response => {
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
              this.$store.state.submittimer = setInterval(this.timer, 1000);
            })
            .catch(error => {
              this.$message.error("服务器错误！" + "(" + JSON.stringify(error.response.data) + ")");
            });
        });
      });
    },
    timer: function() {
      if (this.submitbuttontext == "提交后请勿重复刷新/支持将文件拖入代码框") return;
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
          clearInterval(this.$store.state.submittimer);
          if(testcase=="?")
                response.data["result"] ="Wrong Answer"
        }

        if (response.data["result"] == "-4") {
          response.data["result"] = "Compile Error";
          this.judgetype = "warning";
          clearInterval(this.$store.state.submittimer);
        }

        if (response.data["result"] == "-5") {
          response.data["result"] = "Presentation Error on test " + testcase;
          this.judgetype = "warning";
          clearInterval(this.$store.state.submittimer);
          if(testcase=="?")
                response.data["result"] ="Presentation Error"
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
          clearInterval(this.$store.state.submittimer);
          if(testcase=="?")
                response.data["result"] ="Time Limit Exceeded"
        }

        if (response.data["result"] == "2") {
          response.data["result"] = "Time Limit Exceeded on test " + testcase;
          this.judgetype = "warning";
          clearInterval(this.$store.state.submittimer);
          if(testcase=="?")
                response.data["result"] ="Time Limit Exceeded"
        }

        if (response.data["result"] == "3") {
          response.data["result"] = "Memory Limit Exceeded on test " + testcase;
          this.judgetype = "warning";
          clearInterval(this.$store.state.submittimer);
          if(testcase=="?")
                response.data["result"] ="Memory Limit Exceeded"
        }

        if (response.data["result"] == "4") {
          response.data["result"] = "Runtime Error on test " + testcase;
          this.judgetype = "warning";
          clearInterval(this.$store.state.submittimer);
          if(testcase=="?")
                response.data["result"] ="Runtime Error"
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
