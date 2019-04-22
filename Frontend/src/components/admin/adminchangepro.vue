<template>
  <el-form ref="problemform" :model="problemform" label-position="right" v-loading="loading">
    <el-form-item label="题目编号：">
      <el-input v-model="problemform.problem" @change="problemchange" placeholder="请输入题目编号"></el-input>
      <el-button type="danger" @click="onDelProblem">删除题目</el-button>
    </el-form-item>

    <el-form-item label="作者：">
      <el-input v-model="problemform.author"></el-input>
    </el-form-item>
    <el-form-item label="标题：">
      <el-input v-model="problemform.title"></el-input>
    </el-form-item>
    <el-form-item label="介绍：">
      <el-input type="textarea" v-model="problemform.des" autosize></el-input>
    </el-form-item>
    <el-form-item label="输入：">
      <el-input type="textarea" v-model="problemform.input" autosize></el-input>
    </el-form-item>
    <el-form-item label="输出：">
      <el-input type="textarea" v-model="problemform.output" autosize></el-input>
    </el-form-item>
    <el-form-item label="样例输入（用 |#) 分割）：">
      <el-input type="textarea" v-model="problemform.sinput" autosize></el-input>
    </el-form-item>
    <el-form-item label="样例输出（用 |#) 分割）：">
      <el-input type="textarea" v-model="problemform.soutput" autosize></el-input>
    </el-form-item>
    <el-form-item label="来源：">
      <el-input v-model="problemform.source"></el-input>
    </el-form-item>
    <el-form-item label="时间（ms）：">
      <el-input v-model.number="problemform.time"></el-input>
    </el-form-item>
    <el-form-item label="内存（MB）：">
      <el-input v-model.number="problemform.memory"></el-input>
    </el-form-item>
    <el-form-item label="提示：">
      <el-input type="textarea" v-model="problemform.hint" autosize></el-input>
    </el-form-item>
    <el-form-item label="权限（1为公开，2为私密（比赛题目或禁用题目））：">
      <el-input v-model.number="problemform.auth"></el-input>
    </el-form-item>

    <el-form-item label="难度（1~5）：">
      <el-input v-model.number="problemform.level"></el-input>
    </el-form-item>
    <el-form-item label="标签（用|分割）：">
      <el-input v-model="problemform.tag"></el-input>
    </el-form-item>
    <el-form-item label="分数（建议100~1000）：">
      <el-input v-model.number="problemform.score"></el-input>
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
      :auto-upload="false"
      :http-request="myupload"
    >
      <el-button slot="trigger" size="small" type="primary">选取数据文件</el-button>
      <div
        slot="tip"
        class="el-upload__tip"
      >只能上传zip文件，重命名为 题目编号.zip 如 1.zip，压缩包中输入输出名字要一样，且后缀为.in和.out</div>
    </el-upload>

    <el-form-item>
      <el-button type="primary" @click="onAddProblemSubmit">修改题目</el-button>
    </el-form-item>
  </el-form>
</template>

<script>
export default {
  name: "adminchangepro",
  data() {
    return {
      problemcount: 0,
      uploadaddress: "/uploadfile/",
      fileList: [],
      loading:false,
      problemform: {
        problem: "",
        author: localStorage.name,
        title: "题目标题",
        des: "题目说明",
        input: "输入说明",
        output: "输出说明",
        sinput: "1 1|#)2 2",
        soutput: "2|#)4",
        source: "LPOJ",
        time: 1000,
        memory: 64,
        hint: "提示",
        auth: 2,
        tag: "简单题|模拟|贪心",
        level: 3,
        score: 100
      },
      problemdataform: {
        problem: this.problemcount + 1,
        title: "题目标题",
        tag: "简单题|模拟|贪心",
        level: 3,
        score: 100
      }
    };
  },
  methods: {
     myupload(f){

      let param = new FormData(); //创建form对象
         param.append('file',f.file);//通过append向form对象添加数据
         let config = {
           headers:{'Content-Type':'multipart/form-data'}
         };  //添加请求头
         this.$axios.post(f.action,param,config)//上传图片
         .then(response=>{
           console.log(response.data)
           f.onSuccess(response.data)
         })
         .catch(err => {
           console.log(err)
           f.onError(err)
         })   

    },
    onDelProblem(){
      this.$message.error("请把权限设置为2（私密）即可！");
    },
    problemchange(num) {
      this.$axios
        .get(
          "/problem/" +
            this.problemform.problem +
            "/"
        )
        .then(response => {
          this.$axios
            .get(
              "/problemdata/" +
                this.problemform.problem +
                "/"
            )
            .then(response2 => {
              response.data.level = response2.data.level;
              response.data.tag = response2.data.tag;
              response.data.score = response2.data.score;
              this.problemform = response.data;
            }).catch(error=>{
              this.$message.error("服务器错误！"+JSON.stringify(error.response.data));
              this.problemform={}
        });
        }).catch(error=>{
              this.$message.error("服务器错误！"+JSON.stringify(error.response.data));
              this.problemform={}
        });
    },
    handleRemove(file, fileList) {
      this.fileList = [];
    },
    handleExceed(file, fileList) {
      this.$message.error("只能上传一个文件！");
    },
    handleChange(file, fileList) {
      var name = file.name;
      var li = name.split(".");
      this.fileList = fileList;
      if (li[0] != this.problemform.problem) {
        this.$message.error(
          "数据文件名名不正确！应为" + this.problemform.problem + ".zip"
        );
        this.fileList = [];
      }
    },
    handleError(response, file, fileList) {
      this.$message.error("数据上传失败！" + response);
    },
    handleSuccess(response, file, fileList) {
      this.$axios
        .put(
          "/problem/" +
            this.problemform.problem +
            "/",
          this.problemform
        )
        .then(response => {
          this.problemdataform.problem = this.problemform.problem;
          this.problemdataform.title = this.problemform.title;
          this.problemdataform.level = this.problemform.level;
          this.problemdataform.tag = this.problemform.tag;
          this.problemdataform.score = this.problemform.score;
          this.problemdataform.auth = this.problemform.auth;
           var tag = this.problemdataform.tag.split("|")
          for(var i=0;i<tag.length;i++){
            this.$axios
            .post(
              "/problemtag/",
              {
                tagname:tag[i],
                count:1,
              }
            ).catch(error=>{});
          }
          this.$axios
            .put(
              "/problemdata/" +
                this.problemform.problem +
                "/",
              this.problemdataform
            )
            .then(response2 => {
              this.$message({
                message: "修改成功！修改题目编号为：" + response2.data.problem,
                type: "success"
              });
              this.fileList=[]
              this.loading=false
            });
        });
    },

    onAddProblemSubmit() {
      if (this.fileList.length <= 0) {
        this.$confirm("确定修改吗？本次修改没有更新数据", "修改题目：" + this.problemform.problem, {
        confirmButtonText: "确定",
        cancelButtonText: "取消",
        type: "warning"
      }).then(() => {
        this.handleSuccess(1,2,3);
      });
        
        return;
      }
      this.$confirm("确定修改吗？本次修改将会用新数据覆盖旧数据", "修改题目：" + this.problemform.problem, {
        confirmButtonText: "确定",
        cancelButtonText: "取消",
        type: "warning"
      }).then(() => {
        this.loading=true
        this.$refs.upload.submit();
      });
    }
  },
  created() {}
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
h1 {
  position: relative;
}
</style>
