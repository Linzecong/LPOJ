<template>
      <mavon-editor
        :boxShadow="false"
        :value="value"
        :subfield="prop.subfield"
        :defaultOpen="prop.defaultOpen"
        :toolbarsFlag="prop.toolbarsFlag"
        :editable="prop.editable"
        :scrollStyle="prop.scrollStyle"
        :autofocus="false"
        v-loading="loading"
      ></mavon-editor>
</template>

<script>
import { mavonEditor } from "mavon-editor";
import "mavon-editor/dist/css/index.css";
export default {
  name: "wikidetail",
  components: {
    mavonEditor
  },
  computed: {
    prop() {
      let data = {
        subfield: false, // 单双栏模式
        defaultOpen: "preview", //edit： 默认展示编辑区域 ， preview： 默认展示预览区域
        editable: false,
        toolbarsFlag: false,
        scrollStyle: true
      };
      return data;
    }
  },
  data() {
    return {
      value: "",
    };
  },
  created() {
    this.getdata("std", this.$route.params.wikiid);
  },
  methods: {
    getdata(username, type) {
      this.$axios
        .get("/wiki/?username=" + username + "&type=" + type)
        .then(response => {
          this.value =
            response.data.length > 0 ? response.data[0].value : "# 暂无数据";
          this.loading = false;
        })
        .catch(error => {
          this.$message.error(
            "服务器错误！" + "(" + JSON.stringify(error.response.data) + ")"
          );
        });
    }
  }
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>
