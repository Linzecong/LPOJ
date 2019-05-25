<template>
  <el-card>
    <p :key="index" v-for="(item,index) in tabledata" v-html="item"/>

    <el-form label-position="right" v-if="isadmin">
      <el-form-item label="Announcement：">
        <el-input
          type="textarea"
          v-model="anvalue"
          autosize
          style="width:700px"
          @keyup.native.enter="anClick"
        ></el-input>
      </el-form-item>
      <el-button @click="anClick">{{label.send}}</el-button>
    </el-form>
  </el-card>
</template>

<script>
export default {
  name: "contestannounce",
  data() {
    return {
      label:{
        send:"Send"
      },
      tabledata: [],
      isadmin: false,
      anvalue: ""
    };
  },
  created() {
    this.isadmin = sessionStorage.type == 2 || sessionStorage.type == 3;
  },
  methods: {
    anClick() {
      this.$confirm("确定提交吗？", "提交", {
        confirmButtonText: "确定",
        cancelButtonText: "取消",
        type: "warning"
      }).then(() => {
        this.$axios
          .post("/contestannouncement/", {
            contestid: this.$route.params.contestID,
            announcement: this.anvalue
          })
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
      this.tabledata = [];
      this.$axios
        .get("/contestannouncement/?contestid=" + this.$route.params.contestID)
        .then(response => {
          for (let i = 0; i < response.data.length; i++) {
            this.tabledata.push(response.data[i]["announcement"]);
          }
        })
        .catch(error => {
          this.$message.error(
            "服务器出错！" + JSON.stringify(error.response.data)
          );
        });
    }
  }
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>
