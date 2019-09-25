<template>
  <el-form ref="addproblemform" :model="addproblemform" label-position="right" v-loading="loading">
    <el-form-item label="题目编号：">
      <el-input v-model="addproblemform.problem" style="width:400px;" readonly></el-input>
    </el-form-item>
    <el-form-item label="特殊选项：添加其他OJ题目用！不知道的话请忽略">
      <el-input v-model="addproblemform.oj" placeholder="OJ" style="width:100px;"></el-input>
      <el-input
        v-model="addproblemform.source"
        placeholder="Pro ID"
        style="width:100px;margin-left:40px;"
      ></el-input>
    </el-form-item>
    <el-form-item label="作者：">
      <el-input v-model="addproblemform.author" style="width:400px;"></el-input>
    </el-form-item>
    <el-form-item label="标题：">
      <el-input v-model="addproblemform.title" style="width:400px;"></el-input>
    </el-form-item>
    <el-form-item label="介绍：">
      <el-input type="textarea" v-model="addproblemform.des" autosize style="width:800px;"></el-input>
    </el-form-item>
    <el-form-item label="输入：">
      <el-input type="textarea" v-model="addproblemform.input" autosize style="width:800px;"></el-input>
    </el-form-item>
    <el-form-item label="输出：">
      <el-input type="textarea" v-model="addproblemform.output" autosize style="width:800px;"></el-input>
    </el-form-item>
    <el-form-item label="样例输入（多个样例间用 |#) 分割）：">
      <el-input type="textarea" v-model="addproblemform.sinput" autosize style="width:800px;"></el-input>
    </el-form-item>
    <el-form-item label="样例输出（多个样例间用 |#) 分割）：">
      <el-input type="textarea" v-model="addproblemform.soutput" autosize style="width:800px;"></el-input>
    </el-form-item>
    <el-form-item label="提示：">
      <el-input type="textarea" v-model="addproblemform.hint" autosize style="width:800px;"></el-input>
    </el-form-item>
    <el-form-item label="来源：">
      <el-input v-model="addproblemform.source" style="width:400px;"></el-input>
    </el-form-item>
    <el-form-item label="时间（ms）：">
      <el-input-number style="width:200px;" v-model="addproblemform.time" :step="1000" :min="100" :max="60000"></el-input-number>      
    </el-form-item>
    <el-form-item label="内存（MB）：">
      <el-input-number style="width:200px;" v-model="addproblemform.memory" :step="64" :min="4" :max="1024"></el-input-number>
    </el-form-item>
    <el-form-item label="权限：">
      <el-select v-model="addproblemform.auth" placeholder="请选择" style="width:200px;">
        <el-option key="1" label="公开" :value="1"></el-option>
        <el-option key="2" label="私密" :value="2"></el-option>
        <el-option key="3" label="比赛中" :value="3"></el-option>
      </el-select>
    </el-form-item>

    <el-form-item label="难度：">
      <el-select v-model="addproblemform.level" placeholder="请选择" style="width:200px;">
        <el-option key="1" label="简单" :value="1"></el-option>
        <el-option key="2" label="普通" :value="2"></el-option>
        <el-option key="3" label="中等" :value="3"></el-option>
        <el-option key="4" label="困难" :value="4"></el-option>
        <el-option key="5" label="极其困难" :value="5"></el-option>
      </el-select>
    </el-form-item>
    <el-form-item label="标签（用|分割）：">
      <el-input v-model="addproblemform.tag" style="width:400px;"></el-input>
    </el-form-item>
    <el-form-item label="分数（建议100~10000）：">
        <el-input-number style="width:200px;" v-model="addproblemform.score" :step="100" :min="100" :max="10000"></el-input-number>
    </el-form-item>

    <el-upload
      style="width:400px;"
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
      <div slot="tip" class="el-upload__tip">只能上传zip文件,压缩包内的不要有文件夹，输入输出文件后缀为.in和.out.添加一个casedes.txt文件可以对每一个样例进行说明，每行一个说明，中间不要有多余的空行，对应的case用|隔开，如：  data1|xxxxxx  </div>
    </el-upload>

    <el-button type="success" @click="onAddProblemSubmit" style="float:right;">添加题目</el-button>
  </el-form>
</template>

<script>
export default {
  name: "admin",
  data() {
    return {
      problemcount: 0,
      uploadaddress: "/uploadfile/",
      fileList: [],
      loading: false,
      addproblemform: {
        problem: this.problemcount + 1,
        author: sessionStorage.name,
        title: "题目标题",
        des: "题目说明\n支持HTML格式和Katex公式\n\n",
        input: "输入说明\n支持HTML格式和Katex公式\n\n",
        output: "输出说明\n支持HTML格式和Katex公式\n\n",
        sinput: "1 1|#)2 2",
        soutput: "2|#)4",
        source: "LPOJ",
        time: 1000,
        memory: 64,
        hint: "提示\n支持HTML格式和Katex公式\n\n",
        auth: 2,
        tag: "简单题|模拟",
        level: 3,
        score: 100,
        oj: "LPOJ"
      },
      addproblemdataform: {
        problem: this.problemcount + 1,
        title: "题目标题",
        tag: "简单题|模拟|贪心",
        level: 3,
        score: 100,
        auth: 2,
        oj: ""
      }
    };
  },
  methods: {
    myupload(f) {
      this.$message.success("提交中！请等待自动刷新！");
      let param = new FormData(); //创建form对象

      var newfile = new File([f.file], this.addproblemform.problem + ".zip");

      param.append("file", newfile); //通过append向form对象添加数据
      let config = {
        headers: { "Content-Type": "multipart/form-data" }
      }; //添加请求头
      this.$axios
        .post(f.action, param, config) //上传图片
        .then(response => {
          console.log(response.data);
          f.onSuccess(response.data);
        })
        .catch(err => {
          console.log(err);
          f.onError(err);
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
      if (li[1] != "zip") {
        this.$message.error("数据文件名名不正确！后缀应为zip");
        this.fileList = [];
      }
    },
    handleError(response, file, fileList) {
      this.$message.error("数据上传失败！" + response);
    },
    handleSuccess(response, file, fileList) {
      this.$axios.post("/problem/", this.addproblemform).then(response => {
        this.addproblemdataform.problem = this.addproblemform.problem;
        this.addproblemdataform.title = this.addproblemform.title;
        this.addproblemdataform.level = this.addproblemform.level;
        this.addproblemdataform.tag = this.addproblemform.tag;
        this.addproblemdataform.score = this.addproblemform.score;
        this.addproblemdataform.auth = this.addproblemform.auth;
        this.addproblemdataform.oj = this.addproblemform.oj;

        var tag = this.addproblemdataform.tag.split("|");
        for (var i = 0; i < tag.length; i++) {
          this.$axios
            .post("/problemtag/", {
              tagname: tag[i],
              count: 1
            })
            .catch(error => {});
        }

        this.$axios
          .post("/problemdata/", this.addproblemdataform)
          .then(response2 => {
            this.$message({
              message: "提交成功！题目编号为：" + response2.data.problem,
              type: "success"
            });
            this.loading = false;
            this.$router.go(0);
          });
      });
    },

    onAddProblemSubmit() {
      if (this.fileList.length <= 0) {
        this.$confirm(
          "确定添加吗？本次添加没有添加数据文件！后续可在修改题目中添加",
          "添加题目",
          {
            confirmButtonText: "确定",
            cancelButtonText: "取消",
            type: "warning"
          }
        ).then(() => {
          this.handleSuccess(1, 2, 3);
        });
        return;
      }
      console.log(this.fileList);
      var name = this.fileList[0].name;
      var li = name.split(".");
      if (li[1] != "zip") {
        this.$message.error("数据文件名名不正确！后缀应为zip");
        this.fileList = [];
      }
      this.$confirm("确定添加吗？", "添加题目", {
        confirmButtonText: "确定",
        cancelButtonText: "取消",
        type: "warning"
      }).then(() => {
        this.loading = true;
        this.$refs.upload.submit();
      });
    }
  },
  created() {
    this.$axios
      .get("/problemdata/?limit=1")
      .then(response => {
        this.problemcount = response.data.count;
        this.addproblemform.problem = this.problemcount + 1;
        this.addproblemdataform.problem = this.problemcount + 1;
      })
      .catch(error => {
        this.$message.error(
          "服务器出错！" + JSON.stringify(error.response.data)
        );
      });
  }
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>
