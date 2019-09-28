<template>
  <mu-container>
    <mu-card>
      <mu-card-text>
    <mu-tabs :value.sync="curactive" @change="tabClick" inverse color="secondary" text-color="rgba(0, 0, 0, .54)" center>
      <mu-tab>Overview</mu-tab>
      <mu-tab>Submissions</mu-tab>
      <mu-tab>Rankings</mu-tab>
    </mu-tabs>
    <br>
    <contestoverview ref="Overview" v-show="curactive==0"></contestoverview>

    <contestsubmit ref="Submissions" v-show="curactive==1"></contestsubmit>

    <contestrank ref="Rankings" v-show="curactive==2"></contestrank>
      </mu-card-text>
    </mu-card>
  </mu-container>
</template>

<script>
import contestoverview from "@/components/contest/contestoverview";
import contestsubmit from "@/components/contest/contestsubmit";
import contestrank from "@/components/contest/contestrank";
export default {
  name: "contestdetail",
  components: {
    contestoverview,
    contestsubmit,
    contestrank,
  },
  data() {
    return {
      contestid: this.$route.params.contestID,
      haveauth: false,
      anvalue: 0,
      anlist: [],
      curactive: 0
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

          if (sessionStorage.type == 2 || sessionStorage.type == 3) {
            this.haveauth = 1;
            return;
          }

        });
      })
      .catch(error => {
        this.$toast.error(
          "服务器错误！" + JSON.stringify(error.response.data)
        );
        return;
      });
  },
  mounted() {
    
  },
  destroyed() {
  },
  methods: {

    tabClick(tab) {
      //console.log(tab);
      // if (tab.label == "Problems")
      //   this.$refs.Problems.getproblem(this.$route.params.contestID);
      if (tab == 1) {
        this.$refs.Submissions.$children[0].creattimer();
      } else {
        clearInterval(this.$store.state.timer);
      }
      if (tab == 2) {
        this.$refs.Rankings.setproblemcount(this.$route.params.contestID);
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
