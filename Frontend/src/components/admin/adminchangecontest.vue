<template>
  <el-row>
    <el-row>
      <el-form :model="changecontestform" label-position="right">
        <el-form-item label="比赛编号：">
          <el-input v-model="contestid" @change="contestchange" placeholder="请输入比赛编号"></el-input>
          <el-button type="danger" @click="onDelContest">删除比赛</el-button>
        </el-form-item>

        <el-form-item label="作者：">
          <el-input v-model="changecontestform.creator"></el-input>
        </el-form-item>
        <el-form-item label="比赛名称：">
          <el-input v-model="changecontestform.title"></el-input>
        </el-form-item>
        <el-form-item label="比赛难度（1~5）：">
          <el-input v-model="changecontestform.level"></el-input>
        </el-form-item>
        <el-form-item label="比赛描述：">
          <el-input type="textarea" v-model="changecontestform.des" autosize></el-input>
        </el-form-item>
        <el-form-item label="比赛提示：">
          <el-input type="textarea" v-model="changecontestform.note" autosize></el-input>
        </el-form-item>
        <el-form-item label="比赛时间：">
          <el-date-picker
            v-model="changecontestform.timerange"
            type="datetimerange"
            align="right"
            start-placeholder="开始日期"
            end-placeholder="结束日期"
            @change="timerangechange"
            :default-time="['12:00:00', '17:00:00']"
          ></el-date-picker>
        </el-form-item>
        <el-form-item label="比赛类型（ACM/OI/其他）：">
          <el-input v-model="changecontestform.type"></el-input>
        </el-form-item>
        <el-form-item label="比赛权限（1 public 2 private 0 protect(可注册)）：">
          <el-input v-model.number="changecontestform.auth"></el-input>
        </el-form-item>

        <el-form-item label="默认参赛人员（如果是公开比赛，请忽略，私有比赛请务必填写，因为私有比赛不可注册，中间用英文逗号隔开）：">
          <el-input type="textarea" v-model="contestregister" autosize></el-input>
        </el-form-item>

        <el-form-item>
          <el-button type="primary" @click="onChangeContestSubmit">更新比赛</el-button>
        </el-form-item>
      </el-form>
    </el-row>

    <el-row>
      <el-row>
        <el-tag
          :key="index"
          v-for="(tag,index) in problemnames"
          closable
          :disable-transitions="false"
          @close="handleClose(tag)"
        >{{tag}}</el-tag>
      </el-row>
      <el-row>
        <el-row>
          <el-col :span="4">
            <el-input @change="addproblemchange" v-model="tmpaddproblemid" placeholder="题目编号"></el-input>
          </el-col>
          <el-col :span="4">
            <el-input v-model="tmpaddproblemtitle" placeholder="比赛中的题目标题"></el-input>
          </el-col>
          <el-col :span="10">
            <el-button type="primary" @click="addproblemclick" plain :disabled="!canadd">添加题目</el-button>
          </el-col>
        </el-row>
        <el-row>
          <el-button type="primary" @click="uploadproblemclick" :disabled="contestid==-1">更新题目</el-button>
        </el-row>
      </el-row>
    </el-row>
  </el-row>
</template>

<script>
import moment from "moment";
export default {
  name: "adminaddcontest",
  data() {
    return {
      contestregister: "",
      contestid: -1,
      problemnames: [],
      tmpaddproblemid: "",
      tmpaddproblemtitle: "",
      canadd: false,
      changecontestform: {
        creator: localStorage.name,
        title: "",
        level: 1,
        des: "",
        note: "",
        timerange: [new Date(), new Date()],
        begintime: new Date(),
        lasttime: 0,
        type: "",
        auth: 0
      }
    };
  },
  methods: {
    contestchange(num) {
      this.$axios
        .get("/contestinfo/" + num + "/")
        .then(response => {
          response.data.timerange = [];
          response.data.timerange.push(response.data.begintime);
          response.data.timerange.push(
            moment(
              new Date(response.data.begintime).getTime() +
                response.data.lasttime * 1000
            ).format("YYYY-MM-DD HH:mm:ss")
          );
          this.changecontestform = response.data;

          this.$axios
            .get("/contestregister/?contestid=" + num)
            .then(response2 => {
              var str = "";
              for (var i = 0; i < response2.data.length; i++) {
                str = str + response2.data[i].user + ",";
              }
              if (str != "") str = str.substring(0, str.length - 1);

              this.contestregister = str;

              this.$axios
                .get("/contestproblem/?contestid=" + num)
                .then(response3 => {
                  var li = [];
                  for (var i = 0; i < response3.data.length; i++) {
                    li.push(
                      response3.data[i].problemid +
                        "|" +
                        response3.data[i].problemtitle
                    );
                  }
                  this.problemnames = li;
                })
                .catch(error => {
                  this.$message.error(
                    "服务器出错！" + JSON.stringify(error.response.data)
                  );
                });
            })
            .catch(error => {
              this.$message.error(
                "服务器出错！" + JSON.stringify(error.response.data)
              );
            });
        })
        .catch(error => {
          this.$message.error(
            "服务器错误！" + JSON.stringify(error.response.data)
          );
          this.changecontestform = {};
        });
    },
    onDelContest() {
      this.$confirm("删除比赛id：" + this.contestid, "确定删除比赛吗？", {
        confirmButtonText: "确定",
        cancelButtonText: "取消",
        type: "warning"
      }).then(() => {
        this.$confirm("再次确认", "确定删除比赛吗？", {
          confirmButtonText: "确定",
          cancelButtonText: "取消",
          type: "warning"
        }).then(() => {
          this.$axios
            .delete("/contestinfo/" + this.contestid + "/")
            .then(res => {
              this.$message({
                message: "删除成功！",
                type: "success"
              });
              this.$router.go(0);
            })
            .catch(error => {
              this.$message.error("删除失败！" + error);
            });
        });
      });
    },
    uploadproblemclick() {
      this.$confirm(
        "更新题目的比赛id：" +
          this.contestid +
          "         更新的题目：  " +
          this.problemnames,
        "确定更新题目吗？",
        {
          confirmButtonText: "确定",
          cancelButtonText: "取消",
          type: "warning"
        }
      ).then(() => {
        this.$axios
          .get("/contestproblem/?contestid=" + this.contestid)
          .then(response2 => {
            for (var i = 0; i < response2.data.length; i++) {
              this.$axios.delete(
                "/contestproblem/" + response2.data[i].id + "/"
              );
            }

            for (var i = 0; i < this.problemnames.length; i++) {
              var li = this.problemnames[i].split("|");
              this.$axios.post("/contestproblem/", {
                contestid: this.contestid,
                problemid: li[0],
                problemtitle: li[1],
                rank: i
              });
            }
          });

        this.$message({
          message: "更新题目成功！",
          type: "success"
        });
      });
    },
    addproblemclick() {
      if (
        this.tmpaddproblemtitle.indexOf("|") >= 0 ||
        this.tmpaddproblemid.indexOf("|") >= 0
      ) {
        this.$message.error("非法字符 | ");
        return;
      }
      this.problemnames.push(
        this.tmpaddproblemid + "|" + this.tmpaddproblemtitle
      );
    },
    addproblemchange(num) {
      this.$axios
        .get("/problemdata/" + num + "/")
        .then(response2 => {
          this.tmpaddproblemtitle = response2.data.title;
          this.canadd = true;
        })
        .catch(error => {
          this.canadd = false;
          this.$message.error(
            "服务器错误！" + JSON.stringify(error.response.data)
          );
        });
    },
    handleClose(tag) {
      this.problemnames.splice(this.problemnames.indexOf(tag), 1);
    },

    timerangechange(range) {
      this.changecontestform.begintime = moment(range[0]).format(
        "YYYY-MM-DD HH:mm:ss"
      );
      this.changecontestform.lasttime = parseInt(
        (range[1].getTime() - range[0].getTime()) / 1000
      );
      console.log(this.changecontestform.begintime);
    },

    onChangeContestSubmit() {
      if (this.contestid <= 0 || isNaN(this.contestid)) {
        this.$message.error("比赛ID不合法");
        return;
      }
      if (this.changecontestform.lasttime < 600) {
        this.$message.error("比赛时间太短");
        return;
      }
      if (
        this.changecontestform.level < 1 ||
        this.changecontestform.level > 5
      ) {
        this.$message.error("比赛等级应为1~5");
        return;
      }
      if (this.changecontestform.auth < 0 || this.changecontestform.auth > 2) {
        this.$message.error("比赛权限应为0,1,2");
        return;
      }

      this.$confirm("确定更新吗？", "更新比赛id： " + this.contestid, {
        confirmButtonText: "确定",
        cancelButtonText: "取消",
        type: "warning"
      }).then(() => {
        this.$axios
          .put("/contestinfo/" + this.contestid + "/", this.changecontestform)
          .then(response => {
            this.contestid = response.data.id;

            if (response.data.auth != 1) {
              this.$axios
                .get("/contestregister/?contestid=" + this.contestid)
                .then(response2 => {
                  for (var i = 0; i < response2.data.length; i++) {
                    this.$axios.delete(
                      "/contestregister/" + response2.data[i].id + "/"
                    );
                  }

                  var li = this.contestregister.split(",");

                  for (var i = 0; i < li.length; i++) {
                    this.$axios.post("/contestregister/", {
                      contestid: this.contestid,
                      user: li[i]
                    });
                  }
                });
            }

            this.$message({
              message: "更新比赛成功！比赛编号：" + response.data.id,
              type: "success"
            });
          })
          .catch(error => {
            this.$message.error(
              "服务器出错！" + JSON.stringify(error.response.data)
            );
          });
      });
    }
  },
  created() {}
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.el-tag + .el-tag {
  margin-left: 10px;
}
</style>
