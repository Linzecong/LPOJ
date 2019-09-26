<template>
  <el-card>
    <h2>{{'编辑 '+username+' 的代码：'}}</h2>
    <el-row>
      <el-input placeholder="请输入模板描述" v-model="mbDes" style="width:300px;"></el-input>
    </el-row>
    <el-row>
      <el-autocomplete
        placeholder="请输入代码分组"
        :fetch-suggestions="queryGroup"
        v-model="group"
        style="width:300px;"
      ></el-autocomplete>
      <el-autocomplete
        placeholder="请输入代码标题"
        :fetch-suggestions="queryTitle"
        v-model="title"
        style="margin-left:30px;width:300px;"
      ></el-autocomplete>
      <el-button type="primary" @click="getcode" style="margin-left:30px;">获取代码</el-button>
    </el-row>
    <el-row>
      <el-input type="textarea" placeholder="请输入代码介绍，支持MD格式，在导出时有效" v-model="des" style="width:300px;"></el-input>
    </el-row>
    <el-row>
      <codemirror v-model="code" :options="cmOptions"></codemirror>
    </el-row>
    <el-row>
      <el-button type="primary" @click="save">保存代码</el-button>
    </el-row>
  </el-card>
</template>

<script>
import { codemirror } from "vue-codemirror";
require("codemirror/lib/codemirror.css");
require("codemirror/theme/base16-light.css");
require("codemirror/mode/clike/clike");
export default {
  name: "codeedit",
  components: {
    codemirror
  },
  data() {
    return {
      cmOptions: {
        tabSize: 4,
        mode: "text/x-c++src",
        theme: "base16-light",
        lineNumbers: true
      },
      mbDes: "",
      group: "",
      title: "",
      des: "",
      username: "",
      code: "",
      id: 0,
      groups: [],
      titles: [],
      no: false
    };
  },
  created() {
    if (sessionStorage.type == 3) this.username = "std";
    else this.username = sessionStorage.username;
    if (!this.username) {
      this.$message.error("请先登录");
      this.username = "匿名用户";
    }

    this.$axios
      .get("/mbcode/?username=" + this.username)
      .then(response => {
        this.mbDes = response.data.length > 0 ? response.data[0].des : "";
        this.no = response.data.length > 0 ? false : true;
      })
      .catch(error => {
        this.$message.error(
          "服务器错误！" + "(" + JSON.stringify(error.response.data) + ")"
        );
      });

    this.$axios
      .get("/mbcodedetailnocode/?username=" + this.username)
      .then(response => {
        for (let i = 0; i < response.data.length; i++) {
          this.groups.push(response.data[i].group);
        }
        this.$axios
          .get("/mbcodedetailnocode/?username=std")
          .then(response2 => {
            for (let i = 0; i < response2.data.length; i++) {
              this.groups.push(response2.data[i].group);
            }
            this.groups = this.uniq(this.groups);
          })
          .catch(error => {
            this.$message.error(
              "服务器错误！" + "(" + JSON.stringify(error.response.data) + ")"
            );
          });
      })
      .catch(error => {
        this.$message.error(
          "服务器错误！" + "(" + JSON.stringify(error.response.data) + ")"
        );
      });
  },
  methods: {
    uniq(array) {
      var temp = []; //一个新的临时数组
      for (var i = 0; i < array.length; i++) {
        if (temp.indexOf(array[i]) == -1) {
          temp.push(array[i]);
        }
      }
      return temp;
    },
    queryGroup(queryString, cb) {
      var groups = this.groups;
      var results = queryString
        ? groups.filter(this.createStateFilter(queryString))
        : groups;

      var res = [];
      for (let i = 0; i < results.length; i++) res.push({ value: results[i] });
      cb(res);
    },
    queryTitle(queryString, cb) {
      if (this.group == "") {
        return cb([{ value: "请先输入分组" }]);
      }
      this.titles = [];
      this.$axios
        .get(
          "/mbcodedetailnocode/?username=" +
            this.username +
            "&group=" +
            this.group
        )
        .then(response => {
          for (let i = 0; i < response.data.length; i++) {
            this.titles.push(response.data[i].title);
          }
          this.$axios
            .get("/mbcodedetailnocode/?username=std&group=" + this.group)
            .then(response2 => {
              for (let i = 0; i < response2.data.length; i++) {
                this.titles.push(response2.data[i].title);
              }
              this.titles = this.uniq(this.titles);
              var titles = this.titles;
              var results = queryString
                ? titles.filter(this.createStateFilter(queryString))
                : titles;

              var res = [];
              for (let i = 0; i < results.length; i++)
                res.push({ value: results[i] });
              cb(res);
            })
            .catch(error => {
              this.$message.error(
                "服务器错误！" + "(" + JSON.stringify(error.response.data) + ")"
              );
            });
        })
        .catch(error => {
          this.$message.error(
            "服务器错误！" + "(" + JSON.stringify(error.response.data) + ")"
          );
        });
    },
    createStateFilter(queryString) {
      return state => {
        return state.indexOf(queryString) === 0;
      };
    },
    getcode() {
      if (this.title != "" && this.group != "") {
        this.$axios
          .get(
            "/mbcodedetail/?username=" +
              this.username +
              "&group=" +
              this.group +
              "&title=" +
              this.title
          )
          .then(response => {
            if (response.data.length == 0) {
              this.id = 0;
              this.$message.success("未查找到代码，提交代码将新建代码！");
            } else {
              this.id = response.data[0].id;
              this.code = response.data[0].code;
              this.des = response.data[0].des;
              this.$message.success("获取成功，修改将覆盖代码！");
            }
          })
          .catch(error => {
            this.$message.error(
              "服务器错误！" + "(" + JSON.stringify(error.response.data) + ")"
            );
          });
      } else {
        this.$message.error("请输入分组和标题");
      }
    },
    save() {
      if (this.username == "匿名用户") {
        this.$message.error("请先登录");
        return;
      }
      if (this.mbDes == "") {
        this.$message.error("请输入模板描述！");
        return;
      } else {
        if (this.no == true) {
          this.$axios
            .post("/mbcode/", {
              username: this.username,
              des: this.mbDes
            })
            .then(response => {})
            .catch(error => {
              this.$message.error(
                "服务器错误！" + "(" + JSON.stringify(error.response.data) + ")"
              );
            });
        } else {
          this.$axios
            .put("/mbcode/" + this.username + "/", {
              des: this.mbDes
            })
            .then(response => {})
            .catch(error => {
              this.$message.error(
                "服务器错误！" + "(" + JSON.stringify(error.response.data) + ")"
              );
            });
        }

        if (this.id != 0) {
          this.$axios
            .put("/mbcodedetail/" + this.id + "/", {
              username: this.username,
              title: this.title,
              des: this.des,
              group: this.group,
              code: this.code
            })
            .then(response => {
              this.$message.success("保存代码成功！");
            })
            .catch(error => {
              this.$message.error(
                "服务器错误！" + "(" + JSON.stringify(error.response.data) + ")"
              );
            });
        } else {
          this.$axios
            .post("/mbcodedetail/", {
              username: this.username,
              title: this.title,
              des: this.des,
              group: this.group,
              code: this.code
            })
            .then(response => {
              this.$message.success("新建代码成功！");
            })
            .catch(error => {
              this.$message.error(
                "服务器错误！" + "(" + JSON.stringify(error.response.data) + ")"
              );
            });
        }
      }
    }
  }
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>
