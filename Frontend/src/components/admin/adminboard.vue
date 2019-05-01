<template>
  <el-row>
    <el-table :data="tableData" size="mini">
      <el-table-column prop="username" label="User"></el-table-column>
      <el-table-column prop="classes" label="Class" ></el-table-column>
      <el-table-column prop="number" label="Number"></el-table-column>
      <el-table-column prop="account" label="Account" :width="300"></el-table-column>
      <el-table-column prop="acnum" label="AC" :width="70"></el-table-column>
      <el-table-column prop="submitnum" label="Submit" :width="70"></el-table-column>
      <el-table-column prop="blogaddress" label="BlogAddress" :width="350"></el-table-column>
    </el-table>

    <el-form label-position="right">
      <el-form-item label="请输入要修改或添加的用户名：">
        <el-input
          v-model="username"
          placeholder="请输入要修改或添加的用户名："
          style="width:200px"
          @change="getuser"
          @keyup.native.enter="getuser"
        ></el-input>
      </el-form-item>
      <el-form-item label="班级">
        <el-input v-model="classes" placeholder="班级" style="width:200px"></el-input>
      </el-form-item>
      <el-form-item label="学号">
        <el-input v-model="number" placeholder="学号" style="width:200px"></el-input>
      </el-form-item>
      <el-form-item label="Codeforces账号">
        <el-input v-model="cf" placeholder="请填写Codeforces账号，无则留空" style="width:200px"></el-input>
      </el-form-item>
      <el-form-item label="HDU账号">
        <el-input v-model="hdu" placeholder="请填写HDU账号，无则留空" style="width:200px"></el-input>
      </el-form-item>
      <el-form-item label="Vjudge账号">
        <el-input v-model="vjudge" placeholder="请填写Vjudge账号，无则留空" style="width:200px"></el-input>
      </el-form-item>
      <el-form-item label="LPOJ账号">
        <el-input v-model="lpoj" placeholder="请填写LPOJ账号，无则留空" style="width:200px"></el-input>
      </el-form-item>
      <el-form-item label="博客RSS地址">
        <el-input
          v-model="blog"
          placeholder="请填写RSS地址，如https://blog.csdn.net/lzc504603913/rss/list，博客园也有http://feed.cnblogs.com/blog/u/117633/rss"
          style="width:800px"
        ></el-input>
      </el-form-item>
      <el-button type="danger" @click="deleteuser">删除此用户</el-button>
      <el-button type="primary" @click="submit">提交</el-button>
    </el-form>
  </el-row>
</template>

<script>
export default {
  name: "adminboard",
  data() {
    return {
      username: "",
      cf: "",
      hdu: "",
      vjudge: "",
      lpoj: "",
      blog: "",
      classes: "",
      number: "",
      acnum: "",
      submitnum: "",
      tableData: [],
      isnew: true
    };
  },
  methods: {
    getuser() {
      this.$axios
        .get("/board/" + this.username + "/")
        .then(response => {
          var d = response.data.account;
          var li = d.split("|");
          this.cf = li[0];
          this.hdu = li[1];
          this.vjudge = li[2];
          this.lpoj = li[3];
          this.blog = response.data.blogaddress;
          this.classes = response.data.classes;
          this.number = response.data.number;
          this.acnum = response.data.acnum;
          this.submitnum = response.data.submitnum;
          this.isnew = false;
        })
        .catch(error => {
          this.isnew = true;
        });
    },
    deleteuser() {
      if (this.username == "") return;
      this.$confirm("确定要删除： " + this.username + "  吗？", "确定删除？", {
        confirmButtonText: "确定",
        cancelButtonText: "取消",
        type: "warning"
      }).then(() => {
        this.$axios
          .delete("/board/" + this.username + "/")
          .then(response => {
            this.$message.success("删除成功！");
          })
          .catch(error => {
            this.$message.error(
              "服务器错误！" + "(" + JSON.stringify(error.response.data) + ")"
            );
          });
      });
    },
    submit() {
      this.$confirm(
        "确定要修改或添加： " + this.username + "  吗？",
        "确定要修改或添加？",
        {
          confirmButtonText: "确定",
          cancelButtonText: "取消",
          type: "warning"
        }
      ).then(() => {
        if (this.isnew == false) {
          var acc = "";
          acc = this.cf + "|" + this.hdu + "|" + this.vjudge + "|" + this.lpoj;
          this.$axios
            .put("/board/" + this.username + "/", {
              username: this.username,
              classes: this.classes,
              number: this.number,
              account: acc,
              blogaddress: this.blog
            })
            .then(response => {
              this.$message.success("修改成功！");
            })
            .catch(error => {
              this.$message.error(
                "服务器错误！" + "(" + JSON.stringify(error.response.data) + ")"
              );
            });
        } else {
          var acc = "";
          acc = this.cf + "|" + this.hdu + "|" + this.vjudge + "|" + this.lpoj;
          this.$axios
            .post("/board/", {
              username: this.username,
              classes: this.classes,
              number: this.number,
              account: acc,
              blogaddress: this.blog
            })
            .then(response => {
              this.$message.success("添加成功！");
            })
            .catch(error => {
              this.$message.error(
                "服务器错误！" + "(" + JSON.stringify(error.response.data) + ")"
              );
            });
        }
      });
    }
  },
  mounted() {
    this.$axios
      .get("/board/")
      .then(response => {
        this.tableData = response.data;
      })
      .catch(error => {
        this.$message.error(
          "服务器错误！" + "(" + JSON.stringify(error.response.data) + ")"
        );
      });
  }
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.el-tag + .el-tag {
  margin-left: 10px;
}
</style>
