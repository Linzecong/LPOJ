<template>
  <mu-dialog title="LOGIN" width="90%" :open.sync="dialogLoginVisible">
    <mu-form ref="form" :model="form">
      <mu-form-item label="UserName" prop="username">
        <mu-text-field v-model="form.username" prop="username"></mu-text-field>
      </mu-form-item>
      <mu-form-item label="Password" prop="password">
        <mu-text-field type="password" v-model="form.password" prop="password"></mu-text-field>
      </mu-form-item>
    </mu-form>
    <mu-button slot="actions" flat color="primary" @click="loginClick">LOGIN</mu-button>
  </mu-dialog>
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
            this.$toast.error("密码错误");
            return;
          }
          this.$toast.success("登录成功！");

          sessionStorage.setItem("username", this.form.username);
          sessionStorage.setItem("name", response.data.name);
          sessionStorage.setItem("type", response.data.type);

          this.dialogLoginVisible = false;

          this.$axios
            .post("/setlogindata/", {
              username: this.form.username,
              ip: this.$store.state.loginip,
              msg: this.$store.state.logininfo
            })
            .then(response => {
              this.$router.go(0);
            })
            .catch(error => {
              this.$toast.error(
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
          this.$toast.error("用户名不存在（" + error + "）");
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