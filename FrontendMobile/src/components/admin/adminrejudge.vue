<template>
  <el-row>
    <el-row>
      <el-form label-position="right">
        <el-form-item label="比赛题目重测：">
          <el-input v-model="contestid" placeholder="请输入比赛编号" style="width:200px"></el-input>
          <el-input v-model="contestproblem" placeholder="请输入比赛题目编号的数字，A=0,B=1" style="width:400px"></el-input>
          <el-button type="primary" @click="contestrejudge">提交</el-button>
        </el-form-item>
        <el-form-item label="题目重测：">
          <el-input v-model="problem" placeholder="请输入题目编号" style="width:200px"></el-input>
          <el-button type="primary" @click="problemrejudge">提交</el-button>
        </el-form-item>
        <el-form-item label="根据ID重测：">
          <el-input v-model="statusid" placeholder="请输入提交编号" style="width:200px"></el-input>
          <el-button type="primary" @click="statusrejudge">提交</el-button>
        </el-form-item>
        <el-form-item label="根据类型重测：">
          <el-select v-model="resulttype" placeholder="请选择类型">
            <el-option key="2" label="Waiting" value="-6"></el-option>
            <el-option key="3" label="Presentation Error" value="-5"></el-option>
            <el-option key="4" label="Compile Error" value="-4"></el-option>
            <el-option key="6" label="Judging" value="-2"></el-option>
            <el-option key="11" label="System Error" value="5"></el-option>
          </el-select>
          <el-button type="primary" @click="typerejudge">提交</el-button>
        </el-form-item>
      </el-form>
    </el-row>
  </el-row>
</template>

<script>
import moment from "moment";
export default {
  name: "adminrejudge",
  data() {
    return {
      contestid: "",
      contestproblem: "",
      problem: "",
      statusid: "",
      resulttype: ""
    };
  },
  methods: {
    contestrejudge() {
      this.$axios
        .post("/rejudge/", {
          contestid: this.contestid,
          problem: this.contestproblem
        })
        .then(response => {
          this.$message.success("提交成功！" + response);
        })
        .catch(error => {
          this.$message.error(
            "服务器错误！" + JSON.stringify(error.response.data)
          );
        });
    },
    problemrejudge() {
      this.$axios
        .post("/rejudge/", {
          problem: this.problem
        })
        .then(response => {
          this.$message.success("提交成功！" + response);
        })
        .catch(error => {
          this.$message.error(
            "服务器错误！" + JSON.stringify(error.response.data)
          );
        });
    },
    statusrejudge() {
      this.$axios
        .post("/rejudge/", {
          statusid: this.statusid
        })
        .then(response => {
          this.$message.success("提交成功！" + response);
        })
        .catch(error => {
          this.$message.error(
            "服务器错误！" + JSON.stringify(error.response.data)
          );
        });
    },
    typerejudge() {
      this.$axios
        .post("/rejudge/", {
          statustype: this.resulttype
        })
        .then(response => {
          this.$message.success("提交成功！" + response.data);
        })
        .catch(error => {
          this.$message.error(
            "服务器错误！" + JSON.stringify(error.response.data)
          );
        });
    }
  },
  created() {}
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.el-tag + .el-tag {
  margin-left: 10px;
}
</style>
