<template>
  <el-tabs type="border-card" v-show="canshow">
    <el-row>
      <el-row>
        <el-input placeholder="请输入一道题的分值（一题多少分）" v-model="singalscore" clearable></el-input>

        <el-col>
          <el-input placeholder="请输入正确答案(不区分大小写)" v-model="standardanswer" clearable></el-input>
        </el-col>
      </el-row>
      <el-row>
        <el-button type="success" :disabled="!isadmin" @click="Score">评阅</el-button>
      </el-row>

      <el-row>
        <el-table :data="tableData" id="out-table" style="width: 100%">
          <el-table-column prop="username" label="用户名" width="180"></el-table-column>
          <el-table-column prop="realname" label="真实姓名" width="180"></el-table-column>
          <el-table-column prop="number" label="学号" width="180"></el-table-column>
          <el-table-column prop="answer" label="学生答案" width="400"></el-table-column>
          <el-table-column prop="score" label="分数" width="180"></el-table-column>
        </el-table>
      </el-row>

      <el-row></el-row>
      <el-button type="success" :disabled="!isadmin" @click="SubmitScore">提交评阅</el-button>
      <el-button type="primary" :disabled="!isadmin" @click="exportExcel">导出表格</el-button>
      <el-alert title="数据库中保存有学生答题的详细信息，包含了学生选的选项描述，选择题题目，选择题id，学生用户名，真实姓名，最后一次提交答案的时间" type="info"></el-alert>
    </el-row>
  </el-tabs>
</template>
<script>
import FileSaver from "file-saver";
import XLSX from "xlsx";
export default {
  name: "givechoiceproblemscore",
  data() {
    return {
      singalscore: "",
      studentcount: "",
      type: 1,
      isadmin: false,
      canshow: false,
      standardanswer: "",
      tableData: [],
      contestid: "",

      scoreform: {
        ContestId: "",
        ChoiceProblemAnswer: "",
        one_pro_score: ""
      }
    };
  },
  methods: {
    exportExcel() {
      /* 从表生成工作簿对象 */
      var wb = XLSX.utils.table_to_book(document.querySelector("#out-table"));
      /* 获取二进制字符串作为输出 */
      var wbout = XLSX.write(wb, {
        bookType: "xlsx",
        bookSST: true,
        type: "array"
      });
      try {
        FileSaver.saveAs(
          //Blob 对象表示一个不可变、原始数据的类文件对象。
          //Blob 表示的不一定是JavaScript原生格式的数据。
          //File 接口基于Blob，继承了 blob 的功能并将其扩展使其支持用户系统上的文件。
          //返回一个新创建的 Blob 对象，其内容由参数中给定的数组串联组成。
          new Blob([wbout], { type: "application/octet-stream" }),
          //设置导出文件名称
          "ChoiceProblemScores.xlsx"
        );
      } catch (e) {
        if (typeof console !== "undefined") this.$message.error(e);
      }
      return wbout;
    },
    SubmitScore() {
      this.$confirm("确定提交评阅分数吗？数据库中学生分数将在后台完成更新。", {
        confirmButtonText: "确定",
        cancelButtonText: "取消",
        type: "warning"
      }).then(() => {
        this.scoreform.ContestId = this.$route.query.contestid;
        this.scoreform.ChoiceProblemAnswer = this.standardanswer;
        this.scoreform.one_pro_score = this.singalscore;
        this.$axios
          .post("/scorecontestchoiceproblems", this.scoreform)
          .then(response3 => {
            this.$message({
              message: response3.data,
              type: "success"
            });
          })
          .catch(error => {
            this.$message.error(
              "提交评阅失败！请再提交一次。可能是你没有登录，或者后台出错，请联系管理员查看后台输出日志以获取错误信息" +
                "(" +
                JSON.stringify(error.response.data) +
                ")"
            );
          });
      });
    },
    Score() {
      var Answer = this.standardanswer.toUpperCase();
      for (var i = 0; i < this.studentcount; i++) {
        var stuAnswer = this.tableData[i].answer;
        var Score = Number(0);
        for (var ii = 0; ii < Answer.length; ii++) {
          if (stuAnswer[ii] === Answer[ii]) Score += Number(this.singalscore);
        }
        this.tableData[i].score = Number(Score);
      }
    }
  },
  created() {
    this.type = sessionStorage.type;
    if (this.type != 2 && this.type != 3) {
      this.$message.error("非法访问！");
      this.canshow = false;
      return;
    }
    this.canshow = true;
    if (this.type == 3) {
      this.isadmin = true;
    }
    this.contestid = this.$route.query.contestid;
    this.$axios
      .get("/conteststudentchoiceanswer/?contestid=" + this.contestid)
      .then(response => {
        this.tableData = response.data;
        this.studentcount = response.data.length;
      });
  }
};
</script>
<style scoped>
</style>
