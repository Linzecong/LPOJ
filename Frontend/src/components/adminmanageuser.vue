<template>
  <el-form :model="form">
    <el-row :gutter="10">
      <el-col :span="3">
        <div style="text-align:center;margin:5px;">用户名</div>
      </el-col>
      <el-col :span="12">
        <el-input v-model="form.username" autocomplete="off" @change="usernamechange"></el-input>
      </el-col>
    </el-row>

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
        <div style="text-align:center;margin:5px;">密码</div>
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
    <el-row :gutter="10">
      <el-col :span="3">
        <div style="text-align:center;margin:5px;">权限（1 普通 2 管理员 3 超级管理员）</div>
      </el-col>
      <el-col :span="12">
        <el-input v-model="form.type" autocomplete="off"></el-input>
      </el-col>
    </el-row>
    <el-button type="primary" @click="updateClick">更新</el-button>
  </el-form>
</template>

<script>
export default {
  name: "adminmanageuser",
  data() {
    return {
      form: {
        username: "",
        password: "",
        comfirm: "",
        name: "",
        school: "",
        course: "",
        classes: "",
        number: "",
        realname: "",
        qq: "",
        email: "",
        type: 1
      },
      userid: -1
    };
  },
  methods: {
    usernamechange() {
      if (this.form.username) {
        this.$axios
          .get(
            "/api/user/?username=" +
              this.form.username
          )
          .then(response => {
            if (response.data.length <= 0) {
              this.$message.error("用户不存在！");
              return;
            }
            this.form = response.data[0];
            this.userid = this.form.username;
          })
          .catch(error => {
            this.$message.error("服务器错误！" + error);
          });
      }
    },

    updateClick() {
      if (
        !this.form.name ||
        !this.form.school ||
        !this.form.course ||
        !this.form.classes ||
        !this.form.number ||
        !this.form.realname ||
        !this.form.qq ||
        !this.form.email ||
        !this.form.type ||
        !this.form.username
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
      if (this.form.type != 1 && this.form.type != 2 && this.form.type != 3) {
        this.$message.error("权限应为1,2,3");
        return;
      }

      this.form.password = this.$md5(this.form.password);
      this.$axios
        .put(
          "/api/changeall/" +
            this.userid +
            "/",
          this.form
        )
        .then(
          response => {
            this.$message({
              message: "更新成功！",
              type: "success"
            });
            this.form = {};
          },
          response => {
            this.$message.error("更新失败（" + response + "）");
          }
        );
    }
  },
  created() {}
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>
