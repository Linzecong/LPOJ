<template>
  <div id="app" style="top:0px;left:0px;">

    <mu-appbar id="nav" style="width: 100%;" color="primary">
      <mu-button icon slot="left" @click="opendrawer=!opendrawer">
        <mu-icon value="menu"></mu-icon>
      </mu-button>
      LPOJ
      <mu-button flat slot="right" @click="loginopen" v-show="!loginshow">Login</mu-button>
      <mu-button flat slot="right" @click="registeropen" v-show="!loginshow">Register</mu-button>


      <mu-menu slot="right" v-show="loginshow" :open.sync="openusermenu">
        <mu-button flat><mu-icon value="account_circle">{{"  "}}</mu-icon>{{"  "+name}}</mu-button>
        <mu-list slot="content" @change="handleCommand">
          <mu-list-item button value="home">
            <mu-list-item-content>
              <mu-list-item-title>Home</mu-list-item-title>
            </mu-list-item-content>
          </mu-list-item>

          <mu-list-item button value="submittion">
            <mu-list-item-content>
              <mu-list-item-title>Submittion</mu-list-item-title>
            </mu-list-item-content>
          </mu-list-item>

          <mu-list-item button value="setting">
            <mu-list-item-content>
              <mu-list-item-title>Setting</mu-list-item-title>
            </mu-list-item-content>
          </mu-list-item>

          <mu-list-item button v-show="isadmin" value="admin">
            <mu-list-item-content>
              <mu-list-item-title>Admin</mu-list-item-title>
            </mu-list-item-content>
          </mu-list-item>

          <mu-list-item button value="logout">
            <mu-list-item-content>
              <mu-list-item-title>Logout</mu-list-item-title>
            </mu-list-item-content>
          </mu-list-item>


        </mu-list>
      </mu-menu>

    </mu-appbar>

    <mu-appbar style="width: 100%;">
    </mu-appbar>
    
    <transition name="el-fade-in-linear" mode="out-in">
      <router-view id="route"></router-view>
    </transition>


    <div class="footer">
      <p>
        <!-- <a href="http://www.miitbeian.gov.cn" target="_blank" style="text-decoration: none;color:#409EFF;">粤ICP备19042174号-1</a> -->
      </p>
      <p>
        Powered by
        <a
          href="https://github.com/Linzecong/LPOJ"
          target="_blank"
          style="text-decoration: none;color:#409EFF;"
        >Linzecong</a>
        <span>
          &nbsp; Version: 3.1&nbsp;&nbsp; Docs:&nbsp;&nbsp;
          <a
            href="https://docs.lpoj.cn"
            target="_blank"
            style="text-decoration: none;color:#409EFF;"
          >LPOJ Docs</a>
        </span>
      </p>
    </div>


    <mu-drawer :open.sync="opendrawer" :docked="false" :right="false">
      <mu-list @change="opendrawer=false">
        <mu-list-item button to="/main">
          <mu-list-item-action>
              <mu-icon value="home"></mu-icon>
          </mu-list-item-action>
          <mu-list-item-title>Home</mu-list-item-title>
        </mu-list-item>

        <mu-list-item button to="/problem">
          <mu-list-item-action>
              <mu-icon value="assignment"></mu-icon>
          </mu-list-item-action>
          <mu-list-item-title>Problem</mu-list-item-title>
        </mu-list-item>
        
        <mu-list-item button to="/statue">
          <mu-list-item-action>
              <mu-icon value="reorder"></mu-icon>
          </mu-list-item-action>
          <mu-list-item-title>Status</mu-list-item-title>
        </mu-list-item>

        <mu-list-item button to="/contest">
          <mu-list-item-action>
              <mu-icon value="event"></mu-icon>
          </mu-list-item-action>
          <mu-list-item-title>Contest</mu-list-item-title>
        </mu-list-item>

        <mu-list-item button to="/rank">
          <mu-list-item-action>
              <mu-icon value="stars"></mu-icon>
          </mu-list-item-action>
          <mu-list-item-title>Rank</mu-list-item-title>
        </mu-list-item>

        <mu-list-item button to="/wiki">
          <mu-list-item-action>
              <mu-icon value="grade"></mu-icon>
          </mu-list-item-action>
          <mu-list-item-title>Wiki</mu-list-item-title>
        </mu-list-item>
      </mu-list>
    </mu-drawer>

    <register ref="registerdialog"></register>
    <login ref="logindialog"></login>

    <el-backtop :bottom="50">
      <div
        style="{
        height: 100%;
        width: 100%;
        background-color: #f2f5f6;
        box-shadow: 0 0 6px rgba(0,0,0, .12);
        text-align: center;
        line-height: 40px;
        color: #1989fa;
      }"
      >UP</div>
    </el-backtop>

    
    
  </div>
</template>

<script>
import login from "@/login";
import register from "@/register";
export default {
  name: "App",
  components: {
    login,
    register
  },
  data() {
    return {
      activeIndex: "1",
      school: "LPOJ",
      loginshow: sessionStorage.username,
      username: sessionStorage.username,
      name: sessionStorage.name,
      isadmin: false,
      opendrawer:false,
      openusermenu:false,
    };
  },
  mounted() {
    this.isadmin = sessionStorage.type == 2 || sessionStorage.type == 3;
    this.$axios
      .get("/settingboard/")
      .then(res => {
        if (res.data.length > 0) this.school = res.data[0].ojname;
        else this.school = "LPOJ";
      })
      .catch(error => {
        this.$message.error(
          "服务器错误！" + "(" + JSON.stringify(error.response.data) + ")"
        );
      });
  },
  methods: {
    loginopen() {
      this.$refs.logindialog.open();
    },
    registeropen() {
      this.$refs.registerdialog.open();
    },

    handleCommand(command) {
      this.openusermenu = false;
      if (command == "logout") {
        this.$axios
          .get("/logout/")
          .then(response => {
            this.$message({
              message: "登出成功！",
              type: "success"
            });
            sessionStorage.setItem("username", "");
            sessionStorage.setItem("name", "");
            sessionStorage.setItem("rating", "");
            sessionStorage.setItem("type", "");
            this.loginshow = 0;
            this.username = "";
            this.$router.go(0);
          })
          .catch(error => {
            this.$message.error(
              "服务器错误！" + "(" + JSON.stringify(error.response.data) + ")"
            );
          });
      }
      if (command == "home") {
        this.$router.push({
          name: "user",
          query: { username: sessionStorage.username }
        });
      }
      if (command == "setting") {
        this.$router.push({
          name: "setting",
          params: { username: sessionStorage.username }
        });
      }
      if (command == "submittion") {
        this.$router.push({
          name: "statue",
          query: { username: sessionStorage.username }
        });
      }
      if (command == "admin") {
        this.$router.push({
          name: "admin"
        });
      }
    }
  }
};
</script>

<style scope>
.el-dropdown-link {
  cursor: pointer;
  color: #409eff;
}
#button {
  float: right;
  margin: 10px;
}
#user {
  float: right;
  margin: 10px;
}
#nav {
  position: fixed;
  left: 0px;
  top: 0px;
  z-index: 5;
  width: 100%;
  /* box-shadow: 00px 0px 00px rgb(255, 255, 255),
    0px 0px 10px rgb(255, 255, 255),
     0px 0px 0px rgb(255, 255, 255),
     1px 1px 0px rgb(218, 218, 218);  */
}
#drawer {
  position: fixed;
  left: 0px;
  bottom: 0px;
  z-index: 5;
  width: 100%;
   box-shadow: 00px 0px 00px rgb(255, 255, 255),
    0px 0px 10px rgb(255, 255, 255),
     0px 0px 0px rgb(255, 255, 255),
     1px 1px 0px rgb(218, 218, 218);
}
#route {
  position: relative;
  top: 10px;
}
#title {
  font-size: 20px;
  font-weight: bold;
}
.el-row {
  margin-bottom: 20px;
}
.footer {
  margin-top: 20px;
  margin-bottom: 10px;
  text-align: center;
  font-size: small;
}
</style>
