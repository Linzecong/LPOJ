<template>
  <el-dialog title="登录" :visible.sync="dialogLoginVisible">
    <el-form :model="form" @keyup.native.enter="loginClick">
      <el-row :gutter="10">
        <el-col :span="3">
          <div style="text-align:center;margin:5px;">User</div>
        </el-col>
        <el-col :span="12">
          <el-input v-model="form.username" autocomplete="off" :autofocus="true"></el-input>
        </el-col>
      </el-row>
      <el-row :gutter="10">
        <el-col :span="3">
          <div style="text-align:center;margin:5px;">Password</div>
        </el-col>
        <el-col :span="12">
          <el-input type="password" v-model="form.password" autocomplete="off"></el-input>
        </el-col>
      </el-row>
    </el-form>
    <div slot="footer" class="dialog-footer">
      <el-button @click="dialogLoginVisible = false">Cancel</el-button>
      <el-button type="primary" @click="loginClick">OK</el-button>
    </div>
  </el-dialog>
</template>

<script>
export default {
  name: "login",
  data() {
    return {
      dialogLoginVisible: false,
      form: {
        username: "",
        password: ""
      }
    };
  },
  methods: {
    open() {
      this.dialogLoginVisible = true;
    },
    loginClick() {
      var pas = this.$md5(this.form.password);
      this.$axios
        .post("/login/", {
          username: this.form.username,
          password: pas
        })
        .then(response => {
          if (response.data == "passworderror") {
            this.$message.error("密码错误");
            return;
          }
          this.$message({
            message: "登录成功！",
            type: "success"
          });

          sessionStorage.setItem("username", this.form.username);
          sessionStorage.setItem("name", response.data.name);
          sessionStorage.setItem("type", response.data.type);

          this.dialogLoginVisible = false;

          this.$axios
            .post("/userlogindata/", {
              username: this.form.username,
              ip: this.$store.state.loginip,
              msg: this.$store.state.logininfo
            })
            .then(response => {
              this.$router.go(0);
            })
            .catch(error => {
              this.$message.error(
                "服务器错误！" + "(" + JSON.stringify(error.response.data) + ")"
              );
              sessionStorage.setItem("username", "");
              sessionStorage.setItem("name", "");
              sessionStorage.setItem("rating", "");
              sessionStorage.setItem("type", "");
              sessionStorage.setItem("acpro", "");
            });
        })
        .catch(error => {
          this.$message.error("用户名不存在（" + error + "）");
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