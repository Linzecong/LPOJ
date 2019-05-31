<template>
  <el-tabs type="border-card" @tab-click="tabClick">
    <el-tab-pane label="Overview">
      <span slot="label">
        <b>
          <i class="el-icon-document"></i> Overview
        </b>
      </span>
      <contestoverview ref="Overview"></contestoverview>
    </el-tab-pane>
    <el-tab-pane label="Problems" :disabled="!haveauth" :lazy="true">
      <span slot="label">
        <b>
          <i class="el-icon-menu"></i> Problems
        </b>
      </span>
      <contestproblem ref="Problems"></contestproblem>
    </el-tab-pane>
    <el-tab-pane label="Submissions">
      <span slot="label">
        <b>
          <i class="el-icon-edit-outline"></i> Submissions
        </b>
      </span>
      <contestsubmit ref="Submissions"></contestsubmit>
    </el-tab-pane>
    <el-tab-pane label="Rankings">
      <span slot="label">
        <b>
          <i class="el-icon-star-on"></i> Rankings
        </b>
      </span>
      <contestrank ref="Rankings"></contestrank>
    </el-tab-pane>

    <el-tab-pane label="Announcements" :disabled="!haveauth">
      <span slot="label">
        <b>
          <el-badge :value="anvalue" :hidden="anvalue==0" style="margin-top:5px"></el-badge>
          <i class="el-icon-bell" v-if="anvalue==0"></i>
          Announcements
        </b>
      </span>
      <contestannounce ref="Announcements"></contestannounce>
    </el-tab-pane>

    <el-tab-pane label="Comments" :disabled="!haveauth">
      <span slot="label">
        <b>
          <i class="el-icon-info"></i> Comments
        </b>
      </span>
      <contestcomment ref="Comments"></contestcomment>
    </el-tab-pane>
    <el-tab-pane label="Tutorial" :disabled="!haveauth">
      <span slot="label">
        <b>
          <i class="el-icon-notebook-1"></i> Tutorial
        </b>
      </span>
      <contesttutorial ref="Tutorial"></contesttutorial>
    </el-tab-pane>
  </el-tabs>
</template>

<script>
import contestoverview from "@/components/contest/contestoverview";
import contestproblem from "@/components/contest/contestproblem";
import contestannounce from "@/components/contest/contestannounce";
import contestsubmit from "@/components/contest/contestsubmit";
import contestrank from "@/components/contest/contestrank";
import contestcomment from "@/components/contest/contestcomment";
import contesttutorial from "@/components/contest/contesttutorial";
export default {
  name: "contestdetail",
  components: {
    contestoverview,
    contestproblem,
    contestannounce,
    contestsubmit,
    contestrank,
    contestcomment,
    contesttutorial
  },
  data() {
    return {
      contestid: this.$route.params.contestID,
      haveauth: false,
      anvalue: 0,
      anlist: []
    };
  },
  created() {
    this.contestid = this.$route.params.contestID;

    this.$axios
      .get("/contestinfo/" + this.contestid + "/")
      .then(response => {
        var auth = response.data.auth;

        var sDate1 = response.data.begintime;

        var date2 = "";
        var date1 = new Date(Date.parse(sDate1));

        this.$axios.get("/currenttime/").then(response2 => {
          date2 = response2.data;

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

          if(sessionStorage.type==2||sessionStorage.type==3){
            this.haveauth = 1;
            return;
          }

          var username = sessionStorage.username;
          if (username) {
            this.$axios
              .get(
                "/contestregister/?user=" +
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
        this.$message.error(
          "服务器错误！" + JSON.stringify(error.response.data)
        );
        return;
      });
  },
  mounted() {
    this.$store.state.antimer = setInterval(this.getan, 120000);
    this.getan()
  },
  destroyed() {
    clearInterval(this.$store.state.antimer);
  },
  methods: {
    getan() {
      this.$axios
        .get("/contestannouncement/?contestid=" + this.$route.params.contestID)
        .then(response => {
          this.anvalue = response.data.length;
          for (let i = 0; i < response.data.length; i++) {
            let flag = false;
            for (let j = 0; j < this.anlist.length; j++) {
              if (this.anlist[j] == response.data[i]["announcement"])
                flag = true;
            }
            if (flag == false) {
              this.anlist.push(response.data[i]["announcement"]);
                this.$notify.warning({
                  dangerouslyUseHTMLString: true,
                  title: "提示",
                  message: response.data[i]["announcement"],
                  duration: 7000
                });
            }
          }
        });
    },

    tabClick(tab) {
      //console.log(tab);
      // if (tab.label == "Problems")
      //   this.$refs.Problems.getproblem(this.$route.params.contestID);

      if (tab.label == "Submissions") {
        this.$refs.Submissions.$children[0].creattimer();
      } else {
        clearInterval(this.$store.state.timer);
      }

      if (tab.label == "Rankings") {
        this.$refs.Rankings.setproblemcount(this.$route.params.contestID);
      }

      if (tab.label == "Announcements") {
        this.$refs.Announcements.reflash();
      }

      if (tab.label == "Comments") {
        this.$refs.Comments.reflash(this.$route.params.contestID);
      }
      if (tab.label == "Tutorial") {
        this.$refs.Tutorial.reflash(this.$route.params.contestID);
      }
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
