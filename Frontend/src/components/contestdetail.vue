<template>
  <el-tabs type="border-card" @tab-click="tabClick">
    <el-tab-pane label="Overview">
      <span slot="label">
        <i class="el-icon-document"></i> Overview
      </span>
      <contestoverview ref="Overview"></contestoverview>
    </el-tab-pane>
    <el-tab-pane label="Problems" :disabled="!haveauth">
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
    <!-- <el-tab-pane label="Announcements" :disabled="!haveauth">
      <span slot="label">
        <i class="el-icon-bell"></i> Announcements
      </span>
      <contestannounce ref="Announcements"></contestannounce>
    </el-tab-pane>
    <el-tab-pane label="Comments" :disabled="!haveauth">
      <span slot="label">
        <i class="el-icon-info"></i> Comments
      </span>
      <contestcomment ref="Comments"></contestcomment>
    </el-tab-pane> -->
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
    contestoverview,
    contestproblem,
    contestannounce,
    contestsubmit,
    contestrank,
    contestcomment
  },
  data() {
    return {
      contestid: this.$route.params.contestID,
      haveauth: false
    };
  },
  created() {
    this.contestid = this.$route.params.contestID;

    this.$axios
      .get(
        "/api/contestinfo/" +
          this.contestid +
          "/"
      )
      .then(response => {
        var auth = response.data.auth;

        var sDate1 = response.data.begintime;

        var date2 = "";
        var date1 = new Date(Date.parse(sDate1));

        this.$axios
          .get("http://quan.suning.com/getSysTime.do")
          .then(response2 => {
            date2 = response2.data.sysTime2;

            var left = parseInt(
              (new Date(Date.parse(date2)).getTime() - date1.getTime()) / 1000
            );
            if (left >= response.data.lasttime) {
              auth = "1";
            }
            if (auth == "1") {
              this.haveauth = 1;
              this.$refs.Overview.haveauth = 1;
              return;
            }
            var username = sessionStorage.username;
            if (username) {
              this.$axios
                .get(
                  "/api/contestregister/?user=" +
                    username +
                    "&contestid=" +
                    this.contestid
                )
                .then(response => {
                  if (response.data.length > 0) {
                    this.haveauth = 1;
                    this.$refs.Overview.haveauth = 1;
                  }
                });
            }
          });
      })
      .catch(error => {
        this.$message.error("服务器错误！" + error);
        return;
      });
  },
  methods: {
    tabClick(tab) {
      console.log(tab);
      // if (tab.label == "Problems")
      //   this.$refs.Problems.getproblem(this.$route.params.contestID);

      // if (tab.label == "Overview")
      //   this.$refs.Overview.refresh(this.$route.params.contestID);
      
      if (tab.label == "Rankings")
        this.$refs.Rankings.setproblemcount(this.$route.params.contestID);
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
