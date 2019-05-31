<template>
  <el-row>
    <el-dialog title="选择题目" :visible.sync="dialogTableVisible" width="75%">
      <el-input
        placeholder="输入Title来筛选..."
        v-model="searchpro"
        @keyup.native.enter="searchprotitle"
        style="float:right;width:200px;"
      >
        <el-button slot="append" icon="el-icon-search" @click="searchprotitle"></el-button>
      </el-input>
      <el-pagination
        @current-change="handleCurrentChange"
        :current-page="currentpage"
        :page-size="20"
        :total="totalproblem"
        layout="total,prev, pager, next, jumper"
      ></el-pagination>

      <el-table :data="gridData" @cell-click="problemclick">
        <el-table-column property="problem" label="ID" width="70"></el-table-column>
        <el-table-column property="title" label="标题" width="350"></el-table-column>
        <el-table-column property="tag" label="标签"></el-table-column>
        <el-table-column property="score" label="分数" width="80"></el-table-column>
        <el-table-column property="oj" label="OJ" width="70"></el-table-column>
        <el-table-column property="level" label="难度" width="70"></el-table-column>
        <el-table-column property="ac" label="AC数" width="70"></el-table-column>
        <el-table-column property="submission" label="提交数" width="70"></el-table-column>
      </el-table>
    </el-dialog>
    <el-dialog title="选择比赛" :visible.sync="dialogTableVisible2" width="75%">
      <el-input
        v-model="searchtitle"
        placeholder="输入Title来筛选..."
        style="float:right;width:200px;"
        @change="searchcontest"
        @keyup.native.enter="searchcontest"
      >
        <el-button slot="append" icon="el-icon-search" @click="searchcontest"></el-button>
      </el-input>
      <el-pagination
        @current-change="handleCurrentContestChange"
        :current-page="currentpage2"
        :page-size="20"
        :total="totalcontest"
        layout="total,prev, pager, next, jumper"
      ></el-pagination>

      <el-table
        :data="gridData2"
        @cell-click="contestclick"
        :default-sort="{prop: 'id', order: 'descending'}"
      >
        <el-table-column property="id" label="ID" width="70"></el-table-column>
        <el-table-column property="title" label="比赛标题" ></el-table-column>
        <el-table-column prop="type" label="比赛类型" width="100"></el-table-column>
        <el-table-column prop="begintime" label="开始时间" width="200"></el-table-column>
        <el-table-column prop="lasttime" label="持续时间" width="90"></el-table-column>
      </el-table>
    </el-dialog>
    <el-row>
      <el-form :model="changecontestform" label-position="right">
        <el-form-item label="比赛编号：">
          <el-input
            style="width:200px;"
            v-model="contestid"
            @change="contestchange"
            placeholder="请输入比赛编号"
          ></el-input>
          <el-button
            style="margin-left:20px;"
            type="success"
            @click="dialogTableVisible2 = true"
          >选择比赛</el-button>
          <el-button type="danger" style="float:right;" @click="onDelContest">删除比赛</el-button>
        </el-form-item>

        <el-form-item label="作者：">
          <el-input v-model="changecontestform.creator" style="width:200px;"></el-input>
        </el-form-item>
        <el-form-item label="比赛名称：">
          <el-input v-model="changecontestform.title" style="width:400px;"></el-input>
        </el-form-item>
        <el-form-item label="比赛难度：">
          <el-select v-model="changecontestform.level" placeholder="请选择" style="width:200px;">
            <el-option key="1" label="简单" :value="1"></el-option>
            <el-option key="2" label="普通" :value="2"></el-option>
            <el-option key="3" label="中等" :value="3"></el-option>
            <el-option key="4" label="困难" :value="4"></el-option>
            <el-option key="5" label="极其困难" :value="5"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="比赛描述：">
          <el-input type="textarea" v-model="changecontestform.des" autosize style="width:800px;"></el-input>
        </el-form-item>
        <el-form-item label="比赛提示：">
          <el-input type="textarea" v-model="changecontestform.note" autosize style="width:800px;"></el-input>
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
          <el-select v-model="changecontestform.type" placeholder="Choose type...">
            <el-option key="0" label="ACM" value="ACM"></el-option>
            <el-option key="1" label="Rated" value="Rated"></el-option>
            <el-option key="2" label="Homework" value="Homework"></el-option>
            <el-option key="3" label="Personal" value="Personal"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="比赛权限：">
          <el-select
            style="width:200px;"
            v-model="changecontestform.auth"
            placeholder="Choose type..."
          >
            <el-option key="0" label="Public" :value="1"></el-option>
            <el-option key="1" label="Private" :value="2"></el-option>
            <el-option key="2" label="Protect(可注册)" :value="0"></el-option>
          </el-select>
        </el-form-item>

        <el-form-item label="默认参赛人员（如果是公开比赛，请忽略，私有比赛请务必填写，因为私有比赛不可注册，中间用英文逗号隔开）：">
          <el-input type="textarea" v-model="contestregister" autosize></el-input>
        </el-form-item>

        <el-form-item>
          <el-button type="success" @click="onChangeContestSubmit">更新比赛</el-button>
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
        <el-row :gutter="20">
          <el-col :span="4">
            <el-input @change="addproblemchange" v-model="tmpaddproblemid" placeholder="题目编号">
              <el-button slot="append" icon="el-icon-search" @click="addproblemchange"></el-button>
            </el-input>
          </el-col>
          <el-col :span="4">
            <el-input v-model="tmpaddproblemtitle" placeholder="比赛中的题目标题"></el-input>
          </el-col>
          <el-col :span="2">
            <el-button type="success" @click="dialogTableVisible = true">选择题目</el-button>
          </el-col>
          <el-col :span="4">
            <el-button type="primary" @click="addproblemclick" plain :disabled="!canadd">添加题目</el-button>
          </el-col>
        </el-row>
        <el-button type="success" @click="uploadproblemclick" :disabled="contestid==-1">更新题目</el-button>
      </el-row>
    </el-row>

    <el-row>
      编辑题解：
      <mavon-editor
        style="margin-top:20px"
        v-model="context"
        :toolbars="toolbars"
        @save="savemethod"
        @imgAdd="$imgAdd"
      />
    </el-row>
  </el-row>
</template>

<script>
import moment from "moment";
import { mavonEditor } from "mavon-editor";
import "mavon-editor/dist/css/index.css";
export default {
  name: "adminaddcontest",
  components: {
    mavonEditor
  },
  data() {
    return {
      dialogTableVisible2: false,
      dialogTableVisible: false,
      currentpage: 1,
      currentpage2: 1,
      gridData: [],
      gridData2: [],
      totalproblem: 0,
      totalcontest: 0,
      contestregister: "",
      contestid: -1,
      problemnames: [],
      tmpaddproblemid: "",
      tmpaddproblemtitle: "",
      canadd: false,

      searchtitle: "",
      searchpro: "",

      changecontestform: {
        creator: sessionStorage.name,
        title: "",
        level: 1,
        des: "",
        note: "",
        timerange: [new Date(), new Date()],
        begintime: new Date(),
        lasttime: 0,
        type: "",
        auth: 0
      },
      toolbars: {
        bold: true, // 粗体
        italic: true, // 斜体
        header: true, // 标题
        underline: true, // 下划线
        mark: true, // 标记
        superscript: true, // 上角标
        quote: true, // 引用
        ol: true, // 有序列表
        link: true, // 链接
        imagelink: true, // 图片链接
        help: true, // 帮助
        code: true, // code
        subfield: true, // 是否需要分栏
        fullscreen: true, // 全屏编辑
        readmodel: true, // 沉浸式阅读
        /* 1.3.5 */
        undo: true, // 上一步
        trash: true, // 清空
        save: true, // 保存（触发events中的save事件）
        /* 1.4.2 */
        navigation: true // 导航目录
      },
      context: "暂无数据！"
    };
  },
  methods: {
    searchprotitle() {
      this.currentpage = 1;
      this.$axios
        .get(
          "/problemdata/?limit=20&offset=" +
            (this.currentpage - 1) * 20 +
            "&search=" +
            this.searchpro
        )
        .then(response => {
          this.totalproblem = response.data.count;
          this.gridData = response.data.results;
        });
    },
    searchcontest() {
      this.currentpage2 = 1;
      this.$axios
        .get(
          "/contestinfo/?limit=20&offset=" +
            (this.currentpage2 - 1) * 20 +
            "&search=" +
            this.searchtitle
        )
        .then(response => {
          for (let i = 0; i < response.data.results.length; i++) {
            response.data.results[i].begintime = moment(
              response.data.results[i].begintime
            ).format("YYYY-MM-DD HH:mm:ss");
            response.data.results[i]["lasttime"] =
              parseInt(response.data.results[i]["lasttime"] / 60 / 60) +
              ":" +
              parseInt((response.data.results[i]["lasttime"] / 60) % 60) +
              ":" +
              parseInt((response.data.results[i]["lasttime"] % 60) % 60);
          }
          
          this.gridData2 = response.data.results;
          this.totalcontest = response.data.count;
        });
    },
    contestclick: function(row, column, cell, event) {
      this.contestid = row.id;
      this.contestchange(row.id);
      this.dialogTableVisible2 = false;
    },
    handleCurrentChange(val) {
      this.currentpage = val;
      this.$axios
        .get(
          "/problemdata/?limit=20&offset=" +
            (this.currentpage - 1) * 20 +
            "&search=" +
            this.searchpro
        )
        .then(response => {
          this.totalproblem = response.data.count;
          this.gridData = response.data.results;
        });
    },
    handleCurrentContestChange(val) {
      this.currentpage2 = val;

      this.$axios
        .get(
          "/contestinfo/?limit=20&offset=" +
            (this.currentpage2 - 1) * 20 +
            "&search=" +
            this.searchtitle
        )
        .then(response => {
          for (let i = 0; i < response.data.results.length; i++) {
            response.data.results[i].begintime = moment(
              response.data.results[i].begintime
            ).format("YYYY-MM-DD HH:mm:ss");
            response.data.results[i]["lasttime"] =
              parseInt(response.data.results[i]["lasttime"] / 60 / 60) +
              ":" +
              parseInt((response.data.results[i]["lasttime"] / 60) % 60) +
              ":" +
              parseInt((response.data.results[i]["lasttime"] % 60) % 60);
          }
          this.gridData2 = response.data.results;
          this.totalcontest = response.data.count;
        });
    },
    problemclick: function(row, column, cell, event) {
      this.tmpaddproblemid = row.problem;
      this.tmpaddproblemtitle = row.title;
      this.addproblemchange(row.problem);
      this.dialogTableVisible = false;
    },
    $imgAdd(pos, $file) {
      this.$message.error("暂不支持上传图片！请使用链接添加！");
    },
    savemethod(v, r) {
      this.$axios
        .get("/contesttutorial/?contestid=" + this.contestid)
        .then(response2 => {
          var tid = response2.data[0].id;
          this.$axios
            .put("/contesttutorial/" + tid + "/", {
              contestid: this.contestid,
              value: v
            })
            .then(response => {
              this.$message.success("保存成功！");
            })
            .catch(error => {
              this.$message.error(
                "服务器错误！" + "(" + JSON.stringify(error.response.data) + ")"
              );
            });
        })
        .catch(error => {
          this.$message.error(
            "服务器错误！" + "(" + JSON.stringify(error.response.data) + ")"
          );
        });
    },
    contestchange(num) {
      this.$axios
        .get("/contesttutorial/?contestid=" + num)
        .then(response22 => {
          if (response22.data.length > 0)
            this.context = response22.data[0].value;
        })
        .catch(error => {
          this.$message.error(
            "服务器出错！" + JSON.stringify(error.response.data)
          );
        });

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
  created() {
    this.$axios
      .get(
        "/problemdata/?limit=20&offset=" +
          (this.currentpage - 1) * 20 +
          "&search=" +
          this.searchpro
      )
      .then(response => {
        this.totalproblem = response.data.count;
        this.gridData = response.data.results;
        this.$axios
          .get(
            "/contestinfo/?limit=20&offset=" +
              (this.currentpage2 - 1) * 20 +
              "&search=" +
              this.searchtitle
          )
          .then(response2 => {
            for (let i = 0; i < response2.data.results.length; i++) {
              response2.data.results[i].begintime = moment(
                response2.data.results[i].begintime
              ).format("YYYY-MM-DD HH:mm:ss");
              response2.data.results[i]["lasttime"] =
              parseInt(response2.data.results[i]["lasttime"] / 60 / 60) +
              ":" +
              parseInt((response2.data.results[i]["lasttime"] / 60) % 60) +
              ":" +
              parseInt((response2.data.results[i]["lasttime"] % 60) % 60);
            }
            this.gridData2 = response2.data.results;
            this.totalcontest = response2.data.count;
          });
      });
  }
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.el-tag + .el-tag {
  margin-left: 10px;
}
</style>
