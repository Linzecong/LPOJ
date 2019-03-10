<template>
  <el-tabs type="border-card" v-show="canshow">
    <el-tab-pane label="添加题目">

      <el-form ref="addproblemform" :model="addproblemform" label-position="right">
        <el-form-item label="题目编号：">
          <el-input v-model="addproblemform.problem" readonly="true"></el-input>
        </el-form-item>
        <el-form-item label="作者：">
          <el-input v-model="addproblemform.author"></el-input>
        </el-form-item>
        <el-form-item label="标题：">
          <el-input v-model="addproblemform.title"></el-input>
        </el-form-item>
        <el-form-item label="介绍：">
          <el-input type="textarea" v-model="addproblemform.des"></el-input>
        </el-form-item>
        <el-form-item label="输入：">
          <el-input type="textarea" v-model="addproblemform.input"></el-input>
        </el-form-item>
        <el-form-item label="输出：">
          <el-input type="textarea" v-model="addproblemform.output"></el-input>
        </el-form-item>
        <el-form-item label="样例输入（用 |#) 分割）：">
          <el-input type="textarea" v-model="addproblemform.sinput"></el-input>
        </el-form-item>
        <el-form-item label="样例输出（用 |#) 分割）：">
          <el-input  type="textarea" v-model="addproblemform.soutput"></el-input>
        </el-form-item>
        <el-form-item label="来源：">
          <el-input v-model="addproblemform.source"></el-input>
        </el-form-item>
        <el-form-item label="时间（ms）：">
          <el-input v-model.number="addproblemform.time"></el-input>
        </el-form-item>
        <el-form-item label="内存（MB）：">
          <el-input v-model.number="addproblemform.memory"></el-input>
        </el-form-item>
        <el-form-item label="提示：">
          <el-input type="textarea" v-model="addproblemform.hint"></el-input>
        </el-form-item>
        <el-form-item label="权限（1为公开，2为私密（比赛题目））：">
          <el-input v-model.number="addproblemform.auth"></el-input>
        </el-form-item>

        <el-form-item label="难度（1~5）：">
          <el-input v-model.number="addproblemform.level"></el-input>
        </el-form-item>
        <el-form-item label="标签（用|分割）：">
          <el-input v-model="addproblemform.tag"></el-input>
        </el-form-item>
        <el-form-item label="分数（建议100~1000）：">
          <el-input v-model.number="addproblemform.score"></el-input>
        </el-form-item>

        <el-upload
          class="upload-demo"
          ref="upload"
          :action="uploadaddress"

          :on-exceed="handleExceed"
          :on-change="handleChange"
          :on-success="handleSuccess"
          :on-error="handleError"
          :on-remove="handleRemove"

          :file-list="fileList"
          :multiple="false"
          :limit="1"
          :auto-upload="false">
          <el-button slot="trigger" size="small" type="primary">选取数据文件</el-button>
          <div slot="tip" class="el-upload__tip">只能上传zip文件，重命名为 题目编号.zip 如 1.zip，压缩包中输入输出名字要一样，且后缀为.in和.out</div>
        </el-upload>

        <el-form-item>
          <el-button type="primary" @click="onAddProblemSubmit">添加题目</el-button>
        </el-form-item>

      </el-form>


    </el-tab-pane>

    <el-tab-pane label="添加比赛" :lazy="true"></el-tab-pane>
    <el-tab-pane label="题目修改"></el-tab-pane>
    <el-tab-pane label="比赛设置"></el-tab-pane>
    <el-tab-pane label="管理用户" :disabled="!isadmin"></el-tab-pane>
  </el-tabs>
</template>

<script>
export default {
  name: "admin",
  data() {
    return {
      msg: "欢迎来到LPOJ",
      type: 1,
      isadmin: false,
      canshow: false,
      problemcount: 0,
      uploadaddress:"http://" + this.$ip + ":" + this.$port + "/uploadfile/",
      fileList: [],
      addproblemform:{
        problem:this.problemcount+1,
        author:sessionStorage.name,
        title:"题目标题",
        des:"题目说明",
        input:"输入说明",
        output:"输出说明",
        sinput:"1 1|#)2 2",
        soutput:"2|#)4",
        source:"LPOJ",
        time:1000,
        memory:64,
        hint:"提示",
        auth:2,
        tag:"简单题|模拟|贪心",
        level:3,
        score:100,
      },
      addproblemdataform:{
        problem:this.problemcount+1,
        title:"题目标题",
        tag:"简单题|模拟|贪心",
        level:3,
        score:100,
      }
    };
  },
  methods:{
      handleRemove(file, fileList){
        this.fileList=[]
      },
      handleExceed(file, fileList) {
        this.$message.error("只能上传一个文件！")
      },
      handleChange(file, fileList) {
        var name = file.name;
        var li=name.split(".");
        this.fileList=fileList
        if(li[0]!=this.addproblemform.problem){
          this.$message.error("数据文件名名不正确！应为"+this.addproblemform.problem+".zip");
          this.fileList=[]
        }
        
      },
      handleError(response, file, fileList) {
        this.$message.error("数据上传失败！"+response)
      },
      handleSuccess(response, file, fileList) {
        this.$axios
        .post("http://" + this.$ip + ":" + this.$port + "/problem/",this.addproblemform)
        .then(response => {
          this.addproblemdataform.problem=this.addproblemform.problem;
          this.addproblemdataform.title=this.addproblemform.title;
          this.addproblemdataform.level=this.addproblemform.level;
          this.addproblemdataform.tag=this.addproblemform.tag;
          this.addproblemdataform.score=this.addproblemform.score;

          this.$axios
        .post("http://" + this.$ip + ":" + this.$port + "/problemdata/",this.addproblemdataform)
        .then(response => {
            this.$message({
              message: "提交成功！题目编号为："+response.data.problem,
              type: "success"
            });


        });


        });
      },


    onAddProblemSubmit(){
      if(this.fileList.length<=0){
        this.$message.error("请选择数据文件")
        return;
      }
      this.$confirm("确定添加吗？", "添加题目", {
        confirmButtonText: "确定",
        cancelButtonText: "取消",
        type: "warning"
      }).then(() => {
        this.$refs.upload.submit();

      });

      

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

    this.$axios
      .get("http://" + this.$ip + ":" + this.$port + "/problemdata/?limit=1")
      .then(response => {
        this.problemcount = response.data.count;
        this.addproblemform.problem=this.problemcount+1;
        this.addproblemdataform.problem=this.problemcount+1;
      });


  }
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
h1 {
  position: relative;
}
</style>
