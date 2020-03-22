<template>
  <el-tabs type="border-card"
           v-show="canshow"
           v-loading="loading">
    
    <el-tab-pane label="添加题目">
      <adminaddproblem></adminaddproblem>
    </el-tab-pane>

    <el-tab-pane label="添加选择题">
      <adminaddchoiceproblem></adminaddchoiceproblem>
    </el-tab-pane>

    <el-tab-pane label="添加比赛"
                 :lazy="true">
      <adminaddcontest></adminaddcontest>
    </el-tab-pane>
    <el-tab-pane label="题目列表"
                 :lazy="true">
      <adminchangepro></adminchangepro>
    </el-tab-pane>

    <el-tab-pane label="选择题列表"
                 :lazy="true">
      <adminchangechoiceproblem></adminchangechoiceproblem>
    </el-tab-pane>

    <el-tab-pane label="比赛列表"
                 :lazy="true">
      <adminchangecontest></adminchangecontest>
    </el-tab-pane>
    <el-tab-pane label="用户列表"
                 :disabled="!isadmin"
                 :lazy="true">
      <adminmanageuser></adminmanageuser>
    </el-tab-pane>
    <el-tab-pane label="Rejudge"
                 :disabled="!isadmin"
                 :lazy="true">
      <adminrejudge></adminrejudge>
    </el-tab-pane>
    <el-tab-pane label="添加与修改训练"
                 :disabled="!isadmin"
                 :lazy="true">
      <admintrainning></admintrainning>
    </el-tab-pane>
    <el-tab-pane label="爬虫信息管理"
                 :disabled="!isadmin"
                 :lazy="true">
      <adminboard></adminboard>
    </el-tab-pane>
    <el-tab-pane label="班级管理"
                 :lazy="true">
      <adminclassmanage></adminclassmanage>
    </el-tab-pane>
    <el-tab-pane label="网站设置"
                 :disabled="!isadmin"
                 :lazy="true">
      <adminsetting></adminsetting>
    </el-tab-pane>
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
import adminboard from "@/components/admin/adminboard";
import adminsetting from "@/components/admin/adminsetting";
import adminclassmanage from "@/components/admin/adminclassmanage";
import adminaddchoiceproblem from "@/components/admin/adminaddchoiceproblem";
import adminchangechoiceproblem from "@/components/admin/adminchangechoiceproblem";

export default {
  name: "admin",
  components: {
    adminaddproblem,
    adminaddcontest,
    adminchangepro,
    adminchangecontest,
    adminmanageuser,
    adminrejudge,
    admintrainning,
    adminboard,
    adminsetting,
    adminclassmanage,
    adminaddchoiceproblem,
    adminchangechoiceproblem,
  },
  data () {
    return {
      type: 1,
      isadmin: false,
      canshow: false,
      loading: true
    };
  },
  methods: {

  },
  created () {
    this.type = sessionStorage.type;
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
  mounted () {
    this.loading = false
  },
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
h1 {
  position: relative;
}
</style>
