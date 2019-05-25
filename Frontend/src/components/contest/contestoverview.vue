<template>
  <el-card>
    <el-dialog :visible.sync="clonedialogVisible">
      <el-form :model="addcontestform" label-position="right">
        <el-form-item label="比赛名称：">
          <el-input v-model="addcontestform.title"></el-input>
        </el-form-item>
        <el-form-item label="比赛描述：">
          <el-input type="textarea" v-model="addcontestform.des" autosize style="width:500px;"></el-input>
        </el-form-item>
        <el-form-item label="比赛提示：">
          <el-input type="textarea" v-model="addcontestform.note" autosize style="width:500px;"></el-input>
        </el-form-item>
        <el-form-item label="比赛时间：">
          <el-date-picker
            v-model="addcontestform.timerange"
            type="datetimerange"
            align="right"
            start-placeholder="开始日期"
            end-placeholder="结束日期"
            @change="timerangechange"
            :default-time="['12:00:00', '17:00:00']"
          ></el-date-picker>
        </el-form-item>
      </el-form>

      <div slot="footer" class="dialog-footer">
        <el-button @click="clonedialogVisible = false">Cancel</el-button>
        <el-button type="primary" @click="clonecontest">Clone</el-button>
      </div>
    </el-dialog>

    <el-row :gutter="5">
      <el-col :span="4">
        <el-button
          plain
          :disabled="!contestisend"
          style="float:left;"
          @click="clonedialogVisible =true"
        >Clone</el-button>
      </el-col>

      <el-col :span="16">
        <center>
          <h1>{{ title }}</h1>
        </center>
      </el-col>

      <el-col :span="4">
        <el-button
          plain
          round
          :type="contestauth(auth)"
          @click="register"
          :foucs="false"
          :disabled="!canregister"
          style="float:right;"
        >
          <b>{{ auth }}</b>
        </el-button>
      </el-col>
    </el-row>

    <el-row :gutter="5">
      <center>
        <el-progress
          :text-inside="true"
          :stroke-width="18"
          :percentage="leftpercentage"
          :status="barstatus"
        ></el-progress>
        <br>
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
        :row-style="ratingcolor"
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
      title: "",
      level: 1,
      des: "",
      note: "",
      lefttime: 0.0,
      leftpercentage: 0,
      barstatus: "exception",
      timestyle: "wait",
      left: -100,
      lasttime: 0,
      contestisend: false,
      auth: 404,
      clonefrom:-1,

      currentpage: 1,
      pagesize: 10,
      totaluser: 10,
      tableData2: [],

      haveauth: 0,
      type: "1",
      showp: true,
      canregister: false,

      clonedialogVisible: false,
      addcontestform: {
        creator: sessionStorage.name,
        title: "新比赛",
        level: 3,
        des: "无",
        note: "无",
        timerange: [new Date(), new Date()],
        begintime: new Date(),
        lasttime: 0,
        type: "Personal",
        auth: 1,
        clonefrom:this.$route.params.contestID,
      }
    };
  },
  methods: {
    ratingcolor({ row, rowIndex }) {
      if (row.rating >= 3000) return "color:red;font-weight: bold;";
      if (row.rating >= 2600) return "color:#BB5E00;font-weight: bold;";
      if (row.rating >= 2200) return "color:#E6A23C;font-weight: bold;";
      if (row.rating >= 2050) return "color:#930093;font-weight: bold;";
      if (row.rating >= 1900) return "color:#0000AA;font-weight: bold;";
      if (row.rating >= 1700) return "color:#007799;font-weight: bold;";
      if (row.rating >= 1500) return "color:#227700;font-weight: bold;";
      if (row.rating >= 1350) return "color:#67C23A;font-weight: bold;";
      if (row.rating >= 1200) return "color:#909399;font-weight: bold;";
      return "color:#303133;font-weight: bold;";
    },
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
          this.$message.error(
            "服务器错误！" + "(" + JSON.stringify(error.response.data) + ")"
          );
        });
    },
    handleCurrentChange(val) {
      this.currentpage = val;
      this.$axios
        .get(
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
          this.$message.error(
            "服务器错误！" + "(" + JSON.stringify(error.response.data) + ")"
          );
        });
    },
    register() {
      if (this.haveauth) {
        this.$message({
          message: "你已注册或比赛已结束！",
          type: "success"
        });
        return;
      }
      if (this.left > 0) {
        this.$message.error("比赛已开始，无法注册！");
        return;
      }
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
            .post("/contestregister/", {
              contestid: parseInt(this.id),
              user: sessionStorage.username,
              rating: parseInt(sessionStorage.rating)
            })
            .then(res => {
              this.$message({
                message: "注册比赛成功！",
                type: "success"
              });

              this.$router.go(0);
            })
            .catch(error => {
              this.$message.error(
                "服务器错误！" + JSON.stringify(error.response.data)
              );
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
      this.$store.state.contestisend = false;
      this.$axios.get("/contestinfo/" + id + "/").then(response => {
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

        this.addcontestform.title = "[Clone] " + response.data.title;
        this.addcontestform.level = response.data.level;
        this.addcontestform.note = response.data.note;
        this.addcontestform.des = response.data.des;

        this.auth = response.data["auth"];
        this.title = response.data.title;
        this.$store.state.contesttitle = this.title;
        this.level = response.data.level;
        this.des = response.data.des;
        this.note = response.data.note;
        this.addcontestform.clonefrom = response.data.clonefrom == -1?response.data.id:response.data.clonefrom
        var sDate1 = response.data.begintime;

        var date2 = "";
        var date1 = new Date(Date.parse(sDate1));

        this.$axios
          .get("/currenttime/")
          .then(response2 => {
            date2 = response2.data;

            this.left = parseInt(
              (new Date(Date.parse(date2)).getTime() - date1.getTime()) / 1000
            );

            if (this.left < 0) this.timestyle = "wait";
            else {
              this.timestyle = "begin";
              this.barstatus = "success";
            }

            this.lasttime = response.data.lasttime;
            if (
              this.left >= response.data.lasttime &&
              isNaN(this.left) == false
            ) {
              this.left = response.data.lasttime;
              this.timestyle = "end";
              this.$store.state.contestisend = true;
            }
            
            this.$store.state.contestleft = this.left;
            var t = Math.abs(this.left);
            this.leftpercentage = parseInt(
              (Math.abs(this.left) / response.data.lasttime) * 100
            );

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

            this.$store.state.contestbegintime = date1.getTime();
            this.$store.state.contesttype = response.data.type;
            this.$store.state.contestfrom = response.data.clonefrom;
            this.tableData = [response.data];
            this.$axios
              .get(
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

                this.$store.state.contesttimer = setInterval(
                  this.refreshtime,
                  1000
                );
                this.canregister = true;
              })
              .catch(error => {
                this.$message.error(
                  "服务器错误！" +
                    "(" +
                    JSON.stringify(error.response.data) +
                    ")"
                );
              });
          })
          .catch(error => {
            this.$message.error(
              "服务器错误！" + "(" + JSON.stringify(error.response.data) + ")"
            );
          });
      });
    },
    refreshtime() {
      if (this.auth != "Public" && this.auth != "Private") {
        if (this.haveauth == 0 && this.left <= 0)
          this.auth = "Protect(Click to register)";
        else this.auth = "Protect";
      }

      this.left++;
      this.$store.state.contestleft = this.left;

      if (this.left == 0) {
        this.$router.go(0);
      }

      if (this.left < 0) this.timestyle = "wait";
      else {
        this.timestyle = "begin";
        this.barstatus = "success";
      }

      if (this.$store.state.contestisend == false) {
        if (this.left >= this.lasttime && isNaN(this.left) == false) {
          this.left = this.lasttime;
          this.timestyle = "end";
          this.$store.state.contestisend = true;
          this.contestisend = false;
          this.$router.go(0);
        }
      } else {
        this.left = this.lasttime;
        this.timestyle = "end";
        this.$store.state.contestisend = true;
        this.contestisend = true;
      }

      var t = Math.abs(this.left);
      this.leftpercentage = parseInt(
        (Math.abs(this.left) / this.lasttime) * 100
      );

      this.lefttime =
        parseInt(t / 60 / 60) +
        ":" +
        parseInt((t / 60) % 60) +
        ":" +
        parseInt((t % 60) % 60);
    },
    clonecontest() {
      if (this.addcontestform.lasttime < 600) {
        this.$message.error("比赛时间太短");
        return;
      }
      if (this.addcontestform.level < 1 || this.addcontestform.level > 5) {
        this.$message.error("比赛等级应为1~5");
        return;
      }
      if (this.addcontestform.auth < 0 || this.addcontestform.auth > 2) {
        this.$message.error("比赛权限应为0,1,2");
        return;
      }

      this.$confirm(
        "确定复制比赛吗？",
        "复制比赛：" + this.addcontestform.title,
        {
          confirmButtonText: "确定",
          cancelButtonText: "取消",
          type: "warning"
        }
      ).then(() => {
        this.$axios
          .post("/contestinfo/", this.addcontestform)
          .then(response => {
            var contestid = response.data.id;

            this.$axios.post("/contesttutorial/", {
              contestid: this.contestid,
              value: "暂无数据！"
            });

            this.$message({
              message: "复制比赛成功！比赛编号：" + response.data.id,
              type: "success"
            });

            this.$axios
              .get("/contestproblem/?contestid=" + this.id)
              .then(response2 => {
                for (let i = 0; i < response2.data.length; i++) {
                  this.$axios.post("/contestproblem/", {
                    contestid: response.data.id,
                    problemid: response2.data[i].problemid,
                    problemtitle: response2.data[i].problemtitle,
                    rank: response2.data[i].rank
                  });
                }
              });
            this.clonedialogVisible = false;
          })
          .catch(error => {
            this.$message.error(
              "服务器出错！" + JSON.stringify(error.response.data)
            );
          });
      });
    },
    timerangechange(range) {
      this.addcontestform.begintime = moment(range[0]).format(
        "YYYY-MM-DD HH:mm:ss"
      );
      this.addcontestform.lasttime = parseInt(
        (range[1].getTime() - range[0].getTime()) / 1000
      );
    }
  },
  destroyed() {
    clearInterval(this.$store.state.contesttimer);
  },
  mounted() {
    this.refresh(this.$route.params.contestID);
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
