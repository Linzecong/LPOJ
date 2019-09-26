<template>
  <el-row>
    <el-row>
      <el-form label-position="right">
        <el-form-item label="标题与介绍">
          <el-input v-model="title" placeholder="修改或添加的标题" style="width:200px" @change="change"></el-input>
          <el-input v-model="des" placeholder="训练说明" style="width:500px"></el-input>
        </el-form-item>
        <el-form-item label="教程链接">
          <el-input v-model="tips" placeholder="| 号隔开，如 intro_index|dp_index" style="width:200px"></el-input>

          <el-select
            placeholder="选择教程"
            @keyup.native.enter="addtype"
            v-model="curtype"
            filterable
            style="width:200px"
          >
            <algorithmselect></algorithmselect>
          </el-select>
          <el-button type="primary" @click="addtype">添加教程</el-button>
        </el-form-item>
        <el-form-item label="分组与序号">
          <el-input v-model="group" placeholder="1,2,3,4" style="width:200px"></el-input>
          <el-input v-model="num" placeholder="1,2,3,4" style="width:500px"></el-input>
        </el-form-item>
        <el-form-item label="题号">
          <el-input v-model="problem" placeholder="1,2,3,4" style="width:200px"></el-input>
          <el-button type="primary" @click="click">提交</el-button>
        </el-form-item>
      </el-form>
    </el-row>
  </el-row>
</template>

<script>
import algorithmselect from "@/components/utils/algorithmselect";
export default {
  name: "adminrejudge",
  components: {
    algorithmselect
  },
  data() {
    return {
      title: "",
      des: "",
      tips: "",
      group: "",
      num: "",
      problem: "",
      curtype: ""
    };
  },
  methods: {
    addtype() {
      if (this.tips == "") this.tips = this.curtype;
      else this.tips += "|" + this.curtype;
    },
    click() {
      this.$axios
        .get("/trainning/?title=" + this.title)
        .then(response => {
          if (response.data.length == 0) {
            this.$axios
              .post("/trainning/", {
                title: this.title,
                des: this.des,
                tips: this.tips,
                group: this.group,
                num: this.num,
                problem: this.problem
              })
              .then(res => {
                this.$message.success("提交成功！");
              })
              .catch(error => {
                this.$message.error(
                  "服务器错误！" +
                    "(" +
                    JSON.stringify(error.response.data) +
                    ")"
                );
              });
          } else {
            this.$axios
              .put("/trainning/" + response.data[0].id + "/", {
                title: this.title,
                des: this.des,
                tips: this.tips,
                group: this.group,
                num: this.num,
                problem: this.problem
              })
              .then(res => {
                this.$message.success("覆盖成功！");
              })
              .catch(error => {
                this.$message.error(
                  "服务器错误！" +
                    "(" +
                    JSON.stringify(error.response.data) +
                    ")"
                );
              });
          }
        })
        .catch(error => {
          this.$message.error(
            "服务器错误！" + "(" + JSON.stringify(error.response.data) + ")"
          );
        });
    },
    change() {
      this.$axios
        .get("/trainning/?title=" + this.title)
        .then(response => {
          if (response.data.length > 0) {
            this.title = response.data[0].title;
            this.des = response.data[0].des;
            this.tips = response.data[0].tips;
            this.group = response.data[0].group;
            this.num = response.data[0].num;
            this.problem = response.data[0].problem;
          }
        })
        .catch(error => {
          this.$message.error(
            "服务器错误！" + "(" + JSON.stringify(error.response.data) + ")"
          );
        });
    }
  },
  created() {}
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.el-tag + .el-tag {
  margin-left: 10px;
}
</style>
