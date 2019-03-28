<template>
  <el-tabs type="border-card" v-show="canshow">
    <el-tab-pane label="添加题目">
      <adminaddproblem></adminaddproblem>
    </el-tab-pane>

    <el-tab-pane label="添加比赛"><adminaddcontest></adminaddcontest></el-tab-pane>
    <el-tab-pane label="题目修改"><adminchangepro></adminchangepro></el-tab-pane>
    <el-tab-pane label="比赛设置"><adminchangecontest></adminchangecontest></el-tab-pane>
    <el-tab-pane label="管理用户" :disabled="!isadmin"><adminmanageuser></adminmanageuser></el-tab-pane>
  </el-tabs>
</template>

<script>
import adminaddproblem from "@/components/adminaddproblem";
import adminaddcontest from "@/components/adminaddcontest";
import adminchangepro from "@/components/adminchangepro";
import adminchangecontest from "@/components/adminchangecontest";
import adminmanageuser from "@/components/adminmanageuser";
export default {
  name: "admin",
  components: {
    adminaddproblem,
    adminaddcontest,
    adminchangepro,
    adminchangecontest,
    adminmanageuser
  },
  data() {
    return {
      type: 1,
      isadmin: false,
      canshow: false,
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
  }
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
h1 {
  position: relative;
}
</style>
