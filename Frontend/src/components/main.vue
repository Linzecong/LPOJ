<template>
  <el-row :gutter="12">
    <el-col :span="6">
      <el-row :gutter="10">
        <el-card>
          <h3>{{ msg }}</h3>
          <h3>当前版本：1.2</h3>
          <h3>支持语言：C/C++/Java</h3>
        </el-card>
        <el-card style="margin-top:10px">
          <h3>Top User</h3>
          <el-table
            :data="tableData"
            border
            style="width: 100%"
            @cell-click="userclick"
            size="mini"
            :row-style="rankcolor"
          >
            <el-table-column type="index" width="40"></el-table-column>
            <el-table-column prop="username" label="User"></el-table-column>
            <el-table-column prop="score" label="Score"></el-table-column>
          </el-table>
        </el-card>
        <ojmessage></ojmessage>
      </el-row>
    </el-col>
    <el-col :span="18">
      <el-tabs type="border-card">
        <el-tab-pane label="队伍">
          <teamchart></teamchart>
        </el-tab-pane>
        <el-tab-pane label="个人" :lazy="true">
          <rankchart></rankchart>
        </el-tab-pane>
        <el-tab-pane label="规则" :lazy="true">
          <h3>基于艾洛积分系统（Elo Rating System）修改</h3>
          <h4>1、所有队伍初始得分为1500</h4>
          <h4>2、每场比赛后计算一个排名得分S （ S=（比赛得分线性归一化后）*比赛队伍数 ）（线性归一化函数: x = (x-min)/(max-min)）</h4>
          <h4>3、每场比赛后计算一个期望得分E （ E=sum(1/(1+10^((Rb-Ra)/400)))</h4>
          <h4>其中Ra代表你当前积分，Rb代表每一队伍的得分</h4>
          <h4>4、为了鼓励思考，计算一个系数K，K=（本次比赛得分/平均分）</h4>
          <h4>5、为了鼓励新人，计算一个系数P，P=（开始比赛前的积分排名/总人数）</h4>
          <h4>6、计算积分的变化 D = 20*(K+P+S-E)</h4>

          <h3>每场比赛排名怎么算?</h3>
          <h3>LPOJ个人赛：</h3>
          <h4>每道题目有一个积分，按照AC顺序得分为 题目积分-(题目积分/做出总人数/2)*(AC顺序-1)</h4>
          <h4>每一次失败提交-20分，一血加分为 题目积分/100</h4>
          <br>
          <h4>集训组队赛：</h4>
          <h4>为减轻管理员负担，并鼓励积极思考，按照如下规则算分，所有队伍仅算校内队伍</h4>
          <h4>每道题初始分为500+500*(比赛总队伍-AC队数)</h4>
          <h4>每道题目有一个积分，按照AC顺序得分为 题目积分-(题目积分/做出总人数/2)*(AC顺序-1)</h4>
          <h4>每一次失败提交-50分（每道题目最多算十发罚时），一血加分为 题目积分/100</h4>

          <br>
          <br>
          <h2>每场比赛结果都会保存，所以如果积分系统崩了的话，可以用其他方式计算，保证公平性</h2>
        </el-tab-pane>
      </el-tabs>
      <el-card style="margin-top:10px">
        <center>
          <h3>近期比赛</h3>
        </center>
        <el-table
          :data="tableData2"
          @cell-click="contestclick"
          :default-sort="{prop: 'begintime', order: 'descending'}"
        >
          <el-table-column prop="id" label="ID" :width="100"></el-table-column>
          <el-table-column prop="title" label="Title"></el-table-column>
          <el-table-column prop="begintime" label="Begin Time"></el-table-column>
          <el-table-column prop="lasttime" label="Duration"></el-table-column>
          <el-table-column prop="auth" label="Openness">
            <template slot-scope="scope">
              <el-tag
                id="leveltag"
                size="medium"
                disable-transitions
                hit
                :type="contestauth(scope.row.auth)"
              >{{ scope.row.auth }}</el-tag>
            </template>
          </el-table-column>
        </el-table>
      </el-card>

      <el-card style="margin-top:10px">
        <center>
          <h3>最新博客</h3>
        </center>
        <el-table :data="tableData3" @cell-click="blogclick" size="small">
          <el-table-column prop="username" label="User" :width="150"></el-table-column>
          <el-table-column prop="title" label="Title (Click to view content)">
            <template slot-scope="scope">
              <el-popover trigger="hover" placement="top" :width="500">
                <p>摘要: {{ scope.row.summary }}</p>
                <div slot="reference" class="name-wrapper">
                  <b>{{ scope.row.title }}</b>
                </div>
              </el-popover>
            </template>
          </el-table-column>
          <el-table-column prop="time" label="Time" :width="160"></el-table-column>
        </el-table>
      </el-card>
    </el-col>
  </el-row>
</template>

<script>
import moment from "moment";
import rankchart from "@/components/rankchart";
import teamchart from "@/components/teamchart";
import ojmessage from "@/components/ojmessage";
export default {
  components: {
    rankchart,
    teamchart,
    ojmessage
  },
  name: "main",
  data() {
    return {
      msg: "欢迎来到LPOJ",
      tableData: [],
      tableData2: [],
      tableData3: []
    };
  },
  created() {
    this.$axios
      .get("/userdata/?limit=10&offset=0")
      .then(response => {
        this.tableData = response.data.results;
      })
      .catch(error => {
        this.$message.error("服务器错误！" + "(" + error + ")");
      });
    this.$axios
      .get("/blog/?limit=10&offset=0")
      .then(response => {
        for (var i = 0; i < response.data.results.length; i++) {
          response.data.results[i].time = moment(
            response.data.results[i].time
          ).format("YYYY-MM-DD HH:mm:ss");
        }
        this.tableData3 = response.data.results;
      })
      .catch(error => {
        this.$message.error("服务器错误！" + "(" + error + ")");
      });

    this.$axios
      .get("/contestcominginfo/")
      .then(response => {
        for (var i = 0; i < response.data.length; i++) {
          response.data[i]["begintime"] = moment(
            response.data[i]["begintime"]
          ).format("YYYY-MM-DD HH:mm:ss");
          response.data[i]["lasttime"] =
            parseInt(response.data[i]["lasttime"] / 60 / 60) +
            ":" +
            parseInt((response.data[i]["lasttime"] / 60) % 60) +
            ":" +
            parseInt((response.data[i]["lasttime"] % 60) % 60);

          if (response.data[i]["auth"] == "1")
            response.data[i]["auth"] = "Public";
          if (response.data[i]["auth"] == "2")
            response.data[i]["auth"] = "Private";
          if (response.data[i]["auth"] == "0")
            response.data[i]["auth"] = "Protect";
        }
        this.tableData2 = response.data;
      })
      .catch(error => {
        this.$message.error("服务器错误！" + "(" + error + ")");
      });
  },
  methods: {
    blogclick(row, column, cell, event) {
      window.open(row.url);
    },
    rankcolor({ row, rowIndex }) {
      if (rowIndex == 0) return "color:red;font-weight: bold;";
      if (rowIndex == 1) return "color:#BB5E00;font-weight: bold;";
      if (rowIndex == 2) return "color:#E6A23C;font-weight: bold;";
      if (rowIndex == 3) return "color:#930093;font-weight: bold;";
      if (rowIndex == 4) return "color:#409EFF;font-weight: bold;";
      if (rowIndex == 5) return "color:#00CACA;font-weight: bold;";
      if (rowIndex == 6) return "color:#02DF82;font-weight: bold;";
      if (rowIndex == 7) return "color:#67C23A;font-weight: bold;";
      if (rowIndex == 8) return "color:#909399;font-weight: bold;";
      return "color:#303133;font-weight: bold;";
    },
    contestauth(type) {
      if (type == "Public") return "success";
      if (type == "Protect") return "warning";
      if (type == "Private") return "danger";
    },
    contestclick(row, column, cell, event) {
      this.$router.push({
        name: "contestdetail",
        params: { contestID: row.id }
      });
    },
    userclick(row, column, cell, event) {
      this.$router.push({
        name: "user",
        query: { username: row.username }
      });
    }
  }
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
#leveltag {
  text-align: center;
  font-weight: bold;
}
.el-row {
  margin-bottom: 20px;
}
</style>
