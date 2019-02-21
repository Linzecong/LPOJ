<template>
  <el-tabs type="border-card" @tab-click="tabClick">
    <el-tab-pane label="Overview">
      <span slot="label">
        <i class="el-icon-document"></i> Overview
      </span>
      <contestoverview ref="Overview"></contestoverview>
    </el-tab-pane>
    <el-tab-pane label="Problems">
      <span slot="label">
        <i class="el-icon-menu"></i> Problems
      </span>
      <contestproblem ref="Problems"></contestproblem>
    </el-tab-pane>
    <el-tab-pane label="Submissions" :lazy="true">
      <span slot="label">
        <i class="el-icon-edit-outline"></i> Submissions
      </span>
      <contestsubmit ref="Submissions"></contestsubmit>
    </el-tab-pane>
    <el-tab-pane label="Rankings">
      <span slot="label">
        <i class="el-icon-star-on"></i> Rankings
      </span>
      <contestrank ref="Rankings"></contestrank>
    </el-tab-pane>
    <el-tab-pane label="Announcements">
      <span slot="label">
        <i class="el-icon-bell"></i> Announcements
      </span>
      <contestannounce ref="Announcements"></contestannounce>
    </el-tab-pane>
    <el-tab-pane label="Comments">
      <span slot="label">
        <i class="el-icon-info"></i> Comments
      </span>
      <contestcomment ref="Comments"></contestcomment>
    </el-tab-pane>
  </el-tabs>
</template>

<script>
import contestoverview from "@/components/contestoverview";
import contestproblem from "@/components/contestproblem";
import contestannounce from "@/components/contestannounce";
import contestsubmit from "@/components/contestsubmit";
import contestrank from "@/components/contestrank";
import contestcomment from "@/components/contestcomment";
export default {
  name: "contestdetail",
  components: {
    contestoverview,contestproblem,contestannounce,contestsubmit,contestrank,contestcomment
  },
  data() {
    return {
      msg: this.$route.params.contestID
    };
  },
  methods: {
    tabClick(tab) {
      console.log(tab)
      if(tab.label=="Problems")
        this.$refs.Problems.getproblem(this.$route.params.contestID);
      
      if(tab.label=="Overview")
        this.$refs.Overview.refresh(this.$route.params.contestID);

      
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
