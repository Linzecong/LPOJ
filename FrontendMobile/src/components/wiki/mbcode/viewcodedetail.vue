<template>
  <el-card>
    <el-alert
      :title="codeData.username+'   '+codeData.group+'   '+codeData.title"
      type="success"
      :closable="false"
      :description="codeData.des"
    ></el-alert>
    <el-alert :title="'最后编辑于：'+codeData.time+'  '" type="info" :closable="false">
      <el-button
        size="mini"
        v-clipboard:copy="codeData.code"
        v-clipboard:success="onCopy"
        v-clipboard:error="onError"
      >Copy</el-button>
      <el-button size="mini" type="danger" style="float:right;" @click="del" v-if="show">Delete</el-button>
    </el-alert>

    <codemirror v-model="codeData.code" :options="cmOptions"></codemirror>
  </el-card>
</template>

<style scope>
.CodeMirror {
  height: 500px;
}
</style>

<script>
import moment from "moment";
import { codemirror } from "vue-codemirror";
require("codemirror/lib/codemirror.css");
require("codemirror/theme/base16-light.css");
require("codemirror/mode/clike/clike");
export default {
  name: "mbcodedetaildetail",
  components: {
    codemirror
  },
  data() {
    return {
      codeid: this.$route.params.codeID,
      codeData: {},
      show: false,
      cmOptions: {
        tabSize: 4,
        mode: "text/x-c++src",
        theme: "base16-light",
        lineNumbers: true,
        readOnly: true,
        viewportMargin:Infinity,
        lineWrapping:true,
      }
    };
  },
  created() {
    this.$axios
      .get("/mbcodedetail/" + this.$route.params.codeID + "/")
      .then(response => {
        if (response.data.length == 0) {
          this.codeData["username"] = 404;
          this.codeData["title"] = 404;
          this.codeData["group"] = 404;
        }
        response.data.time = moment(response.data.time).format(
          "YYYY-MM-DD HH:mm:ss"
        );
        this.codeData = response.data;
        this.show =
          this.codeData.username == sessionStorage.username ||
          sessionStorage.type == 3;
      })
      .catch(error => {
        this.$message.error(
          "服务器错误！" + "(" + JSON.stringify(error.response.data) + ")"
        );
      });
  },
  methods: {
    onCopy(e) {
      this.$message.success("复制成功！");
    },
    // 复制失败
    onError(e) {
      this.$message.error("复制失败：" + e);
    },
    del() {
      if (
        this.codeData.username == sessionStorage.username ||
        sessionStorage.type == 3
      ) {
        this.$confirm("确定删除吗？", "删除！", {
          confirmButtonText: "确定",
          cancelButtonText: "取消",
          type: "warning"
        }).then(() => {
          this.$axios
            .delete("/mbcodedetail/" + this.$route.params.codeID + "/")
            .then(response => {
              this.$message.success("删除成功！");
            })
            .catch(error => {
              this.$message.error(
                "服务器错误！" + "(" + JSON.stringify(error.response.data) + ")"
              );
            });
        });
      }
    }
  }
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->

