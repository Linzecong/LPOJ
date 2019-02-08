<template>
  <el-row :gutter="15">
    <el-col :span="20">
      <el-row>
        <el-card shadow="always">
          <el-row :gutter="18" id="title">{{title}}</el-row>
          <br>
          <el-row :gutter="18" id="des">Description</el-row>
          <el-row :gutter="18" id="detail">
            <div style="margin-right:50px;">{{des}}</div>
          </el-row>
          <el-row :gutter="18" id="des">Input</el-row>
          <el-row :gutter="18" id="detail">
            <div style="margin-right:50px;">{{input}}</div>
          </el-row>
          <el-row :gutter="18" id="des">Output</el-row>
          <el-row :gutter="18" id="detail">
            <div style="margin-right:50px;">{{output}}</div>
          </el-row>

          <el-row :gutter="18" style="left:10px">
            <el-col :span="11" id="text">
              <el-row :gutter="18" v-for="(item,index) in sinput.length">
                <el-row :gutter="18" id="des" style="margin-bottom: 0px;">Sample Input {{item}}</el-row>
                <el-row :gutter="18" id="data" style="margin-bottom: 0px;">{{sinput[index]}}</el-row>
              </el-row>
            </el-col>
            <el-col :span="11" id="text">
              <el-row :gutter="18" v-for="(item,index) in sinput.length">
                <el-row :gutter="18" id="des" style="margin-bottom: 0px;">Sample Output {{item}}</el-row>
                <el-row :gutter="18" id="data" style="margin-bottom: 0px;">{{soutput[index]}}</el-row>
              </el-row>
            </el-col>
          </el-row>

          <el-row :gutter="18" id="des">Source</el-row>
          <el-row :gutter="18" id="detail">
            <div style="margin-right:50px;">{{source}}</div>
          </el-row>
          <el-row :gutter="18" id="des">Hint</el-row>
          <el-row :gutter="18" id="detail">
            <div style="margin-right:50px;">{{hint}}</div>
          </el-row>
        </el-card>
      </el-row>
      <el-row>
        <el-card shadow="always">
          <el-row :gutter="15">
            <el-col :span="1">
              <div id="des" style="padding: 5px 10px;">Language:</div>
            </el-col>
            <el-col :span="2" style="margin-left:60px;">
              <el-select v-model="language" placeholder="请选择">
                <el-option key="C++" label="C++" value="C++"></el-option>
                <el-option key="C" label="C" value="C"></el-option>
              </el-select>
            </el-col>
            <el-col :span="18">
              <el-button
                type="primary"
                @click="submit"
                style="font-weight:bold;margin-left:10px;"
              >Submit</el-button>
            </el-col>
          </el-row>
          <el-row :gutter="15">
            <el-input
              type="textarea"
              :autosize="{ minRows: 10, maxRows: 70}"
              placeholder="Please type your code here."
              v-model="code"
            ></el-input>
          </el-row>
        </el-card>
      </el-row>
    </el-col>

    <el-col :span="4">
      <el-row :gutter="15">
        <el-card shadow="always">
          <el-collapse v-model="activeNames">
            <el-collapse-item name="1" id="des">
              <template slot="title">
                <font color="deepskyblue" size="4">Author:</font>
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
                v-for="name in tagnames"
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
        <el-card shadow="always">
          <h2>{{title}}</h2>

          <el-row :gutter="10">
            <el-col :span="3">
              <b>AC:</b>
            </el-col>
            <el-col :span="21">
              <el-progress :text-inside="true" :stroke-width="18" :percentage="ac" status="success"></el-progress>
            </el-col>
          </el-row>

          <el-row :gutter="10">
            <el-col :span="3">
              <b>WA:</b>
            </el-col>
            <el-col :span="21">
              <el-progress
                :text-inside="true"
                :stroke-width="18"
                :percentage="wa"
                status="exception"
              ></el-progress>
            </el-col>
          </el-row>
          <el-row :gutter="10">
            <el-col :span="3">
              <b>PE:</b>
            </el-col>
            <el-col :span="21">
              <el-progress :text-inside="true" :stroke-width="18" :percentage="pe" color="#FF9800"></el-progress>
            </el-col>
          </el-row>
          <el-row :gutter="10">
            <el-col :span="3">
              <b>TLE:</b>
            </el-col>
            <el-col :span="21">
              <el-progress :text-inside="true" :stroke-width="18" :percentage="tle" color="#FF9800"></el-progress>
            </el-col>
          </el-row>
          <el-row :gutter="10">
            <el-col :span="3">
              <b>RTE:</b>
            </el-col>
            <el-col :span="21">
              <el-progress :text-inside="true" :stroke-width="18" :percentage="rte" color="#FF9800"></el-progress>
            </el-col>
          </el-row>
          <el-row :gutter="10">
            <el-col :span="3">
              <b>MLE:</b>
            </el-col>
            <el-col :span="21">
              <el-progress :text-inside="true" :stroke-width="18" :percentage="mle" color="#795548"></el-progress>
            </el-col>
          </el-row>

          <el-row :gutter="10">
            <el-col :span="3">
              <b>CE:</b>
            </el-col>
            <el-col :span="21">
              <el-progress :text-inside="true" :stroke-width="18" :percentage="ce" color="#FFC107"></el-progress>
            </el-col>
          </el-row>

          <el-row :gutter="10">
            <el-col :span="3">
              <b>SE:</b>
            </el-col>
            <el-col :span="21">
              <el-progress
                :text-inside="true"
                :stroke-width="18"
                :percentage="se"
                status="exception"
              ></el-progress>
            </el-col>
          </el-row>
        </el-card>
      </el-row>
    </el-col>
  </el-row>
</template>

<script>
export default {
  name: "problemdetail",
  data() {
    return {
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
      language:"",

      ac: 100,
      mle: 100,
      tle: 100,
      rte: 100,
      pe: 100,
      ce: 100,
      wa: 100,
      se: 100
    };
  },
  created() {
    this.ID = this.$route.params.problemID;
    this.$http
      .get("http://localhost:8000/problemdata/" + this.ID)
      .then(response => {
        if (response.data["level"] == "1") response.data["level"] = "Easy";
        if (response.data["level"] == "2") response.data["level"] = "Medium";
        if (response.data["level"] == "3") response.data["level"] = "Hard";
        if (response.data["level"] == "4") response.data["level"] = "VeryHard";
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
            ((response.data.mle * 100) / response.data.submission).toFixed(2)
          );
          this.tle = parseFloat(
            ((response.data.tle * 100) / response.data.submission).toFixed(2)
          );
          this.rte = parseFloat(
            ((response.data.rte * 100) / response.data.submission).toFixed(2)
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
      });

    this.$http
      .get("http://localhost:8000/problem/" + this.ID)
      .then(response => {
        this.des = response.data.des;
        this.input = response.data.input;
        this.output = response.data.output;
        this.sinput = response.data.sinput.split("|#)"); //分隔符
        this.soutput = response.data.soutput.split("|#)");
        this.author = response.data.author;
        this.addtime =
          response.data["addtime"].split("T")[0] +
          " " +
          response.data["addtime"].split("T")[1].split(".")[0];
        this.oj = response.data.oj;
        this.source = response.data.source;
        this.time = response.data.time + "MS";
        this.memory = response.data.memory + "MB";
        this.hint = response.data.hint;
      });
  },
  methods: {
    problemlevel: function(type) {
      if (type == "Easy") return "info";
      if (type == "Medium") return "success";
      if (type == "Hard") return "";
      if (type == "VeryHard") return "warning";
      if (type == "ExtremelyHard") return "danger";
    },
    submit:function(){

      this.$http.post('http://localhost:8000/judgestatus/',{
        'user':'admin',
        'oj':'LPOJ',
        "problem": this.ID,
        "result": -1,
        "time": 0,
        "memory": 0,
        "length": this.code.length,
        "language": this.language,
        "judger": "waiting for judger",
        "contest": 0,
        "code": this.code,
        "testcase": 0,
        "message": "0"
      }).then((response) =>{
          console.log(response)
      })
  }
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
