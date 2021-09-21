<template>
  <div class="examination">
    <el-row>
      <ul v-for="(item,i) in ChoiceProblemDatas" :key="i">
        <div>{{i+1}}、{{item.des}}</div>
        <br />
        <el-col>
          <el-row>
            <el-radio v-model="radio[i]" :label="item.choiceA" @change="getIputValue(i)"></el-radio>
          </el-row>
          <el-row>
            <el-radio v-model="radio[i]" :label="item.choiceB" @change="getIputValue(i)"></el-radio>
          </el-row>
          <el-row>
            <el-radio v-model="radio[i]" :label="item.choiceC" @change="getIputValue(i)"></el-radio>
          </el-row>
          <el-row>
            <el-radio v-model="radio[i]" :label="item.choiceD" @change="getIputValue(i)"></el-radio>
          </el-row>
        </el-col>
      </ul>
    </el-row>
    <el-row>
      <el-button type="primary" @click="Submit" v-show="havechopro == true">提交</el-button>
    </el-row>

    <div v-show="havechopro == true">已提交的答案</div>
    <el-input placeholder="已提交的答案" v-model="myanswer" :disabled="true" v-show="havechopro == true"></el-input>
  </div>
</template>

<script>
export default {
  name: "contestchoiceproblem",
  data() {
    return {
      form: {
        username: "",
        realname: "",
        number: "",
        contestid: "",
        answer: "",
        score: "0",
        answer_detail: ""
      },
      myanswer: "",
      havechopro: false,
      ProblenCount: "",
      allRadio: [],
      radio: [],
      ChoiceProblemIds: [],
      ChoiceProblemDatas: [],
      choice_problem_data: [],
      curtime: ""
    };
  },
  methods: {
    compare: function(pro) {
      return function(obj1, obj2) {
        var val1 = obj1[pro];
        var val2 = obj2[pro];
        if (val1 < val2) {
          //正序
          return 1;
        } else if (val1 > val2) {
          return -1;
        } else {
          return 0;
        }
      };
    },
    Submit() {
      if (!sessionStorage.username) {
        this.$message.error("请先登录");
        return;
      }
      let post_answer_detail = [];
      if (this.$store.state.contestisend == true) {
        this.$message.error("比赛已结束");
      } else {
        this.$axios
          .get("/user/?username=" + this.form.username)
          .then(response2 => {
            this.form.realname = response2.data[0].realname;
            this.form.number = response2.data[0].number;
            this.form.answer = "";
            this.$axios.get("/currenttime/").then(response4 => {
              this.curtime = response4.data;
              for (var i = 0; i < this.ChoiceProblemDatas.length; i++) {
                //包含了学生选的选项描述，选择题题目，选择题id，学生用户名，真实姓名，最后一次提交答案的时间
                post_answer_detail.push({
                  answer: this.allRadio[i],
                  des: this.radio[i],
                  pro: this.ChoiceProblemDatas[i].des,
                  pro_id: this.ChoiceProblemDatas[i].choice_problem_id,
                  user: sessionStorage.username,
                  real_name: this.form.realname,
                  student_number:this.form.number,
                  last_submit_time: response4.data
                });
                if (this.allRadio[i]) {
                  this.form.answer += this.allRadio[i];
                } else {
                  this.form.answer += "X";
                }
              }
              this.form.answer_detail = JSON.stringify(post_answer_detail);
              this.$axios
                .get(
                  "/conteststudentchoiceanswer/?username=" +
                    this.form.username +
                    "&contestid=" +
                    this.form.contestid
                )
                .then(response => {
                  if (response.data.length > 0) {
                    var updateId = response.data[0].id;
                    this.$axios
                      .put(
                        "/conteststudentchoiceanswer/" + updateId + "/",
                        this.form
                      )
                      .then(response3 => {
                        this.myanswer = this.form.answer;
                        this.$message({
                          message: "提交成功！",
                          type: "success"
                        });
                      })
                      .catch(error => {
                        this.$message.error(
                          "提交失败！请再提交一次" +
                            "(" +
                            JSON.stringify(error.response.data) +
                            ")"
                        );
                      });
                  } else {
                    this.$axios
                      .post("/conteststudentchoiceanswer/", this.form)
                      .then(response3 => {
                        this.myanswer = this.form.answer;
                        this.$message({
                          message: "提交成功！",
                          type: "success"
                        });
                      })
                      .catch(error => {
                        this.$message.error(
                          "提交失败！请再提交一次" +
                            "(" +
                            JSON.stringify(error.response.data) +
                            ")"
                        );
                      });
                  }
                });
            });
          });
      }
    },
    getIputValue(index) {
      var ChooseAnswer = this.radio[index].split(".");
      this.allRadio[index] = ChooseAnswer[0]; // 将数据存入提交给后台的数据中
    },
    GetItem: function(des, choiceA, choiceB, choiceC, choiceD, id) {
      return {
        des: des,
        choiceA: "A. " + choiceA,
        choiceB: "B. " + choiceB,
        choiceC: "C. " + choiceC,
        choiceD: "D. " + choiceD,
        choice_problem_id: id
      };
    }
  },
  created() {
    this.form.username = sessionStorage.username;
    this.form.contestid = this.$route.params.contestID;
    let contest_id = this.$route.params.contestID;
    let post_data = { ContestId: contest_id };
    this.$axios
      .post("/getcontestchoiceproblems", post_data)
      .then(response => {
        let choice_problem_data = response.data;
        this.ProblenCount = parseInt(response.length);
        this.ChoiceProblemDatas = [];
        for (let i = 0; i < choice_problem_data.length; i++) {
          {
            this.ChoiceProblemDatas.push(
              this.GetItem(
                choice_problem_data[i].des,
                choice_problem_data[i].A,
                choice_problem_data[i].B,
                choice_problem_data[i].C,
                choice_problem_data[i].D,
                choice_problem_data[i].cpro_id
              )
            );
          }
        }
        this.havechopro = true;
        this.myanswer = "";
        if (sessionStorage.username) {
          this.$axios
            .get(
              "/conteststudentchoiceanswer/?username=" +
                this.form.username +
                "&contestid=" +
                this.form.contestid
            )
            .then(response5 => {
              var lastanswer = null;
              if (response5.data[0].answer) {
                lastanswer = response5.data[0].answer;
                this.myanswer = response5.data[0].answer;
              } else {
                this.myanswer = "";
              }
              if (lastanswer != null) {
                for (let i = 0; i < this.ChoiceProblemDatas.length; i++) {
                  if (lastanswer[i] == "A") {
                    this.allRadio[i] = "A";
                    this.radio[i] = this.ChoiceProblemDatas[i].choiceA;
                  } else if (lastanswer[i] == "B") {
                    this.allRadio[i] = "B";
                    this.radio[i] = this.ChoiceProblemDatas[i].choiceB;
                  } else if (lastanswer[i] == "C") {
                    this.allRadio[i] = "C";
                    this.radio[i] = this.ChoiceProblemDatas[i].choiceC;
                  } else if (lastanswer[i] == "D") {
                    this.allRadio[i] = "D";
                    this.radio[i] = this.ChoiceProblemDatas[i].choiceD;
                  }
                }
              }
            });
        }
      })
      .catch(error => {
        this.$message.error(
          "获取选择题失败，可能是你没有登录，或者后台出错，请联系管理员查看后台输出日志以获取错误信息" +
            "(" +
            JSON.stringify(error.response.data) +
            ")"
        );
      });
  },
  mounted() {}
};
</script>

<style scoped>
</style>