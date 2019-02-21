<template>
  <el-card>
    <el-row :gutter="10">
      <center>
        <h1>{{ title }}</h1>
        <el-rate v-model="level" disabled text-color="#409EFF" score-template="{value}"></el-rate>
      </center>
    </el-row>

    <el-row :gutter="10">
      <center>
        <h2>{{ des }}</h2>
      </center>
    </el-row>

    <el-row :gutter="10">
      <center>
        <h1 :id="timestyle">{{ lefttime }}</h1>
      </center>
    </el-row>

    <el-row :gutter="10">
      <center>
        <el-table :data="tableData">
          <el-table-column prop="begintime" label="Begin Time"></el-table-column>
          <el-table-column prop="endtime" label="End Time"></el-table-column>
          <el-table-column prop="type" label="Type"></el-table-column>
          <el-table-column prop="creator" label="Owner"></el-table-column>
        </el-table>
      </center>
    </el-row>
    <el-row :gutter="10">
      <center>
        <h2 style="color:#409EFF">{{ note }}</h2>
      </center>
    </el-row>
  </el-card>
</template>

<script>
import moment from "moment";
export default {
  name: "contestoverview",
  data() {
    return {
      level: 3,
      id: this.$route.params.contestID,
      tableData: [],
      title: 404,
      level: 404,
      des: 404,
      note: 404,
      lefttime: 0,
      timestyle: "wait",
      left: 0,
      lasttime:0,
    };
  },
  methods: {
    refresh(id) {
      this.$http
        .get(
          "http://" + this.$ip + ":" + this.$port + "/contestinfo/" + id + "/"
        )
        .then(response => {
          this.title = response.data.title;
          this.level = response.data.level;
          this.des = response.data.des;
          this.note = response.data.note;
          var sDate1 = response.data.begintime;

          var date2 = "";
          var date1 = new Date(Date.parse(sDate1));

          this.$http
            .get("http://quan.suning.com/getSysTime.do")
            .then(response2 => {
              date2 = response2.data.sysTime2;

              this.left = parseInt(
                (new Date(Date.parse(date2)).getTime() - date1.getTime()) / 1000
              );

              if (this.left < 0) this.timestyle = "wait";
              else this.timestyle = "begin";

              this.lasttime=response.data.lasttime
              if (this.left >= response.data.lasttime) {
                this.left = response.data.lasttime;
                this.timestyle = "end";
              }

              var t = Math.abs(this.left);

              this.lefttime =
                parseInt(t / 60 / 60) +
                ":" +
                parseInt((t / 60) % 60) +
                ":" +
                parseInt((t % 60) % 60);

              response.data.begintime = moment(response.data.begintime).format(
                "YYYY-MM-DD HH:mm:ss"
              );
              response.data.endtime = moment(
                date1.getTime() + response.data.lasttime * 1000
              ).format("YYYY-MM-DD HH:mm:ss");

              this.tableData = [response.data];
            });
        });
    },
    refreshtime() {
      this.left++;

      if (this.left < 0) this.timestyle = "wait";
      else this.timestyle = "begin";

      if (this.left >= this.lasttime) {
        this.left = this.lasttime;
        this.timestyle = "end";
      }

      var t = Math.abs(this.left);

      this.lefttime =
        parseInt(t / 60 / 60) +
        ":" +
        parseInt((t / 60) % 60) +
        ":" +
        parseInt((t % 60) % 60);
    }
  },
  destroyed() {
    clearInterval(this.$store.state.contesttimer);
  },
  created() {
    this.refresh(this.$route.params.contestID);
    this.$store.state.contesttimer = setInterval(this.refreshtime, 1000);
  }
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
h1 {
  position: relative;
}
#wait {
  color: #909399;
}
#begin {
  color: #67c23a;
}
#end {
  color: #e6a23c;
}
</style>
