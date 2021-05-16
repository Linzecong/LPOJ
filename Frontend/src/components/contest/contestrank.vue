<template>
  <el-row>
    <el-dialog :visible.sync="statusshow"
               @opened="setstatus"
               :show-close="false"
               @closed="statusclosed">
      <statusmini ref="Status"></statusmini>
    </el-dialog>

    <center>
      <h1>{{ contesttitle }}</h1>
      <h2>{{ isboardlock }}</h2>
    </center>

    <el-form :inline="true"
             :model="filterform"
             v-if="isadmin">
      <el-form-item label="学校">
        <el-input v-model="filterform.school"
                  placeholder="school"></el-input>
      </el-form-item>
      <el-form-item label="专业">
        <el-input v-model="filterform.course"
                  placeholder="course"></el-input>
      </el-form-item>
      <el-form-item label="班级">
        <el-input v-model="filterform.class"
                  placeholder="class"></el-input>
      </el-form-item>
      <el-form-item>
        <el-button type="primary"
                   @click="onfilterboard">查询</el-button>
      </el-form-item>
    </el-form>

    <el-row :gutter="10">
      <el-table :data="tableData"
                :cell-style="cellstyle"
                border
                stripe
                size="small"
                @cell-click="cellclick"
                :row-style="ratingcolor"
                id="out-table">
        <el-table-column type="index"
                         width="45"
                         fixed></el-table-column>
        <el-table-column prop="user"
                         label="User"
                         fixed></el-table-column>
        <el-table-column prop="nickname"
                         label="Nickname"
                         fixed></el-table-column>
        <el-table-column prop="score"
                         :label="SolveLabel"
                         fixed></el-table-column>
        <el-table-column prop="time"
                         label="Time"></el-table-column>
        <el-table-column v-for="(item, index) in probleminfo"
                         :key="index"
                         :prop="item.prop"
                         :label="item.label"
                         style="white-space: pre-line;">
          <template slot-scope="scope">
            <div style="white-space:pre-line;">{{ scope.row[item.prop] }}</div>
          </template>
        </el-table-column>
      </el-table>
      <br />
      <el-button type="primary"
                 @click="exportExcel">点击导出</el-button>
      <br />
    </el-row>
  </el-row>
</template>

<script>
import FileSaver from "file-saver";
import XLSX from "xlsx";
import statusmini from "@/components/utils/statusmini";
export default {
  name: "contestrank",
  components: {
    statusmini
  },
  data () {
    return {
      problemcount: this.$store.state.contestproblemcount,
      contesttitle: this.$store.state.contesttitle,
      contestid: this.$route.params.contestID,
      isboardlock: "",
      probleminfo: [],
      tableData: [],
      problemids: [],
      statusdata: {
        user: "",
        contest: this.$route.params.contestID,
        problemid: ""
      },
      statusshow: false,
      SolveLabel: "Solved",

      filterform: {
        contestid: this.$route.params.contestID,
        school: "",
        course: "",
        class: ""
      },
      isadmin: false,
    };
  },
  created () {
    this.isadmin = sessionStorage.type == 2 || sessionStorage.type == 3;
    //this.setproblemcount(this.$route.params.contestID);
  },
  methods: {
    exportExcel () {
      /* 从表生成工作簿对象 */
      var wb = XLSX.utils.table_to_book(document.querySelector("#out-table"));
      /* 获取二进制字符串作为输出 */
      var wbout = XLSX.write(wb, {
        bookType: "xlsx",
        bookSST: true,
        type: "array"
      });
      try {
        FileSaver.saveAs(
          //Blob 对象表示一个不可变、原始数据的类文件对象。
          //Blob 表示的不一定是JavaScript原生格式的数据。
          //File 接口基于Blob，继承了 blob 的功能并将其扩展使其支持用户系统上的文件。
          //返回一个新创建的 Blob 对象，其内容由参数中给定的数组串联组成。
          new Blob([wbout], { type: "application/octet-stream" }),
          //设置导出文件名称
          "contestrank.xlsx"
        );
      } catch (e) {
        if (typeof console !== "undefined") console.log(e, wbout);
      }
      return wbout;
    },

    sortByProperty (p1, p2) {
      function sortfun (obj1, obj2) {
        //核心代码
        if (obj1[p1] > obj2[p1]) return -1;
        else if (obj1[p1] < obj2[p1]) return 1;
        else if (obj1[p1] == obj2[p1]) {
          if (obj1[p2] < obj2[p2]) return -1;
          else if (obj1[p2] > obj2[p2]) return 1;
          else if (obj1[p2] == obj2[p2]) return 0;
        }
      }
      return sortfun;
    },
    toChar (val) {
      var A = "A";
      return String.fromCharCode(val + A.charCodeAt());
    },
    cellclick (row, column, cell, event) {
      if (column.property.length > 1) return;
      var A = "A";
      this.statusdata.user = row.user;
      this.statusdata.problemid = this.problemids[
        column.property.charCodeAt() - A.charCodeAt()
      ];
      if (row.nickname.indexOf("[Clone]") > -1)
        this.statusdata.contest = this.$store.state.contestfrom;
      else this.statusdata.contest = this.$route.params.contestID;

      this.statusshow = true;
    },
    statusclosed () {
      this.$refs.Status.setstatus("0", "|#)", "-1");
    },
    setstatus () {
      this.$refs.Status.setstatus(
        this.statusdata.problemid,
        this.statusdata.user,
        this.statusdata.contest
      );
    },
    ratingcolor ({ row, rowIndex }) {
      if (row.nickname.indexOf("[Clone]") > -1) return "color:#AAAAAA";
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
    cellstyle (data) {
      var id = data.columnIndex - 5;
      var str = this.toChar(id);
      if (id < 0) return "background-color:white;text-align:center;";
      if (data.row[str].indexOf("❤") > -1)
        return "background-color:#009100;text-align:center;font-weight:bold;color:white;";
      if (data.row[str].indexOf(":") > -1)
        return "background-color:#79FF79;text-align:center;color:black;";
      if (data.row[str].indexOf("Submit") > -1)
        return "background-color:purple;text-align:center;color:black;";
      if (data.row[str].indexOf("(") > -1)
        return "background-color:#F56C6C;text-align:center;color:black;";
      
      return "background-color:white";
    },

    onfilterboard () {
      this.setproblemcount(this.$route.params.contestID);
    },

    setproblemcount (cid) {
      if (this.$store.state.contesttype == "Rated") this.SolveLabel = "Score";

      this.contesttitle = this.$store.state.contesttitle;
      this.$axios.get("/contestproblem/?contestid=" + cid).then(response3 => {
        this.$store.state.contestproblemcount = response3.data.length;
        this.problemcount = this.$store.state.contestproblemcount;
        this.probleminfo = [];
        for (let i = 0; i < response3.data.length; i++) {
          this.probleminfo.push({
            prop: this.toChar(i),
            label: this.toChar(i)
          });
          this.problemids.push(response3.data[i].problemid);
        }

        this.setboard(cid, { data: [] });

      });
    },

    setboard (cid, response) {
      this.$axios.post("/isboardlock/", {
        contestid:this.$route.params.contestID
      }).then(res1 => {
        if(res1.data == "yes"){
          this.isboardlock = "当前封榜中...封榜后提交显示为Pending，榜单只显示提交次数..."
        }
      })

      this.$axios.post("/contestfilterboard/", this.filterform).then(res1 => {
        for (let i = 0; i < res1.data.length; i++) {
          response.data.push(res1.data[i]);
        }

        var data = [];

        //初始化每道题目的AC/Sub数
        var proac = [];
        var prosub = [];
        for (var iii = 0; iii < this.problemcount; iii++) proac.push(0);
        for (var iiii = 0; iiii < this.problemcount; iiii++) prosub.push(0);

        //获取所有提交，提取出参加比赛的有哪些人
        var nameset = new Set();
        var namevis = { "!!!": 1 };
        for (let index = 0; index < response.data.length; index++) {
          // if(response.data[index].username=="admin") //这里可以排除某些用户！
          //   continue;
          nameset.add(
            response.data[index].username + "|" + response.data[index].user
          );
          namevis[
            response.data[index].username + "|" + response.data[index].user
          ] = 0;
        }



        //遍历每一个人，计算每一个人的信息
        for (var na of nameset) {
          //初始化参赛者信息

          var username = na.split("|")[0];
          var nickname = na.split("|")[1];
          //去重
          if (namevis[na] == 1) continue;
          namevis[na] = 1;

          var PaticipantData = {
            user: username,
            nickname: nickname,
            score: 0,
            time: 0,
            sorttime: 0
          };
          for (var j = 0; j < this.probleminfo.length; j++) {
            PaticipantData[this.probleminfo[j].prop] = "";
          }

          //需要单独计算的信息
          var ACNum = 0;
          var Score = 0;
          var FaShi = 0;

          //计算每道题目的信息

          var ProblemDataList = [];
          for (var ii = 0; ii < this.probleminfo.length; ii++)
            ProblemDataList.push([5552304570991, 0, 0]); //第一个代表AC时间，第二个代表罚时次数，第三个代表提交次数

          //找出每一道题AC的时间
          for (let index = 0; index < response.data.length; index++) {
            if (
              response.data[index].username == username &&
              response.data[index].user == nickname
            ) {

              PaticipantData["rating"] = response.data[index].rating;
              if (parseInt(response.data[index]["type"]) == 1) {
                let time = ProblemDataList[response.data[index].problemrank][0];
                if (parseInt(response.data[index]["submittime"]) < time)
                  ProblemDataList[
                    response.data[index].problemrank
                  ][0] = parseInt(response.data[index]["submittime"]);
              }
              ProblemDataList[response.data[index].problemrank][2] = ProblemDataList[response.data[index].problemrank][2] + 1
            }
          }

          //找出每一道题AC前的提交次数，作为罚时
          for (let index = 0; index < response.data.length; index++) {
            if (
              response.data[index].username == username &&
              response.data[index].user == nickname
            ) {
              if (parseInt(response.data[index]["type"]) == 0) {
                if (
                  parseInt(response.data[index]["submittime"]) <
                  ProblemDataList[response.data[index].problemrank][0]
                )
                  ProblemDataList[response.data[index].problemrank][1]--;
              }
            }
          }

          //计算每一道题的信息
          for (var ii = 0; ii < this.probleminfo.length; ii++) {
            var ProblemScore = 0;
            if (ii == 0) ProblemScore = 1000;
            else if (ii == 1) ProblemScore = 1500;
            else if (ii == 2) ProblemScore = 1600;
            else ProblemScore = 2000;

            //如果AC了
            if (ProblemDataList[ii][0] != 5552304570991) {
              proac[ii]++;
              prosub[ii]++;
              ACNum++;

              //计算罚时
              var ACTime = parseInt(ProblemDataList[ii][0]);
              var FaShiNum = parseInt(ProblemDataList[ii][1]);
              var cha = parseInt(
                (ACTime - this.$store.state.contestbegintime) / 1000
              );

              Score +=
                ProblemScore -
                (((cha / 60.0) * (0.7 / (ii + 1))) / 100.0) * ProblemScore;

              FaShi += cha;
              FaShi += -FaShiNum * 20 * 60;
              var actime =
                parseInt(cha / 60 / 60) +
                ":" +
                parseInt((cha / 60) % 60) +
                ":" +
                parseInt((cha % 60) % 60);

              //表格中需要显示的信息
              if (FaShiNum < 0) {
                PaticipantData[this.toChar(ii)] =
                  "(" + FaShiNum + ")\n" + actime;
                prosub[ii] = prosub[ii] - FaShiNum;
                Score += 20 * FaShiNum;
              } else PaticipantData[this.toChar(ii)] = actime;
            } else {
              //表格中需要显示的信息
              var FaShiNum = parseInt(ProblemDataList[ii][1]);
              if (FaShiNum < 0) {
                PaticipantData[this.toChar(ii)] = "(" + FaShiNum + ")";
                prosub[ii] = prosub[ii] - FaShiNum;

                var afternum = ProblemDataList[ii][2] + FaShiNum
                if(afternum > 0)
                  PaticipantData[this.toChar(ii)] = PaticipantData[this.toChar(ii)] + "\n" + String(afternum) + " Submit";
              }
              else // 还没有判题或者封榜消息（-1和2）
              {
                if(ProblemDataList[ii][2]!=0)
                  PaticipantData[this.toChar(ii)] = String(ProblemDataList[ii][2]) + " Submit";
              }
            }
          }
          PaticipantData["score"] =
            this.$store.state.contesttype == "Rated"
              ? parseInt(Score < 0 ? 0 : Score)
              : parseInt(ACNum);

          var TimeTotal =
            parseInt(FaShi / 60 / 60) +
            ":" +
            parseInt((FaShi / 60) % 60) +
            ":" +
            parseInt((FaShi % 60) % 60);
          PaticipantData["time"] = TimeTotal; //排行榜上显示的
          PaticipantData["sorttime"] = FaShi; //用于分数相同时排序的

          data.push(PaticipantData);
        }

        //计算排行榜顶部的ac/sub
        for (var proi = 0; proi < this.problemcount; proi++)
          this.probleminfo[proi].label =
            this.probleminfo[proi].label +
            " ( " +
            proac[proi] +
            " / " +
            prosub[proi] +
            " )";

        //查找FB
        for (var id = 0; id < this.problemcount; id++) {
          var ProblemScore = 0;
          if (id == 0) ProblemScore = 1000;
          else if (id == 1) ProblemScore = 1500;
          else if (id == 2) ProblemScore = 1600;
          else ProblemScore = 2000;

          var pro = this.toChar(id);
          var index = -1;
          var minn = 100000000000000;
          for (var i = 0; i < data.length; i++) {
            if (data[i][pro].indexOf(":") > 0) {
              if (data[i][pro].indexOf("(") < 0) {
                var li = data[i][pro].split(":");
                var time =
                  parseInt(li[0]) * 3600 +
                  parseInt(li[1]) * 60 +
                  parseInt(li[2]);
                if (time < minn) {
                  minn = time;
                  index = i;
                }
              } else {
                var tmp = data[i][pro].split(")");

                var li = tmp[1].split(":");
                var time =
                  parseInt(li[0]) * 3600 +
                  parseInt(li[1]) * 60 +
                  parseInt(li[2]);
                tmp = tmp[0].split("(");
                if (time < minn) {
                  minn = time;
                  index = i;
                }
              }
            }
          }
          if (index != -1) {
            data[index][pro] = data[index][pro] + "\n❤";
            if (this.$store.state.contesttype == "Rated")
              data[index]["score"] += parseInt(ProblemScore / 10);
          }
        }
        data.sort(this.sortByProperty("score", "sorttime"));
        this.tableData = data;
      });
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
