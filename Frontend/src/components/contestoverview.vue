<template>
  <el-card>
    <el-row :gutter="10">
      <center>
        <h1>{{ title }}</h1>
        <el-rate v-model="level" disabled text-color="#409EFF" score-template="{value}"></el-rate>
        <el-button
          plain
          round
          :type="contestauth(auth)"
          @click="register"
          style="margin:30px;"
          :foucs="false"
        >
          <b>{{ auth }}</b>
        </el-button>
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
        <h2 style="color:#409EFF">{{ note }}</h2>
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
    <el-row :gutter="10" v-show="showp">
      <h3>Participant:</h3>
    </el-row>
    <el-row :gutter="10" v-show="showp">
      <el-table
        :stripe="true"
        style="width: 100%"
        :data="tableData2"
        @cell-click="userclick"
        :default-sort="{prop: 'rating', order: 'descending'}"
      >
        <el-table-column prop="user" label="UserID"></el-table-column>
        <el-table-column prop="rating" label="Rating"></el-table-column>
      </el-table>
      <el-pagination
        @size-change="handleSizeChange"
        @current-change="handleCurrentChange"
        :current-page="currentpage"
        :page-sizes="[10, 20, 30, 50]"
        :page-size="pagesize"
        layout="total, sizes, prev, pager, next, jumper"
        :total="totaluser"
      ></el-pagination>
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
      left: -100,
      lasttime: 0,

      auth: 404,

      currentpage: 1,
      pagesize: 10,
      totaluser: 10,
      tableData2: [],

      haveauth: 0,
      type: "1",
      showp: true
    };
  },
  methods: {
    userclick: function(row, column, cell, event) {
      this.$router.push({
        name: "user",
        query: { username: row.user }
      });
    },
    handleSizeChange(val) {
      this.pagesize = val;

      this.$axios
        .get(
          "http://" +
            this.$ip +
            ":" +
            this.$port +
            "/contestregister/?limit=" +
            this.pagesize +
            "&offset=" +
            (this.currentpage - 1) * this.pagesize +
                    "&contestid=" +
                    this.id
        )
        .then(response => {
          this.tableData2 = response.data.results;
          this.totaluser = response.data.count;
        })
        .catch(error => {
          this.$message.error("服务器错误！" + "(" + error + ")");
        });
    },
    handleCurrentChange(val) {
      this.currentpage = val;
      this.$axios
        .get(
          "http://" +
            this.$ip +
            ":" +
            this.$port +
            "/contestregister/?limit=" +
            this.pagesize +
            "&offset=" +
            (this.currentpage - 1) * this.pagesize +
                    "&contestid=" +
                    this.id
        )
        .then(response => {
          this.tableData2 = response.data.results;
          this.totaluser = response.data.count;
        })
        .catch(error => {
          this.$message.error("服务器错误！" + "(" + error + ")");
        });
    },
    register() {
      if (this.type == "1") {
        this.$message({
          message: "公共比赛无需注册！",
          type: "success"
        });
        return;
      }
      if (this.type == "2") {
        this.$message.error("私有比赛，无法注册！");
        return;
      }
      if (this.haveauth) {
        this.$message({
          message: "你已注册！",
          type: "success"
        });
        return;
      }
      var username = sessionStorage.username;
      if (!username) {
        this.$message.error("请先登录！");
        return;
      } else {
        this.$confirm(
          "确定注册吗？比赛时间为：" + this.tableData[0].begintime,
          "提示",
          {
            confirmButtonText: "确定",
            cancelButtonText: "取消",
            type: "warning"
          }
        ).then(() => {
          this.$axios
            .post(
              "http://" + this.$ip + ":" + this.$port + "/contestregister/",
              {
                contestid: this.id,
                user: sessionStorage.username,
                rating: sessionStorage.rating
              }
            )
            .then(res => {
              this.$message({
                message: "注册比赛成功！",
                type: "success"
              });

              this.$router.go(0);
            })
            .catch(error => {
              this.$message.error("服务器错误！" + error);
              return;
            });
        });
      }
    },
    contestauth: function(type) {
      if (type == "Public") return "success";
      if (type == "Protect(Click to register)" || type == "Protect")
        return "warning";
      if (type == "Private") return "danger";
    },
    refresh(id) {
      this.$axios
        .get(
          "http://" + this.$ip + ":" + this.$port + "/contestinfo/" + id + "/"
        )
        .then(response => {
          this.type = response.data["auth"];
          if (response.data["auth"] == "1") {
            response.data["auth"] = "Public";
            this.showp = false;
          }
          if (response.data["auth"] == "2") response.data["auth"] = "Private";
          if (response.data["auth"] == "0") {
            if (this.haveauth == 0)
              response.data["auth"] = "Protect(Click to register)";
            else response.data["auth"] = "Protect";
          }

          this.auth = response.data["auth"];
          this.title = response.data.title;
          this.level = response.data.level;
          this.des = response.data.des;
          this.note = response.data.note;
          var sDate1 = response.data.begintime;

          var date2 = "";
          var date1 = new Date(Date.parse(sDate1));

          this.$axios
            .get("http://quan.suning.com/getSysTime.do")
            .then(response2 => {
              date2 = response2.data.sysTime2;

              this.left = parseInt(
                (new Date(Date.parse(date2)).getTime() - date1.getTime()) / 1000
              );

              if (this.left < 0) this.timestyle = "wait";
              else this.timestyle = "begin";

              this.lasttime = response.data.lasttime;
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
              this.$axios
                .get(
                  "http://" +
                    this.$ip +
                    ":" +
                    this.$port +
                    "/contestregister/?limit=" +
                    this.pagesize +
                    "&offset=" +
                    (this.currentpage - 1) * this.pagesize +
                    "&contestid=" +
                    this.id
                )
                .then(response => {
                  this.tableData2 = response.data.results;
                  this.totaluser = response.data.count;
                })
                .catch(error => {
                  this.$message.error("服务器错误！" + "(" + error + ")");
                });
            });
        });
    },
    refreshtime() {
      if (this.auth != "Public" && this.auth != "Private") {
        if (this.haveauth == 0) this.auth = "Protect(Click to register)";
        else this.auth = "Protect";
      }

      this.left++;

      if(this.left==0){
        this.$router.go(0);
      }

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
