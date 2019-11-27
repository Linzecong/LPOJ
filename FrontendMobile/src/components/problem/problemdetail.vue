<template>
  <mu-container>
    <mu-card raised>
      <mu-card-header
        :title="(this.oj=='LPOJ'?'LPOJ':'')+(this.oj=='LPOJ'?' - ':'')+(this.oj=='LPOJ'?this.proid:'')"
        :sub-title="time+'   '+memory"
      ></mu-card-header>

      <mu-card-title :title="title"></mu-card-title>

      <mu-card-text>
        <div style="word-break:break-all;white-space:pre-line;" v-html="des" :key="des"></div>
      </mu-card-text>

      <mu-card-text>
        <mu-row id="des">Input</mu-row>
        <br />

        <div style="word-break:break-all;white-space:pre-line;" v-html="input"></div>
      </mu-card-text>

      <mu-card-text>
        <mu-row id="des">Output</mu-row>
        <br />
        <div style="word-break:break-all;white-space:pre-line;" v-html="output"></div>
      </mu-card-text>

      <mu-card-text>
        <mu-row v-for="(item,index) in sinput.length" :key="index" gutter style="margin-top:10px;">
          <mu-col span="5" id="text">
            <font id="des" style="margin-bottom: 0px;">Input {{item}}</font>

            <mu-button
              icon
              small
              color="primary"
              v-clipboard:copy="sinput[index]"
              v-clipboard:success="onCopy"
              v-clipboard:error="onError"
            >
              <mu-icon value="assignment"></mu-icon>
            </mu-button>
            <br />

            <mu-row id="data" style="margin-bottom: 0px;">{{sinput[index]}}</mu-row>
          </mu-col>

          <mu-col span="5" id="text" offset="1">
            <font id="des" style="margin-bottom: 0px;">Output {{item}}</font>
            <br />
            <mu-row id="data" style="margin-bottom: 0px;">{{soutput[index]}}</mu-row>
          </mu-col>
        </mu-row>
      </mu-card-text>

      <mu-card-text>
        <mu-row id="des">Source</mu-row>
        <br />
        <div>{{source}}</div>
      </mu-card-text>

      <mu-card-text>
        <mu-row id="des">Hint</mu-row>
        <br />
        <div style="word-break:break-all;white-space:pre-line;" v-html="hint"></div>
      </mu-card-text>
    </mu-card>

    <br />

    <mu-card raised>
      <mu-card-text>
        <mu-select v-model="language" label="Choose a language..." full-width @change="changetemplate">
          <mu-option v-for="item in languagelist" :key="item" :label="item" :value="item"></mu-option>
        </mu-select>

        <br />

        <codemirror
          style="font-size:12px;"
          v-model="code"
          :options="cmOptions"
          @changes="judgetype='success';submitbuttontext='submit'"
        ></codemirror>
        <br />

        <mu-button full-width :color="judgetype" @click="confirmdialog = true">{{submitbuttontext}}</mu-button>

        <mu-dialog
          title="Submit?"
          :esc-press-close="false"
          :overlay-close="false"
          :open.sync="confirmdialog"
        >
          Want to submit your code ?
          <mu-button slot="actions" flat color="primary" @click="confirmdialog = false">No</mu-button>
          <mu-button slot="actions" flat color="primary" @click="submit">Yes</mu-button>
        </mu-dialog>
      </mu-card-text>
    </mu-card>
  </mu-container>
</template>

<style scope>
.CodeMirror {
  height: 500px;
}
</style>
<script>
import moment from "moment";
import { codemirror } from "vue-codemirror";
require("codemirror/lib/codemirror.css");
require("codemirror/theme/base16-light.css");
require("codemirror/mode/clike/clike");
export default {
  name: "problemdetail",
  components: {
    codemirror
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
      proid: "",
      source: "",
      time: "",
      memory: "",
      hint: "",
      tagnames: [],
      activeNames: ["1", "2", "3", "4", "5", "6"],
      level: "Easy",
      code: "",
      language: "Python2",

      codetemplate:{},
      languagelist: ["C++","C","Python3","Python2","Swift5.1","Java"],

      ac: 100,
      mle: 100,
      tle: 100,
      rte: 100,
      pe: 100,
      ce: 100,
      wa: 100,
      se: 100,
      submitbuttontext: "Submit",
      judgetype: "success",
      loadingshow: false,
      submitid: -1,
      confirmdialog: false
    };
  },
  watch: {
    des: function() {
      console.log("data changed");
      this.$nextTick().then(() => {
        this.reRender();
      });
    }
  },
  created() {
    this.ID = this.$route.query.problemID;
    if (!this.ID) {
      this.$toast.error("参数错误" + "(" + this.ID + ")");
      return;
    }
    var auth = 1;
    this.$axios
      .get("/problem/" + this.ID + "/")
      .then(response => {
        auth = response.data.auth;
        if (
          (auth == 2 || auth == 3) &&
          (sessionStorage.type == 1 || sessionStorage.type == "")
        ) {
          this.title = "非法访问！";
          this.$toast.error("服务器错误！" + "(" + "无权限" + ")");
          return;
        }
        this.proid = this.ID;
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

        var li = response.data.template.split("*****")
        for(var i = 1; i < li.length; i+=2){
          this.codetemplate[li[i]]=li[i+1]
        }
        this.code = this.codetemplate[this.language]

        if (this.oj != "LPOJ") {
          this.proid = this.source;
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
            this.$refs.prosta.setdata(this.$data);
            console.log(this.$refs["Statusmini"]);
            this.$refs["Statusmini"].setstatus(
              this.ID,
              sessionStorage.username,
              ""
            );
          })
          .catch(error => {
            this.$toast.error(
              "服务器错误！" + "(" + JSON.stringify(error.response.data) + ")"
            );
          });
      })
      .catch(error => {
        this.title = "非法访问！";
        this.$toast.error(
          "服务器错误！" + "(" + JSON.stringify(error.response.data) + ")"
        );
      });

      this.$axios
      .get("/settingboard/")
      .then(res => {
        if (res.data.length > 0) {
          this.languagelist = res.data[0].openlanguage.split("|");
        } 
      })
      .catch(error => {
        this.$message.error(
          "服务器错误！" + "(" + JSON.stringify(error.response.data) + ")"
        );
      });
  },
  methods: {
    changetemplate(lang){
      
      this.code = this.codetemplate[lang]

    },
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
    onCopy(e) {
      this.$toast.success("复制成功！");
    },
    // 复制失败
    onError(e) {
      this.$toast.error("复制失败：" + e);
    },
    problemlevel: function(type) {
      if (type == "Easy") return "info";
      if (type == "Medium") return "success";
      if (type == "Hard") return "";
      if (type == "VeryHard") return "warning";
      if (type == "ExtremelyHard") return "danger";
    },
    submit: function() {
      this.confirmdialog = false
      if (this.addtime == "") {
        this.$toast.error("非法操作！");
        return;
      }
      if (!sessionStorage.username) {
        this.$toast.error("请先登录！");
        return;
      }
      if (!this.code) {
        this.$toast.error("请输入代码！");
        return;
      }
      if (!this.language) {
        this.$toast.error("请选择语言！");
        return;
      }

      this.$toast.success("提交中...");
      this.$axios.get("/currenttime/").then(response2 => {
        var curtime = response2.data;
        this.$axios
          .post("/judgestatusput/", {
            user: sessionStorage.username,
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
            message: this.oj == "LPOJ" ? "0" : this.proid + "",
            problemtitle:
              (this.oj == "LPOJ" ? "LPOJ" : "") +
              (this.oj == "LPOJ" ? " - " : "") +
              (this.oj == "LPOJ" ? this.proid : "") +
              " " +
              this.title,
            rating: parseInt(sessionStorage.rating)
          })
          .then(response => {
            this.$toast.success("提交成功！");
            clearInterval(this.$store.state.submittimer);
            this.submitid = response.data.id;
            this.submitbuttontext = "Pending";
            this.judgetype = "info";
            this.loadingshow = true;
            //创建一个全局定时器，定时刷新状态
            this.$store.state.submittimer = setInterval(this.timer, 1000);
          })
          .catch(error => {
            this.$toast.error(
              "服务器错误！" + "(" + JSON.stringify(error.response.data) + ")"
            );
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
          this.judgetype = "error";
          clearInterval(this.$store.state.submittimer);
          if (testcase == "?") response.data["result"] = "Wrong Answer";
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
          if (testcase == "?") response.data["result"] = "Presentation Error";
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
          if (testcase == "?") response.data["result"] = "Time Limit Exceeded";
        }

        if (response.data["result"] == "2") {
          response.data["result"] = "Time Limit Exceeded on test " + testcase;
          this.judgetype = "warning";
          clearInterval(this.$store.state.submittimer);
          if (testcase == "?") response.data["result"] = "Time Limit Exceeded";
        }

        if (response.data["result"] == "3") {
          response.data["result"] = "Memory Limit Exceeded on test " + testcase;
          this.judgetype = "warning";
          clearInterval(this.$store.state.submittimer);
          if (testcase == "?")
            response.data["result"] = "Memory Limit Exceeded";
        }

        if (response.data["result"] == "4") {
          response.data["result"] = "Runtime Error on test " + testcase;
          this.judgetype = "warning";
          clearInterval(this.$store.state.submittimer);
          if (testcase == "?") response.data["result"] = "Runtime Error";
        }

        if (response.data["result"] == "5") {
          response.data["result"] = "System Error";
          this.judgetype = "error";
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
  font-size: 20px;
}
#detail {
  font-size: 16px;
}
#text {
  font-weight: normal;
  font-size: 15px;
  white-space: pre-wrap;
  margin-right: 10px;
}
#data {
  left: 30px;
  padding: 5px 10px;
  color: dimgray;
  background: #f8f8f9;
  border: 1px dashed #e9eaec;
}

.mu-row {
  margin-bottom: 20px;
}
</style>
