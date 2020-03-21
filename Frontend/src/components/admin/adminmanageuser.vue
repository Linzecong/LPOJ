<template>
  <el-form :model="form">
    <el-input placeholder="搜索..."
              v-model="searchuser"
              @keyup.native.enter="searchuserdata"
              style="float:right;width:200px;">
      <el-button slot="append"
                 icon="el-icon-search"
                 @click="searchuserdata"></el-button>
    </el-input>
    <el-pagination @current-change="handleUserCurrentChange"
                   :current-page="usercurrentpage"
                   :page-size="10"
                   layout="total, prev, pager, next, jumper"
                   :total="totaluser"></el-pagination>

    <el-table :data="tableData"
              size="small">
      <el-table-column prop="username"
                       label="用户名"></el-table-column>
      <el-table-column prop="name"
                       label="昵称"></el-table-column>
      <el-table-column prop="school"
                       label="学校"></el-table-column>
      <el-table-column prop="course"
                       label="专业"></el-table-column>
      <el-table-column prop="classes"
                       label="班级"></el-table-column>
      <el-table-column prop="number"
                       label="学号"></el-table-column>
      <el-table-column prop="realname"
                       label="真实姓名"
                       width="80"></el-table-column>
      <el-table-column prop="email"
                       label="邮箱"></el-table-column>
      <el-table-column prop="type"
                       label="权限"
                       width="50"></el-table-column>
      <el-table-column prop="regtime"
                       label="注册时间"></el-table-column>
      <el-table-column fixed="right"
                       label="操作"
                       width="160">
        <template slot-scope="scope">
          <el-button @click="userclick(scope.row)"
                     type="primary"
                     size="small">编辑</el-button>
          <el-button @click="gouser(scope.row)"
                     type="primary"
                     size="small">查看</el-button>
        </template>
      </el-table-column>
    </el-table>

    <el-dialog title="登录记录"
               :visible.sync="dialogDataVisible"
               width="75%">
      <el-input placeholder="搜索用户名或IP..."
                v-model="searchlogin"
                @keyup.native.enter="searchdata"
                style="float:right;width:200px;">
        <el-button slot="append"
                   icon="el-icon-search"
                   @click="searchdata"></el-button>
      </el-input>
      <el-pagination @current-change="handleDataCurrentChange"
                     :current-page="datacurrentpage"
                     :page-size="50"
                     layout="total, prev, pager, next, jumper"
                     :total="totaldata"></el-pagination>

      <el-table :data="tableData2"
                size="mini">
        <el-table-column prop="username"
                         label="用户名"></el-table-column>
        <el-table-column prop="ip"
                         label="登录IP"></el-table-column>
        <el-table-column prop="logintime"
                         label="登录时间"></el-table-column>
        <el-table-column prop="msg"
                         label="其他信息"></el-table-column>
      </el-table>
    </el-dialog>

    <el-dialog title="修改用户信息"
               :visible.sync="dialogDataVisible2"
               width="85%">
      <el-row :gutter="10"
              style="margin-top:30px;">
        <el-col :span="3">
          <div style="text-align:center;margin:5px;">用户名</div>
        </el-col>
        <el-col :span="12">
          <el-input v-model="form.username"
                    autocomplete="off"
                    @keyup.native.enter="usernamechange"
                    @change="usernamechange"></el-input>
        </el-col>
        <el-button type="success"
                   @click="checklogin"
                   style="margin-left:20px;">查询登录记录</el-button>
      </el-row>

      <el-row :gutter="10">
        <el-col :span="3">
          <div style="text-align:center;margin:5px;">昵称</div>
        </el-col>
        <el-col :span="12">
          <el-input v-model="form.name"
                    autocomplete="off"></el-input>
        </el-col>
      </el-row>
      <el-row :gutter="10">
        <el-col :span="3">
          <div style="text-align:center;margin:5px;">密码</div>
        </el-col>
        <el-col :span="12">
          <el-input type="password"
                    v-model="password"
                    autocomplete="off"
                    placeholder="不修改密码则留空"></el-input>
        </el-col>
      </el-row>
      <el-row :gutter="10">
        <el-col :span="3">
          <div style="text-align:center;margin:5px;">确认密码</div>
        </el-col>
        <el-col :span="12">
          <el-input type="password"
                    v-model="comfirm"
                    autocomplete="off"
                    placeholder="不修改密码则留空"></el-input>
        </el-col>
      </el-row>
      <el-row :gutter="10">
        <el-col :span="3">
          <div style="text-align:center;margin:5px;">学校</div>
        </el-col>
        <el-col :span="12">
          <el-input v-model="form.school"
                    autocomplete="off"></el-input>
        </el-col>
      </el-row>
      <el-row :gutter="10">
        <el-col :span="3">
          <div style="text-align:center;margin:5px;">专业</div>
        </el-col>
        <el-col :span="12">
          <el-input v-model="form.course"
                    autocomplete="off"></el-input>
        </el-col>
      </el-row>
      <el-row :gutter="10">
        <el-col :span="3">
          <div style="text-align:center;margin:5px;">班级</div>
        </el-col>
        <el-col :span="12">
          <el-input v-model="form.classes"
                    autocomplete="off"></el-input>
        </el-col>
      </el-row>
      <el-row :gutter="10">
        <el-col :span="3">
          <div style="text-align:center;margin:5px;">学号</div>
        </el-col>
        <el-col :span="12">
          <el-input v-model="form.number"
                    autocomplete="off"></el-input>
        </el-col>
      </el-row>
      <el-row :gutter="10">
        <el-col :span="3">
          <div style="text-align:center;margin:5px;">真实姓名</div>
        </el-col>
        <el-col :span="12">
          <el-input v-model="form.realname"
                    autocomplete="off"></el-input>
        </el-col>
      </el-row>
      <el-row :gutter="10">
        <el-col :span="3">
          <div style="text-align:center;margin:5px;">QQ</div>
        </el-col>
        <el-col :span="12">
          <el-input v-model="form.qq"
                    autocomplete="off"></el-input>
        </el-col>
      </el-row>
      <el-row :gutter="10">
        <el-col :span="3">
          <div style="text-align:center;margin:5px;">Email</div>
        </el-col>
        <el-col :span="12">
          <el-input v-model="form.email"
                    autocomplete="off"></el-input>
        </el-col>
      </el-row>
      <el-row :gutter="10">
        <el-col :span="3">
          <div style="text-align:center;margin:5px;">权限</div>
        </el-col>
        <el-col :span="12">
          <el-select v-model="form.type"
                     placeholder="选择权限...">
            <el-option key="普通"
                       label="普通"
                       :value="1"></el-option>
            <el-option key="管理员"
                       label="管理员"
                       :value="2"></el-option>
            <el-option key="超级管理员"
                       label="超级管理员"
                       :value="3"></el-option>
          </el-select>
        </el-col>
        <el-button type="success"
                   @click="updateClick"
                   style="float:right;margin-right:10px;">更新</el-button>
      </el-row>
    </el-dialog>
  </el-form>
</template>

<script>
import moment from "moment";
export default {
  name: "adminmanageuser",
  data () {
    return {
      dialogDataVisible: false,
      dialogDataVisible2: false,
      tableData2: [],
      datacurrentpage: 1,
      totaldata: 0,
      searchlogin: "",

      tableData: [],
      usercurrentpage: 1,
      totaluser: 0,
      searchuser: "",

      form: {
        username: "",
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
      userid: -1,
      password: "",
      comfirm: ""
    };
  },
  methods: {
    gouser (row) {
      window.open("/user?username=" + row.username);
    },
    searchdata () {
      this.datacurrentpage = 1;
      this.$axios
        .get(
          "/userlogindata/?limit=50&offset=" +
          (this.datacurrentpage - 1) * 50 +
          "&search=" +
          this.searchlogin
        )
        .then(response => {
          this.totaldata = response.data.count;

          for (let i = 0; i < response.data.results.length; i++) {
            response.data.results[i].logintime = moment(
              response.data.results[i].logintime
            ).format("YYYY-MM-DD HH:mm:ss");
          }

          this.tableData2 = response.data.results;
        });
    },
    handleDataCurrentChange (val) {
      this.datacurrentpage = val;
      this.$axios
        .get(
          "/userlogindata/?limit=50&offset=" +
          (this.datacurrentpage - 1) * 50 +
          "&search=" +
          this.searchlogin
        )
        .then(response => {
          for (let i = 0; i < response.data.results.length; i++) {
            response.data.results[i].logintime = moment(
              response.data.results[i].logintime
            ).format("YYYY-MM-DD HH:mm:ss");
          }
          this.totaldata = response.data.count;
          this.tableData2 = response.data.results;
        });
    },
    checklogin () {
      this.dialogDataVisible = true;
      this.searchlogin = this.form.username;
      this.searchdata();
    },

    userclick (row) {
      this.form.username = row.username;
      this.usernamechange();
      this.dialogDataVisible2 = true;
    },
    searchuserdata () {
      this.usercurrentpage = 1;
      this.$axios
        .get(
          "/user/?limit=10&offset=" +
          (this.usercurrentpage - 1) * 10 +
          "&search=" +
          this.searchuser
        )
        .then(response => {
          for (let i = 0; i < response.data.results.length; i++) {
            response.data.results[i].regtime = moment(
              response.data.results[i].regtime
            ).format("YYYY-MM-DD HH:mm:ss");
          }
          this.totaluser = response.data.count;
          this.tableData = response.data.results;
        });
    },
    handleUserCurrentChange (val) {
      this.usercurrentpage = val;
      this.$axios
        .get(
          "/user/?limit=10&offset=" +
          (this.usercurrentpage - 1) * 10 +
          "&search=" +
          this.searchuser
        )
        .then(response => {
          for (let i = 0; i < response.data.results.length; i++) {
            response.data.results[i].regtime = moment(
              response.data.results[i].regtime
            ).format("YYYY-MM-DD HH:mm:ss");
          }
          this.totaluser = response.data.count;
          this.tableData = response.data.results;
        });
    },

    usernamechange () {
      if (this.form.username) {
        this.$axios
          .get("/user/?username=" + this.form.username)
          .then(response => {
            if (response.data.length <= 0) {
              this.$message.error("用户不存在！");
              return;
            }
            this.form = response.data[0];
            this.userid = this.form.username;
          })
          .catch(error => {
            this.$message.error(
              "服务器错误！" + JSON.stringify(error.response.data)
            );
          });
      }
    },

    updateClick () {
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
      if (this.password != this.comfirm) {
        this.$message.error("两次密码不一致！");
        return;
      }

      if (this.form.name.length < 2) {
        this.$message.error("昵称太短！");
        return;
      }

      var deepCopy = function (obj) {
        var str,
          newobj = obj.constructor === Array ? [] : {};
        if (typeof obj !== "object") {
          return;
        } else if (window.JSON) {
          (str = JSON.stringify(obj)), //系列化对象
            (newobj = JSON.parse(str)); //还原
        } else {
          for (var i in obj) {
            newobj[i] = typeof obj[i] === "object" ? cloneObj(obj[i]) : obj[i];
          }
        }
        return newobj;
      };

      var myform = deepCopy(this.form);

      if (this.form.type != 1 && this.form.type != 2 && this.form.type != 3) {
        this.$message.error("权限应为1,2,3");
        return;
      }

      if (this.password != "") {
        if (this.password.length < 6) {
          this.$message.error("密码太短！");
          return;
        }
        this.password = this.$md5(this.password);

        myform["password"] = this.password;
      }
      else {
        myform["password"] = "." //用于后台特判
      }

      this.$axios.put("/changeall/", myform).then(
        response => {
          this.$message({
            message: "更新成功！",
            type: "success"
          });
          this.form = {};
          this.dialogDataVisible2 = false;
        },
        response => {
          this.$message.error("更新失败（" + response.response.data + "）");
        }
      );
    }
  },
  created () {
    this.$axios.get("/user/?limit=10&offset=0").then(response => {
      for (let i = 0; i < response.data.results.length; i++) {
        response.data.results[i].regtime = moment(
          response.data.results[i].regtime
        ).format("YYYY-MM-DD HH:mm:ss");
      }
      this.totaluser = response.data.count;
      this.tableData = response.data.results;
    });
  }
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>
