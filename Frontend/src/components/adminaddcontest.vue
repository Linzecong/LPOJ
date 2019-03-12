<template>
  <el-row>
    <el-row>
      <el-form :model="addcontestform" label-position="right">
        <el-form-item label="作者：">
          <el-input v-model="addcontestform.creator"></el-input>
        </el-form-item>
        <el-form-item label="比赛名称：">
          <el-input v-model="addcontestform.title"></el-input>
        </el-form-item>
        <el-form-item label="比赛难度（1~5）：">
          <el-input v-model="addcontestform.level"></el-input>
        </el-form-item>
        <el-form-item label="比赛描述：">
          <el-input type="textarea" v-model="addcontestform.des" autosize></el-input>
        </el-form-item>
        <el-form-item label="比赛提示：">
          <el-input type="textarea" v-model="addcontestform.note" autosize></el-input>
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
        <el-form-item label="比赛类型（ACM/OI/其他）：">
          <el-input v-model="addcontestform.type"></el-input>
        </el-form-item>
        <el-form-item label="比赛权限（1 public 2 private 0 protect(可注册)）：">
          <el-input v-model.number="addcontestform.auth"></el-input>
        </el-form-item>

        <el-form-item label="默认参赛人员（如果是公开比赛，请忽略，私有比赛请务必填写，因为私有比赛不可注册，中间用英文逗号隔开）：">
          <el-input type="textarea" v-model="contestregister" autosize></el-input>
        </el-form-item>

        <el-form-item>
          <el-button type="primary" @click="onAddContestSubmit" :disabled="contestid!=-1">添加比赛</el-button>
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
          <el-button type="primary" @click="uploadproblemclick" :disabled="contestid==-1">提交题目</el-button>
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
      contestregister: "username1,username2,userid3,notnikename4",
      contestid: -1,
      problemnames: [],
      tmpaddproblemid: "",
      tmpaddproblemtitle: "",
      canadd: false,
      addcontestform: {
        creator: sessionStorage.name,
        title: "新比赛",
        level: 3,
        des: "无",
        note: "无",
        timerange: [new Date(), new Date()],
        begintime: new Date(),
        lasttime: 0,
        type: "ACM",
        auth: 0
      }
    };
  },
  methods: {
    uploadproblemclick() {
      this.$confirm(
        "添加题目的比赛id：" +
          this.contestid +
          "         添加的题目：  " +
          this.problemnames,
        "确定添加题目吗？",
        {
          confirmButtonText: "确定",
          cancelButtonText: "取消",
          type: "warning"
        }
      ).then(() => {
        for (var i = 0; i < this.problemnames.length; i++) {
          var li = this.problemnames[i].split("|");
          this.$axios.post(
            "/api/contestproblem/",
            {
              contestid: this.contestid,
              problemid: li[0],
              problemtitle: li[1],
              rank: i
            }
          );
        }
        this.$message({
          message: "添加题目成功！",
          type: "success"
        });
        this.problemnames = [];
        this.contestid = -1;
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
        .get(
          "/api/problemdata/" + num + "/"
        )
        .then(response2 => {
          this.tmpaddproblemtitle = response2.data.title;
          this.canadd = true;
        })
        .catch(error => {
          this.canadd = false;
          this.$message.error("服务器错误！" + error);
        });
    },
    handleClose(tag) {
      this.problemnames.splice(this.problemnames.indexOf(tag), 1);
    },

    timerangechange(range) {
      this.addcontestform.begintime = moment(range[0]).format(
        "YYYY-MM-DD HH:mm:ss"
      );
      this.addcontestform.lasttime = parseInt(
        (range[1].getTime() - range[0].getTime()) / 1000
      );
      console.log(this.addcontestform.begintime);
    },

    onAddContestSubmit() {
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

      this.$confirm("确定添加吗？", "添加比赛：" + this.addcontestform.title, {
        confirmButtonText: "确定",
        cancelButtonText: "取消",
        type: "warning"
      }).then(() => {
        this.$axios
          .post(
            "/api/contestinfo/",
            this.addcontestform
          )
          .then(response => {
            this.contestid = response.data.id;

            if (response.data.auth != 1) {
              var li = this.contestregister.split(",");

              for (var i = 0; i < li.length; i++) {
                this.$axios.post(
                  "/api/contestregister/",
                  {
                    contestid: this.contestid,
                    user: li[i]
                  }
                );
              }
            }

            this.$message({
              message:
                "添加比赛成功！比赛编号：" +
                response.data.id +
                "现在可以添加题目了！",
              type: "success"
            });
          })
          .catch(error => {
            this.$message.error("服务器出错！" + error);
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
