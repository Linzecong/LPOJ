<template>
  <el-form :model="choiceproblemform"
           label-position="right"
           v-loading="loading">

    <el-form-item label="选择题题目编号：">
      <el-input v-model="choiceproblemform.ChoiceProblemId"
                style="width:400px;"
                readonly></el-input>
    </el-form-item>

    <el-form-item label="选择题题目：">
      <el-input type="textarea"
                v-model="choiceproblemform.des"
                autosize
                style="width:800px;"></el-input>
    </el-form-item>

    <el-form-item label="选项A：">
      <el-input type="textarea"
                v-model="choiceproblemform.choiceA"
                autosize
                style="width:800px;"></el-input>
    </el-form-item>

    <el-form-item label="选项B：">
      <el-input type="textarea"
                v-model="choiceproblemform.choiceB"
                autosize
                style="width:800px;"></el-input>
    </el-form-item>

    <el-form-item label="选项C：">
      <el-input type="textarea"
                v-model="choiceproblemform.choiceC"
                autosize
                style="width:800px;"></el-input>
    </el-form-item>

    <el-form-item label="选项D：">
      <el-input type="textarea"
                v-model="choiceproblemform.choiceD"
                autosize
                style="width:800px;"></el-input>
    </el-form-item>

    <el-button type="success"
               @click="AddChoiceProblemSubmit"
               style="float:left;">添加题目</el-button>
  </el-form>
</template>
<script>
export default {
  name: "adminaddchoiceproblem",
  data () {
    return {
      choiceproblemform: {
        ChoiceProblemId: "",
        des: "",
        choiceA: "",
        choiceB: "",
        choiceC: "",
        choiceD: "",

      }
    }
  },
  methods: {
    AddChoiceProblemSubmit () {
      console.log(this.choiceproblemform);
      this.$axios.post("/choiceproblem/", this.choiceproblemform)
        .then(Response => {
          this.$message({
            message: "提交成功！选择题题目编号为：" + this.choiceproblemform.ChoiceProblemId,
            type: "success"
          });
        })
    }
  },
  created () {
    this.$axios.get("/choiceproblem/")
      .then(Response => {
        this.choiceproblemform.ChoiceProblemId = Response.data.length + 1;

      })
  },

}
</script>
<style scoped>
</style>
