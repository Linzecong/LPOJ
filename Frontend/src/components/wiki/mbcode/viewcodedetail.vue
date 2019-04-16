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
    </el-alert>

    <codemirror id="mycode" v-model="codeData.code" :options="cmOptions"></codemirror>
  </el-card>
</template>

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
      cmOptions: {
        tabSize: 4,
        mode: "text/x-c++src",
        theme: "base16-light",
        lineNumbers: true,
        readOnly: true
      }
    };
  },
  created() {
    this.$axios
      .get("/mbcodedetail/" + this.$route.params.codeID + "/")
      .then(response => {
          if(response.data.length==0){
              this.codeData["username"] = 404
              this.codeData["title"] = 404
              this.codeData["group"] = 404
          }
        response.data.time = moment(response.data.time).format(
          "YYYY-MM-DD HH:mm:ss"
        );
        this.codeData = response.data;
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
    }
  }
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>
