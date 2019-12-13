<template>
  <el-card shadow="always" id="card">
    <el-form :model="form">
      <el-row :gutter="10">
        <el-col :span="3">
          <div style="text-align:center;margin:5px;">昵称</div>
        </el-col>
        <el-col :span="12">
          <el-input v-model="form.name" autocomplete="off"></el-input>
        </el-col>
      </el-row>
      <el-row :gutter="10">
        <el-col :span="3">
          <div style="text-align:center;margin:5px;">介绍</div>
        </el-col>
        <el-col :span="12">
          <el-input v-model="form.des" autocomplete="off"></el-input>
        </el-col>
      </el-row>
      <el-row :gutter="10">
        <el-col :span="3">
          <div style="text-align:center;margin:5px;">新密码（不更改，请输入上次密码）</div>
        </el-col>
        <el-col :span="12">
          <el-input type="password" v-model="form.password" autocomplete="off"></el-input>
        </el-col>
      </el-row>
      <el-row :gutter="10">
        <el-col :span="3">
          <div style="text-align:center;margin:5px;">确认密码</div>
        </el-col>
        <el-col :span="12">
          <el-input type="password" v-model="form.comfirm" autocomplete="off"></el-input>
        </el-col>
      </el-row>
      <el-row :gutter="10">
        <el-col :span="3">
          <div style="text-align:center;margin:5px;">学校</div>
        </el-col>
        <el-col :span="12">
          <el-input v-model="form.school" autocomplete="off"></el-input>
        </el-col>
      </el-row>
      <el-row :gutter="10">
        <el-col :span="3">
          <div style="text-align:center;margin:5px;">专业</div>
        </el-col>
        <el-col :span="12">
          <el-input v-model="form.course" autocomplete="off"></el-input>
        </el-col>
      </el-row>
      <el-row :gutter="10">
        <el-col :span="3">
          <div style="text-align:center;margin:5px;">班级</div>
        </el-col>
        <el-col :span="12">
          <el-input v-model="form.classes" autocomplete="off"></el-input>
        </el-col>
      </el-row>
      <el-row :gutter="10">
        <el-col :span="3">
          <div style="text-align:center;margin:5px;">学号</div>
        </el-col>
        <el-col :span="12">
          <el-input v-model="form.number" autocomplete="off"></el-input>
        </el-col>
      </el-row>
      <el-row :gutter="10">
        <el-col :span="3">
          <div style="text-align:center;margin:5px;">真实姓名</div>
        </el-col>
        <el-col :span="12">
          <el-input v-model="form.realname" autocomplete="off"></el-input>
        </el-col>
      </el-row>
      <el-row :gutter="10">
        <el-col :span="3">
          <div style="text-align:center;margin:5px;">QQ</div>
        </el-col>
        <el-col :span="12">
          <el-input v-model="form.qq" autocomplete="off"></el-input>
        </el-col>
      </el-row>
      <el-row :gutter="10">
        <el-col :span="3">
          <div style="text-align:center;margin:5px;">Email</div>
        </el-col>
        <el-col :span="12">
          <el-input v-model="form.email" autocomplete="off"></el-input>
        </el-col>
      </el-row>
    </el-form>

    <el-button type="primary" @click="updateClick">更新</el-button>
  </el-card>
</template>

<script>
export default {
  name: "setting",
  data() {
    return {
      username: "",
      name: "",
      form: {
        username: "",
        password: "",
        comfirm: "",
        name: "",
        des:"",
        school: "",
        course: "",
        classes: "",
        number: "",
        realname: "",
        qq: "",
        email: ""
      },
      userid: -1
    };
  },
  methods: {
    updateClick() {
      if (!this.username) {
        this.$message.error("非法访问！");
        return;
      }
      if (
        !this.form.name ||
        !this.form.school ||
        !this.form.course ||
        !this.form.classes ||
        !this.form.number ||
        !this.form.realname ||
        !this.form.qq ||
        !this.form.email
      ) {
        this.$message.error("字段不能为空！");
        return;
      }
      if (this.form.password != this.form.comfirm) {
        this.$message.error("两次密码不一致！");
        return;
      }

      if (this.form.name.length < 2) {
        this.$message.error("昵称太短！");
        return;
      }

      if (!this.form.password) {
        this.$message.error("请输入密码");
        return;
      }

      if (this.form.password.length < 6) {
        this.$message.error("密码太短！");
        return;
      }

      if(this.form.des.length<=0){
        this.form.des="这个人很懒，什么都没有没有留下。"
      }

 this.$confirm(
        "确定更新吗?",
        "如果你在参与一场比赛，请勿更新你的【昵称】，会影响排行榜计算，后果自负！",
        {
          confirmButtonText: "确定",
          cancelButtonText: "取消",
          type: "warning"
        }
      ).then(() => {

      this.form.password = this.$md5(this.form.password);
      this.$axios
        .put(
          "/changeone/",
          this.form
        )
        
            .then(
              response => {
                this.$message({
                  message: "更新成功！",
                  type: "success"
                });
                sessionStorage.setItem("name", this.form.name);
                this.$router.push({
                  name: "user",
                  query: { username: this.form.username }
                });
              },
              response => {
                this.$message.error("更新失败（" + response + "）");
              }
            );
        
      })



    }
  },
  created() {
    this.username = this.$route.params.username;
    this.form.username = this.username;
    if (this.username) {
      this.$axios
        .get(
          "/user/?username=" +
            this.username
        )
        .then(response => {
          this.form.name = response.data[0].name;
          this.form.school = response.data[0].school;
          this.form.course = response.data[0].course;
          this.form.classes = response.data[0].classes;
          this.form.number = response.data[0].number;
          this.form.realname = response.data[0].realname;
          this.form.qq = response.data[0].qq;
          this.form.email = response.data[0].email;
          this.userid = this.username;
        });
    }
  }
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
#card {
  margin: 200px;
  padding: 200px;
}
.el-table .warning-row {
  background: #fff9f9;
}

.el-table .success-row {
  background: #e6ffdf;
}

.el-table .info-row {
  background: #fffff7;
}

.el-table .judging-row {
  background: #f7ffff;
}

.el-table .danger-row {
  background: #fff9f9;
}

.el-tag {
  text-align: center;
  font-weight: bold;
}
</style>
