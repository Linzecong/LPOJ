<template>
  <el-tabs type="border-card" v-show="canshow" v-loading="loading">
    <el-tab-pane label="添加题目">
      <adminaddproblem></adminaddproblem>
    </el-tab-pane>

    <el-tab-pane label="添加比赛"><adminaddcontest></adminaddcontest></el-tab-pane>
    <el-tab-pane label="题目修改"><adminchangepro></adminchangepro></el-tab-pane>
    <el-tab-pane label="比赛设置"><adminchangecontest></adminchangecontest></el-tab-pane>
    <el-tab-pane label="管理用户" :disabled="!isadmin"><adminmanageuser></adminmanageuser></el-tab-pane>
    <el-tab-pane label="Rejudge" :disabled="!isadmin"><adminrejudge></adminrejudge></el-tab-pane>
    <el-tab-pane label="添加与修改训练" :disabled="!isadmin"><admintrainning></admintrainning></el-tab-pane>
  </el-tabs>
</template>

<script>
import adminaddproblem from "@/components/admin/adminaddproblem";
import adminaddcontest from "@/components/admin/adminaddcontest";
import adminchangepro from "@/components/admin/adminchangepro";
import adminchangecontest from "@/components/admin/adminchangecontest";
import adminmanageuser from "@/components/admin/adminmanageuser";
import adminrejudge from "@/components/admin/adminrejudge";
import admintrainning from "@/components/admin/admintrainning";
export default {
  name: "admin",
  components: {
    adminaddproblem,
    adminaddcontest,
    adminchangepro,
    adminchangecontest,
    adminmanageuser,
    adminrejudge,
    admintrainning
  },
  data() {
    return {
      type: 1,
      isadmin: false,
      canshow: false,
      loading:true
    };
  },
  methods: {

  },
  created() {
    this.type = localStorage.type;
    if (this.type != 2 && this.type != 3) {
      this.$message.error("非法访问！");
      this.canshow = false;
      return;
    }
    this.canshow = true;
    if (this.type == 3) {
      this.isadmin = true;
    }
  },
  mounted() {
    this.loading=false
  },
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
h1 {
  position: relative;
}
</style>
