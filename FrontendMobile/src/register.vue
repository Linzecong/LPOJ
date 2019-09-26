<template>

  <mu-dialog title="Register" width="90%" scrollable :open.sync="dialogRegisterVisible">
    <mu-form ref="form" :model="form">
      <mu-form-item label="UserName" prop="username">
        <mu-text-field v-model="form.username" prop="username"></mu-text-field>
      </mu-form-item>

      <mu-form-item label="NickName" prop="nickname">
        <mu-text-field v-model="form.name" prop="nickname"></mu-text-field>
      </mu-form-item>

      <mu-form-item label="Password" prop="password">
        <mu-text-field type="password" v-model="form.password" prop="password"></mu-text-field>
      </mu-form-item>
      <mu-form-item label="ComfirmPassword" prop="comfirm">
        <mu-text-field type="password" v-model="form.comfirm" prop="comfirm"></mu-text-field>
      </mu-form-item>
      <mu-form-item label="School" prop="school">
        <mu-text-field v-model="form.school" prop="school"></mu-text-field>
      </mu-form-item>
      <mu-form-item label="Course" prop="course">
        <mu-text-field v-model="form.course" prop="course"></mu-text-field>
      </mu-form-item>

      <mu-form-item label="Class" prop="classes">
        <mu-text-field v-model="form.classes" prop="classes"></mu-text-field>
      </mu-form-item>

      <mu-form-item label="Number(学号)" prop="number">
        <mu-text-field v-model="form.number" prop="number"></mu-text-field>
      </mu-form-item>

      <mu-form-item label="RealName" prop="realname">
        <mu-text-field v-model="form.realname" prop="realname"></mu-text-field>
      </mu-form-item>

      <mu-form-item label="QQ" prop="qq">
        <mu-text-field v-model="form.qq" prop="qq"></mu-text-field>
      </mu-form-item>

      <mu-form-item label="Email" prop="email">
        <mu-text-field v-model="form.email" prop="email"></mu-text-field>
      </mu-form-item>


    </mu-form>
    <mu-button slot="actions" flat color="primary" @click="registerClick">REGISTER</mu-button>
  </mu-dialog>

</template>

<script>
export default {
  name: "register",
  data() {
    return {
      dialogRegisterVisible: false,
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
        email: ""
      }
    };
  },
  methods: {
    open() {
      this.dialogRegisterVisible = true;
    },
    registerClick() {
      if (
        !this.form.name ||
        !this.form.school ||
        !this.form.course ||
        !this.form.classes ||
        !this.form.number ||
        !this.form.realname
      ) {
        this.$message.error("字段不能为空！");
        return;
      }
      if (this.form.password != this.form.comfirm) {
        this.$message.error("两次密码不一致！");
        return;
      }
      if (this.form.username.length < 3) {
        this.$message.error("用户名太短！");
        return;
      }
      if (this.form.name.length < 2) {
        this.$message.error("昵称太短！");
        return;
      }
      if (this.form.password.length < 6) {
        this.$message.error("密码太短！");
        return;
      }
      if (
        this.form.username.indexOf("|") >= 0 ||
        this.form.username.indexOf("'") >= 0 ||
        this.form.username.indexOf("#") >= 0
      ) {
        this.$message.error("用户名包含非法字符！");
        return;
      }
      if (
        this.form.username.indexOf("{") >= 0 ||
        this.form.username.indexOf("(") >= 0 ||
        this.form.username.indexOf(")") >= 0
      ) {
        this.$message.error("用户名包含非法字符！");
        return;
      }

      this.form.password = this.$md5(this.form.password);

      this.$axios
        .post("/userdata/", this.form)
        .then(response => {
          this.$axios
            .post("/register/", this.form)
            .then(response => {
              if (response.data == "usererror") {
                this.$message.error("用户名已存在！");
                return;
              }
              this.$message({
                message: "注册成功！",
                type: "success"
              });
              this.dialogRegisterVisible = false;
              this.form.password = "";
            })
            .catch(error => {
              this.$message.error(
                "服务器错误！" + "(" + JSON.stringify(error.response.data) + ")"
              );
            });
        })
        .catch(error => {
          if (JSON.stringify(error.response.data).indexOf("user") >= 0)
            this.$message.error("用户名已存在！");
          else
            this.$message.error(
              "服务器错误！" + "(" + JSON.stringify(error.response.data) + ")"
            );
        });
    }
  }
};
</script>

<style  scoped>
.el-row {
  margin-bottom: 20px;
}
</style>