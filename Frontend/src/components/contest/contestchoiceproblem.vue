<template>
  <div class="examination">
    <el-row>
      <ul v-for="(item,i) in ChoiceProblemDatas"
          :key="i">
        <div>{{i+1}}、{{item.des}}</div>
        <br>
        <el-col>
          <el-row>
            <el-radio v-model="radio[i]"
                      :label="item.choiceA"
                      @change="getIputValue(i)"></el-radio>
          </el-row>
          <el-row>
            <el-radio v-model="radio[i]"
                      :label="item.choiceB"
                      @change="getIputValue(i)"></el-radio>
          </el-row>
          <el-row>
            <el-radio v-model="radio[i]"
                      :label="item.choiceC"
                      @change="getIputValue(i)"></el-radio>
          </el-row>
          <el-row>
            <el-radio v-model="radio[i]"
                      :label="item.choiceD"
                      @change="getIputValue(i)"></el-radio>
          </el-row>
        </el-col>
      </ul>
    </el-row>
    <el-row>
      <el-button type="primary"
                 @click="Submit">提交</el-button>
    </el-row>
  </div>
</template>

<script>
export default {
  name: "contestchoiceproblem",
  data () {
    return {
      form: {
        username: "",
        realname: "",
        number: "",
        contestid: "",
        answer: "",
        score: "0",
      },


      ProblenCount: "",
      allRadio: [],
      radio: [],
      ChoiceProblemIds: [],
      ChoiceProblemDatas: [],
    }
  },
  methods: {
    compare: function (pro) {
      return function (obj1, obj2) {
        var val1 = obj1[pro];
        var val2 = obj2[pro];
        if (val1 < val2) { //正序
          return 1;
        } else if (val1 > val2) {
          return -1;
        } else {
          return 0;
        }
      }
    },
    Submit () {
      if (this.$store.state.contestisend == true) {
        this.$message.error("比赛已结束");
      }
      else {
        this.$confirm("确定提交答案吗？只能提交一次！",
          {
            confirmButtonText: "确定",
            cancelButtonText: "取消",
            type: "warning"
          }).then(() => {

            this.$axios.get(
              "/conteststudentchoiceanswer/?username=" +
              this.form.username +
              "&contestid=" +
              this.form.contestid
            )
              .then(
                response => {
                  if (response.data[0]) {
                    this.$message.error("你已经提交过答案");
                  }
                  else {
                    this.form.answer = "";
                    for (var i = 0; i < this.ProblenCount; i++) {
                      if (this.allRadio[i]) {
                        this.form.answer += this.allRadio[i];
                      }
                      else {
                        this.form.answer += "X";
                      }
                    }
                    this.$axios.get("/user/?username=" + this.form.username)
                      .then(response2 => {
                        this.form.realname = response2.data[0].realname;
                        this.form.number = response2.data[0].number;
                        this.$axios.post("/conteststudentchoiceanswer/", this.form)
                          .then(
                            response3 => {
                              this.$message({
                                message: "提交成功！",
                                type: "success"
                              });
                            }
                          ).catch(error => {
                            this.$message.error(
                              "提交失败！请再提交一次" + "(" + JSON.stringify(error.response.data) + ")"
                            );
                          });
                      }
                      )


                  }
                })
          })
      };

    },
    getIputValue (index) {
      var ChooseAnswer = this.radio[index].split(".");
      this.allRadio[index] = ChooseAnswer[0]; // 将数据存入提交给后台的数据中
      console.log(this.allRadio);
    },
    GetItem: function (des, choiceA, choiceB, choiceC, choiceD, rank) {
      return {
        "des": des,
        "choiceA": "A. " + choiceA,
        "choiceB": "B. " + choiceB,
        "choiceC": "C. " + choiceC,
        "choiceD": "D. " + choiceD,
        "rank": rank,
      }
    }
  },
  created () {

    this.form.username = sessionStorage.username;
    this.form.contestid = this.$route.params.contestID;
    this.$axios.get("/contestchoiceproblem/?ContestId=" + this.$route.params.contestID)
      .then(response => {
        this.ProblenCount = response.data.length;
        for (var i = 0; i < response.data.length; i++) {
          this.ChoiceProblemIds.push(response.data[i].ChoiceProblemId);
        }

        this.ChoiceProblemIds.sort(this.compare("rank"));

        for (var i = 0; i < response.data.length; i++) {
          this.$axios.get(
            "/choiceproblem/?ChoiceProblemId="
            + response.data[i].ChoiceProblemId
          )
            .then(response2 => {
              this.ChoiceProblemDatas.push(
                this.GetItem(
                  response2.data[0].des,
                  response2.data[0].choiceA,
                  response2.data[0].choiceB,
                  response2.data[0].choiceC,
                  response2.data[0].choiceD,
                  response2.data[0].rank,
                ));
            })
        }

      })
  }
}
</script>

<style scoped>
</style>
