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
      AnswerMerge: "",
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
      this.AnswerMerge = "";
      for (var i = 0; i < this.ProblenCount; i++) {
        if (this.allRadio[i]) {
          this.AnswerMerge += this.allRadio[i];
        }
        else {
          this.AnswerMerge += "X";
        }
      }

      console.log(this.AnswerMerge);
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
    this.$axios.get("/contestchoiceproblem/?ContestId=" + this.$route.params.contestID)
      .then(response => {
        this.ProblenCount = response.data.length;
        console.log(this.ProblenCount);
        // for (var ii = 0; ii < response.data.length; ii++) {
        //   this.AnswerMerge += "X";
        // }
        for (var i = 0; i < response.data.length; i++) {
          this.ChoiceProblemIds.push(response.data[i].ChoiceProblemId);
        }

        this.ChoiceProblemIds.sort(this.compare("rank"));
        console.log(this.ChoiceProblemIds);

        for (var i = 0; i < response.data.length; i++) {
          this.$axios.get(
            "/choiceproblem/?ChoiceProblemId="
            + response.data[i].ChoiceProblemId
          )
            .then(response2 => {
              console.log(response2.data[0]);
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

        console.log(this.ChoiceProblemDatas);

      })
  }
}
</script>

<style scoped>
</style>
