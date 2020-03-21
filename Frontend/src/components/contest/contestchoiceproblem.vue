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
        score: "0"
      },
      myanswer: "",
      havechopro: false,
      ProblenCount: "",
      allRadio: [],
      radio: [],
      ChoiceProblemIds: [],
      ChoiceProblemDatas: []
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
      console.log(this.radio);
      if (this.$store.state.contestisend == true) {
        this.$message.error("比赛已结束");
      } else {
        this.form.answer = "";
        for (var i = 0; i < this.ProblenCount; i++) {
          if (this.allRadio[i]) {
            this.form.answer += this.allRadio[i];
          } else {
            this.form.answer += "X";
          }
        }
        this.$axios
          .get("/user/?username=" + this.form.username)
          .then(response2 => {
            this.form.realname = response2.data[0].realname;
            this.form.number = response2.data[0].number;
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
                this.$axios
                  .get(
                    "/conteststudentchoiceanswer/?username=" +
                      this.form.username +
                      "&contestid=" +
                      this.form.contestid
                  )
                  .then(response => {
                    this.myanswer = response.data[0].answer;
                  });
              });
          });
      }
    },
    getIputValue(index) {
      var ChooseAnswer = this.radio[index].split(".");
      this.allRadio[index] = ChooseAnswer[0]; // 将数据存入提交给后台的数据中
    },
    GetItem: function(des, choiceA, choiceB, choiceC, choiceD, rank) {
      return {
        des: des,
        choiceA: "A. " + choiceA,
        choiceB: "B. " + choiceB,
        choiceC: "C. " + choiceC,
        choiceD: "D. " + choiceD,
        rank: rank
      };
    },
    GetItem2: function(ChoiceProblemDatas) {
      return ChoiceProblemDatas;
    },
    reflash(id) {
      this.form.username = sessionStorage.username;
      this.form.contestid = this.$route.params.contestID;
      this.$axios
        .get("/contestchoiceproblem/?ContestId=" + this.$route.params.contestID)
        .then(async response => {
          this.ProblenCount = response.data.length;
          if (response.data.length > 0) this.havechopro = true;
          for (var i = 0; i < response.data.length; i++) {
            this.ChoiceProblemIds.push(response.data[i].ChoiceProblemId);
          }
          this.ChoiceProblemIds.sort(this.compare("rank"));
          this.ChoiceProblemDatas = [];
          for (var i = 0; i < response.data.length; i++) {
            var response2 = await this.$axios.get(
              "/choiceproblem/?ChoiceProblemId=" +
                response.data[i].ChoiceProblemId
            );

            this.ChoiceProblemDatas.push(
              this.GetItem(
                response2.data[0].des,
                response2.data[0].choiceA,
                response2.data[0].choiceB,
                response2.data[0].choiceC,
                response2.data[0].choiceD,
                response2.data[0].rank
              )
            );
          }

          this.$axios
            .get(
              "/conteststudentchoiceanswer/?username=" +
                this.form.username +
                "&contestid=" +
                this.form.contestid
            )
            .then(response => {
              this.myanswer = response.data[0].answer;

              var proCount = this.ProblenCount;
              if (proCount > 0) {
                var lastanswer = response.data[0].answer;
              }
              for (var i = 0; i < proCount; i++) {
                if (lastanswer[i] == "A") {
                  this.allRadio[i] = "A";
                  var tmp = this.ChoiceProblemDatas[i];
                  this.radio[i] = this.GetItem2(tmp.choiceA);
                } else if (lastanswer[i] == "B") {
                  this.allRadio[i] = "B";
                  var tmp = this.ChoiceProblemDatas[i];
                  this.radio[i] = this.GetItem2(tmp.choiceB);
                } else if (lastanswer[i] == "C") {
                  this.allRadio[i] = "C";
                  var tmp = this.ChoiceProblemDatas[i];
                  this.radio[i] = this.GetItem2(tmp.choiceC);
                } else if (lastanswer[i] == "D") {
                  this.allRadio[i] = "D";
                  var tmp = this.ChoiceProblemDatas[i];
                  this.radio[i] = this.GetItem2(tmp.choiceD);
                }
              }
            });
        });
    }
  },

  created() {
    // this.reflash()
  }
};
</script>

<style scoped>
</style>