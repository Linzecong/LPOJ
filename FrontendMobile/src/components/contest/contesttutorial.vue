<template>
  <el-card>
    <mavon-editor
      :boxShadow="false"
      :value="value"
      :subfield="prop.subfield"
      :defaultOpen="prop.defaultOpen"
      :toolbarsFlag="prop.toolbarsFlag"
      :editable="prop.editable"
      :scrollStyle="prop.scrollStyle"
      :autofocus="false"
    ></mavon-editor>
    <br>
    <el-table :data="tableData" style="width: 100%" :row-style="ratingcolor">
      <el-table-column type="expand" label="Expand Comment" :width="150">
        <template slot-scope="props">
          <span>{{ props.row.huifu }}</span>
        </template>
      </el-table-column>
      <el-table-column label="User" prop="user" :width="200"></el-table-column>
      <el-table-column label="Message" prop="message"></el-table-column>
      <el-table-column label="Time" prop="time"></el-table-column>
    </el-table>
    <br>
    <br>
    <el-form ref="contestcomment" :model="contestcomment" label-position="right">
      <el-form-item label="Comment：">
        <el-input
          type="textarea"
          v-model="contestcomment.message"
          autosize
          style="width:700px"
          @keyup.native.enter="commentClick"
        ></el-input>
        <el-button @click="commentClick" type="primary" style="margin-left:10px;" size="small">Send</el-button>
      </el-form-item>
    </el-form>
  </el-card>
</template>

<script>
import moment from "moment";
import { mavonEditor } from "mavon-editor";
import "mavon-editor/dist/css/index.css";
export default {
  name: "contesttutorial",
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
      tableData: [],
      value: "暂无数据！",
      contestcomment: {
        contestid: this.$route.params.contestID,
        user: sessionStorage.username,
        title: "Tutorial",
        message: "",
        problem: "ALL",
        rating: parseInt(sessionStorage.rating)
      }
    };
  },
  methods: {
    ratingcolor({ row, rowIndex }) {
      if (row.rating >= 3000) return "color:red;font-weight: bold;";
      if (row.rating >= 2600) return "color:#BB5E00;font-weight: bold;";
      if (row.rating >= 2200) return "color:#E6A23C;font-weight: bold;";
      if (row.rating >= 2050) return "color:#930093;font-weight: bold;";
      if (row.rating >= 1900) return "color:#0000AA;font-weight: bold;";
      if (row.rating >= 1700) return "color:#007799;font-weight: bold;";
      if (row.rating >= 1500) return "color:#227700;font-weight: bold;";
      if (row.rating >= 1350) return "color:#67C23A;font-weight: bold;";
      if (row.rating >= 1200) return "color:#909399;font-weight: bold;";
      return "color:#303133;font-weight: bold;";
    },

    commentClick() {
      this.$confirm("确定提交吗？", "提交", {
        confirmButtonText: "确定",
        cancelButtonText: "取消",
        type: "warning"
      }).then(() => {
        if (this.contestcomment.user == "") {
          this.$message.error("请先登录！");
          return;
        }
        this.$axios
          .post("/contestcomment/", this.contestcomment)
          .then(response => {
            this.$message.success("提交成功！");
            this.reflash();
          })
          .catch(error => {
            this.$message.error(
              "服务器出错！" + JSON.stringify(error.response.data)
            );
          });
      });
    },
    reflash() {
      this.$axios
        .get("/contesttutorial/?contestid=" + this.$route.params.contestID)
        .then(response => {
          if (response.data.length > 0) this.value = response.data[0].value;
        })
        .catch(error => {
          this.$message.error(
            "服务器出错！" + JSON.stringify(error.response.data)
          );
        });

      this.$axios
        .get("/contestcomment/?problem=ALL&contestid=" + this.$route.params.contestID)
        .then(response => {
          for (let i = 0; i < response.data.length; i++) {
            response.data[i].time = moment(response.data[i].time).format(
              "YYYY-MM-DD HH:mm:ss"
            );
          }

          this.tableData = response.data;
        })
        .catch(error => {
          this.$message.error(
            "服务器出错！" + JSON.stringify(error.response.data)
          );
        });
    }
  },
  created() {
    this.reflash();
  }
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
h1 {
  position: relative;
}
</style>
