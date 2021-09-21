<template>
  <el-row>
    <el-dialog title="选择题目"
               :visible.sync="dialogTableVisible"
               width="75%">
      <el-input placeholder="输入Title来筛选..."
                v-model="searchpro"
                @keyup.native.enter="searchtitle"
                style="float:right;width:200px;">
        <el-button slot="append"
                   icon="el-icon-search"
                   @click="searchtitle"></el-button>
      </el-input>
      <el-pagination @current-change="handleCurrentChange"
                     :current-page="currentpage"
                     :page-size="20"
                     :total="totalproblem"
                     layout="total,prev, pager, next, jumper"></el-pagination>

      <el-table :data="gridData"
                @cell-click="problemclick">
        <el-table-column property="problem"
                         label="ID"
                         width="70"></el-table-column>
        <el-table-column property="title"
                         label="标题"
                         width="350"></el-table-column>
        <el-table-column property="tag"
                         label="标签"></el-table-column>
        <el-table-column property="score"
                         label="分数"
                         width="80"></el-table-column>
        <el-table-column property="oj"
                         label="OJ"
                         width="70"></el-table-column>
        <el-table-column property="level"
                         label="难度"
                         width="70"></el-table-column>
        <el-table-column property="ac"
                         label="AC数"
                         width="70"></el-table-column>
        <el-table-column property="submission"
                         label="提交数"
                         width="70"></el-table-column>
      </el-table>
    </el-dialog>

    <el-dialog title="选择题目"
               :visible.sync="dialogTableVisible3"
               width="75%">
      <el-table :data="TableData"
                @cell-click="choiceproblemclick">
        <el-table-column property="ChoiceProblemId"
                         label="ID"
                         width="50"></el-table-column>
        <el-table-column :show-overflow-tooltip="true"
                         property="des"
                         label="题目"
                         width="350"></el-table-column>
        <el-table-column :show-overflow-tooltip="true"
                         property="choiceA"
                         label="A"
                         width="200"></el-table-column>
        <el-table-column :show-overflow-tooltip="true"
                         property="choiceB"
                         label="B"
                         width="200"></el-table-column>
        <el-table-column :show-overflow-tooltip="true"
                         property="choiceC"
                         label="C"
                         width="200"></el-table-column>
        <el-table-column :show-overflow-tooltip="true"
                         property="choiceD"
                         label="D"
                         width="200"></el-table-column>
      </el-table>
    </el-dialog>

    <el-dialog title="选择班级"
               :visible.sync="dialogTableVisible2"
               width="50%">
      <el-table :data="tableData"
                @cell-click="classclick">
        <el-table-column property="className"
                         label="班级"
                         align="center"></el-table-column>
      </el-table>
    </el-dialog>

    <el-row>
      <el-form :model="addcontestform"
               label-position="right">
        <el-form-item label="作者：">
          <el-input v-model="addcontestform.creator"
                    style="width:200px;"></el-input>
        </el-form-item>
        <el-form-item label="比赛名称：">
          <el-input v-model="addcontestform.title"
                    style="width:400px;"></el-input>
        </el-form-item>
        <el-form-item label="比赛难度：">
          <el-select v-model="addcontestform.level"
                     placeholder="请选择"
                     style="width:200px;">
            <el-option key="1"
                       label="简单"
                       :value="1"></el-option>
            <el-option key="2"
                       label="普通"
                       :value="2"></el-option>
            <el-option key="3"
                       label="中等"
                       :value="3"></el-option>
            <el-option key="4"
                       label="困难"
                       :value="4"></el-option>
            <el-option key="5"
                       label="极其困难"
                       :value="5"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="比赛描述：">
          <el-input type="textarea"
                    v-model="addcontestform.des"
                    autosize
                    style="width:800px;"></el-input>
        </el-form-item>
        <el-form-item label="比赛提示：">
          <el-input type="textarea"
                    v-model="addcontestform.note"
                    autosize
                    style="width:800px;"></el-input>
        </el-form-item>
        <el-form-item label="比赛时间：">
          <el-date-picker v-model="addcontestform.timerange"
                          type="datetimerange"
                          align="right"
                          start-placeholder="开始日期"
                          end-placeholder="结束日期"
                          @change="timerangechange"
                          :default-time="['12:00:00', '17:00:00']"></el-date-picker>
        </el-form-item>
        <el-form-item label="比赛类型（ACM/OI/其他）：">
          <el-select v-model="addcontestform.type"
                     placeholder="Choose type...">
            <el-option key="0"
                       label="ACM"
                       value="ACM"></el-option>
            <el-option key="1"
                       label="Rated"
                       value="Rated"></el-option>
            <el-option key="2"
                       label="Homework"
                       value="Homework"></el-option>
            <el-option key="3"
                       label="Personal"
                       value="Personal"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="比赛权限：">
          <el-select style="width:200px;"
                     v-model="addcontestform.auth"
                     placeholder="Choose type...">
            <el-option key="0"
                       label="Public"
                       :value="1"></el-option>
            <el-option key="1"
                       label="Private"
                       :value="2"></el-option>
            <el-option key="2"
                       label="Protect(可注册)"
                       :value="0"></el-option>
          </el-select>
        </el-form-item>

        <el-form-item label="是否封榜：">
            <el-select style="width:200px;"
                       v-model="addcontestform.lockboard"
                       placeholder="Choose...">
              <el-option key="0"
                         label="不开启封榜（解除封榜）"
                         :value="0"></el-option>
              <el-option key="1"
                         label="开启封榜功能"
                         :value="1"></el-option>
            </el-select>
        </el-form-item>
        
        <el-form-item label="封榜时间（分钟）：">
          <el-input-number
            style="width:200px;"
            v-model="addcontestform.locktime"
            :step="10"
            :min="0"
          ></el-input-number>
        </el-form-item>
        

        <el-row>
          <el-col>
            <el-form-item label="班级">
              <el-input type="textarea"
                        v-model="addClassName"
                        width="100"></el-input>
            </el-form-item>
          </el-col>
          <el-col :span="2">
            <el-button type="success"
                       @click="dialogTableVisible2 = true">选择班级</el-button>
          </el-col>

        </el-row>

        <el-form-item label="默认参赛人员（如果是公开比赛，请忽略，私有比赛请务必填写，因为私有比赛不可注册，中间用英文逗号或换行隔开）：">
          <el-input type="textarea"
                    v-model="contestregister"
                    autosize></el-input>
        </el-form-item>

        <el-form-item>
          <el-button type="success"
                     @click="onAddContestSubmit"
                     :disabled="contestid!=-1">添加比赛</el-button>
        </el-form-item>
      </el-form>
    </el-row>
    (添加比赛后再确认保存题目)
    <el-row style="margin-top:50px;">
      <el-row>
        <el-tag :key="index"
                v-for="(tag,index) in problemnames"
                closable
                :disable-transitions="false"
                @close="handleClose(tag)">{{tag}}</el-tag>
      </el-row>

      <el-row>
        <el-row :gutter="20">
          <el-col :span="4">
            <el-input @change="addproblemchange"
                      v-model="tmpaddproblemid"
                      placeholder="题目编号">
              <el-button slot="append"
                         icon="el-icon-search"
                         @click="addproblemchange"></el-button>
            </el-input>
          </el-col>
          <el-col :span="4">
            <el-input v-model="tmpaddproblemtitle"
                      placeholder="比赛中的题目标题"></el-input>
          </el-col>
          <el-col :span="2">
            <el-button type="success"
                       @click="dialogTableVisible = true">选择题目</el-button>
          </el-col>
          <el-col :span="4">
            <el-button type="primary"
                       @click="addproblemclick"
                       plain
                       :disabled="!canadd">添加题目</el-button>
          </el-col>
        </el-row>

        <el-row>
          <el-row>
            <el-tag :key="index"
                    v-for="(tag,index) in choiceproblemids"
                    closable
                    :disable-transitions="false"
                    @close="handleClose2(tag)">{{tag}}</el-tag>
          </el-row>
          <el-row>
            <el-row :gutter="20">

              <el-col :span="6">
                <el-input v-model="tmpaddchoiceproblemid"
                          placeholder="选择题编号"></el-input>
              </el-col>
              <el-col :span="3">
                <el-button type="success"
                           @click="dialogTableVisible3 = true">选择题目</el-button>
              </el-col>
              <el-col :span="4">
                <el-button type="primary"
                           @click="addchoiceproblemclick"
                           plain
                           :disabled="!canadd2">添加选择题（选择题只会显示题目编号）</el-button>
              </el-col>
            </el-row>

          </el-row>
        </el-row>

        <el-button type="success"
                   @click="uploadproblemclick"
                   :disabled="contestid==-1">确认保存题目</el-button>

      </el-row>
    </el-row>
  </el-row>
</template>

<script>
import moment from "moment";
export default {
  name: "adminaddcontest",
  data () {
    return {
      tableData: [],
      TableData: [],
      choiceproblemids: [],
      tmpaddchoiceproblemid: "",
      dialogTableVisible3: false,
      dialogTableVisible2: false,
      dialogTableVisible: false,
      currentpage: 1,
      gridData: [],
      totalproblem: 0,
      contestregister: "",
      contestid: -1,
      problemnames: [],
      tmpaddproblemid: "",
      tmpaddproblemtitle: "",
      canadd: false,
      canadd2: false,
      searchpro: "",

      addClassName: "",
      classfill: "",
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
        auth: 0,
        iprange: "None",
        classes: "All",
        lockboard:0,
        locktime:0
      }
    };
  },
  methods: {

    searchtitle () {
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
    handleCurrentChange (val) {
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
    problemclick: function (row, column, cell, event) {
      this.tmpaddproblemid = row.problem;
      this.tmpaddproblemtitle = row.title;
      this.addproblemchange(row.problem);
      this.dialogTableVisible = false;
    },
    classclick: function (row, column, cell, event) {
      this.addcontestform.classes = row.className;
      this.addClassName = row.className;
      this.dialogTableVisible2 = false;
    },
    uploadproblemclick () {
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
          this.$axios.post("/contestproblem/", {
            contestid: this.contestid,
            problemid: li[0],
            problemtitle: li[1],
            rank: i
          });
        }

        for (var i = 0; i < this.choiceproblemids.length; i++) {
          var AddId = this.choiceproblemids[i];
          this.$axios.post("/contestchoiceproblem/", {
            ContestId: this.contestid,
            ChoiceProblemId: AddId,
            rank: i
          });
        }


        this.$message({
          message: "添加题目成功！",
          type: "success"
        });
        this.problemnames = [];
        this.contestid = -1;


      });
    },
    addproblemclick () {
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
    addproblemchange (num) {
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

    handleClose (tag) {
      this.problemnames.splice(this.problemnames.indexOf(tag), 1);
    },
    handleClose2 (tag) {
      this.choiceproblemids.splice(this.choiceproblemids.indexOf(tag), 1);
    },

    timerangechange (range) {
      this.addcontestform.begintime = moment(range[0]).format(
        "YYYY-MM-DD HH:mm:ss"
      );
      this.addcontestform.lasttime = parseInt(
        (range[1].getTime() - range[0].getTime()) / 1000
      );
    },

    onAddContestSubmit () {
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
        console.log(this.addcontestform);
        this.$axios
          .post("/contestinfo/", this.addcontestform)
          .then(response => {
            this.contestid = response.data.id;

            if (response.data.auth != 1) {
              var li = this.contestregister.split(/[,\n]/);

              for (var i = 0; i < li.length; i++) {
                this.$axios.post("/contestregister/", {
                  contestid: this.contestid,
                  user: li[i]
                });
              }
            }
            this.$axios.post("/contesttutorial/", {
              contestid: this.contestid,
              value: "暂无数据！"
            });

            this.$message({
              message:
                "添加比赛成功！比赛编号：" +
                response.data.id +
                "现在可以添加题目了！",
              type: "success"
            });
          })
          .catch(error => {
            this.$message.error(
              "服务器出错！" + JSON.stringify(error.response.data)
            );
          });
      });
    },

    choiceproblemclick: function (row, column, cell, event) {
      this.tmpaddchoiceproblemid = row.ChoiceProblemId;
      this.canadd2 = true;
      this.dialogTableVisible3 = false;
    },
    addchoiceproblemclick () {
      this.choiceproblemids.push(
        this.tmpaddchoiceproblemid
      );
    },

  },
  created () {
    this.$axios.get("/classes/")
      .then(
        response5 => {
          console.log(response5.data);
          this.tableData = response5.data;
        }
      )

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

    this.$axios.get("/choiceproblem/")
      .then(response => {
        this.TableData = response.data;
      })
  },


};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.el-tag + .el-tag {
  margin-left: 10px;
}
</style>
