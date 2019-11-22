<template>
  <el-card>
    <el-table :data="tableData" style="width: 100%" :row-style="ratingcolor">
      <el-table-column type="expand" label="Expand Comment" :width="150">
        <template slot-scope="props">
          <span>{{ props.row.huifu }}</span>
        </template>
      </el-table-column>
      <el-table-column label="ID" prop="id" v-if="isadmin" :width="50"></el-table-column>
      <el-table-column label="User" prop="user"></el-table-column>
      <el-table-column label="Title" prop="title"></el-table-column>
      <el-table-column label="Problem" prop="problem"></el-table-column>
      <el-table-column label="Message" prop="message"></el-table-column>
      <el-table-column label="Time" prop="time"></el-table-column>
    </el-table>
    <br>
    <br>
    <el-form ref="contestcomment" :model="contestcomment" label-position="right">
      <el-form-item label="Title：">
        <el-input v-model="contestcomment.title" style="width:700px"></el-input>
      </el-form-item>
      <el-form-item label="Problem Number：">
        <el-select v-model="contestcomment.problem" placeholder="Choose Problem">
          <el-option v-for="(index,K) in pros" :key="K" :label="index" :value="index"></el-option>
        </el-select>
      </el-form-item>
      <el-form-item label="Question：">
        <el-input
          type="textarea"
          v-model="contestcomment.message"
          autosize
          style="width:700px"
          @keyup.native.enter="commentClick"
        ></el-input><el-button @click="commentClick" type="primary" style="margin-left:10px;" size="small">Send</el-button>
      </el-form-item>
      
    </el-form>
    <br>
    <br>
    <el-form label-position="right" v-if="isadmin">
      <el-form-item label="Question Number">
        <el-input v-model="commentid" style="width:700px"></el-input>
      </el-form-item>

      <el-form-item label="Reply：">
        <el-input type="textarea" v-model="commentmessage" autosize style="width:700px"></el-input>
      </el-form-item>
      <el-button @click="huifuClick">Reply</el-button>
    </el-form>
  </el-card>
</template>

<script>
import moment from "moment";
export default {
  name: "contestcomment",
  data() {
    return {
      commentid: "",
      commentmessage: "",
      isadmin: false,
      tableData: [],
      pros: [],
      contestcomment: {
        contestid: this.$route.params.contestID,
        user: sessionStorage.username,
        title: "",
        message: "",
        problem: "",
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
    huifuClick() {
      this.$confirm("确定回复吗？", "回复", {
        confirmButtonText: "确定",
        cancelButtonText: "取消",
        type: "warning"
      }).then(() => {
        this.$axios
          .get("/contestcomment/" + this.commentid + "/")
          .then(response => {
            response.data.huifu = this.commentmessage;
            this.$axios
              .put("/contestcomment/" + this.commentid + "/", response.data)
              .then(response2 => {
                this.$message.success("提交成功！");
                this.reflash();
              })
              .catch(error => {
                this.$message.error(
                  "服务器出错！" + JSON.stringify(error.response.data)
                );
              });
          })
          .catch(error => {
            this.$message.error(
              "服务器出错！" + JSON.stringify(error.response.data)
            );
          });
      });
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
        .get("/contestcomment/?contestid=" + this.$route.params.contestID)
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
    this.isadmin = sessionStorage.type == 2 || sessionStorage.type == 3;

    this.pros.push("ALL");
    for (var i = 65; i < 65 + 26; i++) {
      this.pros.push(String.fromCharCode(i));
    }
    this.reflash()
  }
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
h1 {
  position: relative;
}
</style>
