<template>
  <div>
    <el-row v-if="!isnew">
      <el-select v-model="editpage" placeholder="请输入编辑的页面" @change="typechange" filterable>
        <algorithmselect></algorithmselect>
      </el-select>
      <el-button style="margin-left:50px" type="primary" @click="save">保存</el-button>
    </el-row>

    <el-button type="primary" @click="isnew = !isnew">{{isnew==true?'编辑已存在的词条':'新建词条'}}</el-button>

    <el-row v-if="isnew" style="margin-top:20px;">
      <el-input v-model="title" placeholder="请输入词条名称，如线段树" style="width:20%;"></el-input>
      <el-input
        style="margin-left:20px;width:20%;"
        v-model="type"
        placeholder="请输入index，详见说明"
        @change="newtypechange"
      ></el-input>
      <el-select style="margin-left:20px;width:20%;" v-model="group" placeholder="请输入分组" filterable>
        <el-option key="basic" label="基础算法" value="basic"></el-option>
        <el-option key="search" label="搜索" value="search"></el-option>
        <el-option key="string" label="字符串" value="string"></el-option>
        <el-option key="math" label="数学" value="math"></el-option>
        <el-option key="ds" label="数据结构" value="ds"></el-option>
        <el-option key="graph" label="图论" value="graph"></el-option>
        <el-option key="geometry" label="计算机和" value="geometry"></el-option>
        <el-option key="dp" label="动态规划" value="dp"></el-option>
        <el-option key="misc" label="杂项" value="misc"></el-option>
        <el-option key="intro" label="简介" value="intro"></el-option>
      </el-select>
      <el-button style="margin-left:50px" type="primary" @click="save">保存</el-button>
      <p>说明：index要尽力分好类，并且以两个下划线隔开，如字符串的就用string__aaa</p>
    </el-row>

    <mavon-editor
      style="margin-top:20px"
      v-model="context"
      :toolbars="toolbars"
      @save="savemethod"
      @imgAdd="$imgAdd"
      v-loading="loading"
    />
  </div>
</template>

<script>
import moment from "moment";
import { mavonEditor } from "mavon-editor";
import "mavon-editor/dist/css/index.css";
import algorithmselect from "@/components/utils/algorithmselect";
export default {
  name: "editalgorithm",
  components: {
    mavonEditor,
    algorithmselect
  },

  data() {
    return {
      context: " ", //输入的数据
      editpage: "",
      username: "",
      title: "",
      type: "",
      group: "",
      curid: 0,
      loading: false,
      toolbars: {
        bold: true, // 粗体
        italic: true, // 斜体
        header: true, // 标题
        underline: true, // 下划线
        mark: true, // 标记
        superscript: true, // 上角标
        quote: true, // 引用
        ol: true, // 有序列表
        link: true, // 链接
        imagelink: true, // 图片链接
        help: true, // 帮助
        code: true, // code
        subfield: true, // 是否需要分栏
        fullscreen: true, // 全屏编辑
        readmodel: true, // 沉浸式阅读
        /* 1.3.5 */
        undo: true, // 上一步
        trash: true, // 清空
        save: true, // 保存（触发events中的save事件）
        /* 1.4.2 */
        navigation: true // 导航目录
      },

      isnew: false
    };
  },
  created() {
    if (sessionStorage.type == 3) this.username = "std";
    else this.username = sessionStorage.username;
    if (!this.username) {
      this.$message.error("请先登录");
      this.username = "匿名用户";
    }
  },
  methods: {
    $imgAdd(pos, $file) {
      this.$message.error("暂不支持上传图片！请使用链接添加！");
    },
    save() {
      if (!this.username) {
        this.$message.error("请先登录");
        return;
      }
      this.$message.error(
        "记得保存喔！请使用编辑器中的保存按钮保存！或Ctrl + S"
      );
    },
    savemethod(v, r) {
      if (this.username == "匿名用户") {
        this.$message.error("请先登录");
        return;
      }

      if (this.isnew == false) {
        if (this.curid == 0) {
          this.$axios
            .post("/wiki/", {
              username: this.username,
              value: v,
              type: this.editpage
            })
            .then(response => {
              this.$message.success(
                "保存成功！" +
                  moment(response.data.time).format("YYYY-MM-DD HH:mm:ss")
              );
              this.curid = response.data.id;
            })
            .catch(error => {
              this.$message.error(
                "服务器错误！" + "(" + JSON.stringify(error.response.data) + ")"
              );
            });
        } else {
          this.$axios
            .put("/wiki/" + this.curid + "/", {
              username: this.username,
              value: v,
              type: this.editpage
            })
            .then(response => {
              this.$message.success(
                "保存成功！" +
                  moment(response.data.time).format("YYYY-MM-DD HH:mm:ss")
              );
            })
            .catch(error => {
              this.$message.error(
                "服务器错误！" + "(" + JSON.stringify(error.response.data) + ")"
              );
            });
        }
      } else {
        if (this.type.indexOf("__") < 0) {
          this.$message.error("index请用两个下划线隔开");
          return;
        }
        if (this.curid == 0) {
          this.$axios
            .post("/wiki/", {
              username: this.username,
              value: v,
              type: this.type,
              group: this.group,
              std: 1,
              title: this.title
            })
            .then(response => {
              this.$message.success(
                "保存成功！" +
                  moment(response.data.time).format("YYYY-MM-DD HH:mm:ss")
              );
              this.curid = response.data.id;
            })
            .catch(error => {
              this.$message.error(
                "服务器错误！" + "(" + JSON.stringify(error.response.data) + ")"
              );
            });
        } else {
          this.$axios
            .put("/wiki/" + this.curid + "/", {
              username: this.username,
              value: v,
              type: this.type,
              group: this.group,
              std: 1,
              title: this.title
            })
            .then(response => {
              this.$message.success(
                "保存成功！" +
                  moment(response.data.time).format("YYYY-MM-DD HH:mm:ss")
              );
            })
            .catch(error => {
              this.$message.error(
                "服务器错误！" + "(" + JSON.stringify(error.response.data) + ")"
              );
            });
        }
      }
    },
    typechange(value) {
      this.loading = true;
      this.$axios
        .get("/wiki/?username=" + this.username + "&type=" + value)
        .then(response => {
          this.loading = false;
          this.context =
            response.data.length > 0
              ? response.data[0].value
              : "# 暂无你的数据";
          this.curid = response.data.length > 0 ? response.data[0].id : 0;
          // if (response.data.length > 0) {
          //   this.$store.state.edittimer = setInterval(this.save, 120000);
          // }
        })
        .catch(error => {
          this.$message.error(
            "服务器错误！" + "(" + JSON.stringify(error.response.data) + ")"
          );
        });
    },
    newtypechange(value) {
      this.loading = true;
      this.$axios
        .get("/wiki/?username=" + this.username + "&type=" + value)
        .then(response => {
          this.loading = false;
          this.context =
            response.data.length > 0
              ? response.data[0].value
              : "# 暂无你的数据";
          this.curid = response.data.length > 0 ? response.data[0].id : 0;
          this.title = response.data[0].title;
          this.group = response.data[0].group;
        })
        .catch(error => {
          this.$message.error(
            "服务器错误！" + "(" + JSON.stringify(error.response.data) + ")"
          );
        });
    }
  },
  destroyed() {
    //clearInterval(this.$store.state.edittimer);
  }
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>
