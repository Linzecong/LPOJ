<template>
  <el-row>
    <el-dialog :visible.sync="statusshow" @opened="setstatus" :show-close="false">
      <statusmini ref="Status"></statusmini>
    </el-dialog>

    <center>
      <h1>{{ contesttitle }}</h1>
    </center>
    <el-row :gutter="10">
      <el-table
        :data="tableData"
        :cell-style="cellstyle"
        border
        stripe
        size="small"
        @cell-click="cellclick"
      >
        <el-table-column prop="rank" label="Rank" width="70px" fixed></el-table-column>
        <el-table-column prop="user" label="User" fixed></el-table-column>
        <el-table-column prop="nickname" label="Nickname" fixed></el-table-column>
        <el-table-column prop="solved" label="Solve" fixed></el-table-column>
        <el-table-column prop="time" label="Time"></el-table-column>
        <el-table-column
          v-for="(item,index) in probleminfo"
          :key="index"
          :prop="item.prop"
          :label="item.label"
          style="white-space: pre-line;"
        >
          <template slot-scope="scope">
            <div style="white-space:pre-line;">{{scope.row[item.prop]}}</div>
          </template>
        </el-table-column>
      </el-table>
    </el-row>
  </el-row>
</template>

<script>
import statusmini from "@/components/statusmini";
export default {
  name: "contestrank",
  components: {
    statusmini
  },
  data() {
    return {
      problemcount: this.$store.state.contestproblemcount,
      contesttitle: this.$store.state.contesttitle,
      contestid: this.$route.params.contestID,
      probleminfo: [],
      tableData: [],
      problemids: [],
      statusdata: {
        user: "",
        contest: this.$route.params.contestID,
        problemid: ""
      },
      statusshow: false
    };
  },
  created() {
    //this.setproblemcount(this.$route.params.contestID);
  },
  methods: {
    sortByProperty(p1, p2) {
      function sortfun(obj1, obj2) {
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
    toChar(val) {
      var A = "A";
      return String.fromCharCode(val + A.charCodeAt());
    },
    cellclick(row, column, cell, event) {
      if (column.property.length > 1) return;
      var A = "A";
      this.statusdata.user = row.user;
      this.statusdata.problemid = this.problemids[
        column.property.charCodeAt() - A.charCodeAt()
      ];

      this.statusshow = true;
    },
    setstatus() {
      //console.log(this.statusdata.user,this.statusdata.problemid)
      this.$refs.Status.setstatus(
        this.statusdata.problemid,
        this.statusdata.user
      );
    },
    cellstyle(data) {
      var id = data.columnIndex - 5;
      var str = this.toChar(id);
      if (id < 0) return "background-color:white;text-align:center;";
      if (data.row[str].indexOf("❤") > -1)
        return "background-color:#009100;text-align:center;font-weight:bold;color:white;";
      if (data.row[str].indexOf(":") > -1)
        return "background-color:#79FF79;text-align:center";
      if (data.row[str].indexOf("(") > -1)
        return "background-color:#F56C6C;text-align:center";

      return "background-color:white";
    },
    setproblemcount(id) {
      this.contesttitle = this.$store.state.contesttitle;
      this.$axios.get("/contestproblem/?contestid=" + id).then(response3 => {
        this.$store.state.contestproblemcount = response3.data.length;
        this.problemcount = this.$store.state.contestproblemcount;
        this.probleminfo = [];
        for (var i = 0; i < response3.data.length; i++) {
          this.probleminfo.push({
            prop: this.toChar(i),
            label: this.toChar(i)
          });
          this.problemids.push(response3.data[i].problemid);
        }
        this.$axios.get("/contestboard/?contestid=" + id).then(response => {
          var data = [];
          // 读取所有有提交的用户
          //console.log(this.$store.state.contestbegintime)
          var proac = [];
          var prosub = [];
          for (var iii = 0; iii < this.problemcount; iii++) proac.push(0);
          for (var iiii = 0; iiii < this.problemcount; iiii++) prosub.push(0);

          var nameset = new Set();
          for (let index = 0; index < response.data.length; index++)
            nameset.add(response.data[index].username+"|"+response.data[index].user);

          for (var na of nameset) {
            var k = {
              user: na.split("|")[0],
              nickname: na.split("|")[1],
              solved: 0,
              time: 0,
              sorttime: 0
            };

            for (var j = 0; j < this.probleminfo.length; j++) {
              k[this.probleminfo[j].prop] = "";
            }

            var count = 0;
            var t = 0;

            for (var ii = 0; ii < this.probleminfo.length; ii++) {
              var tmp = [5552304570991, 0];

              let isac = false;
              for (let index = 0; index < response.data.length; index++) {
                if (
                  response.data[index].username == na.split("|")[0] &&
                  response.data[index].problemrank == ii
                ) {
                  if (parseInt(response.data[index]["type"]) == 1) {
                    isac = true;
                    if (parseInt(response.data[index]["submittime"]) < tmp[0])
                      tmp[0] = parseInt(response.data[index]["submittime"]);
                  }
                }
              }

              for (let index = 0; index < response.data.length; index++) {
                if (
                  response.data[index].username == na.split("|")[0] &&
                  response.data[index].problemrank == ii
                ) {
                  if (parseInt(response.data[index]["type"]) == 0) {
                    if (parseInt(response.data[index]["submittime"]) < tmp[0])
                      tmp[1]--;
                  }
                }
              }

              if (isac == true) {
                proac[ii]++;
                prosub[ii]++;

                count++;

                tmp[0] = parseInt(tmp[0]);
                tmp[1] = parseInt(tmp[1]);
                var cha = parseInt(
                  (tmp[0] - this.$store.state.contestbegintime) / 1000
                );
                t += cha;
                t += -tmp[1] * 20 * 60;
                var tt =
                  parseInt(cha / 60 / 60) +
                  ":" +
                  parseInt((cha / 60) % 60) +
                  ":" +
                  parseInt((cha % 60) % 60);

                if (tmp[1] < 0) {
                  k[this.toChar(ii)] = "(" + tmp[1] + ")\n" + tt;
                  prosub[ii] = prosub[ii] - tmp[1];
                } else k[this.toChar(ii)] = tt;
              } else {
                tmp[1] = parseInt(tmp[1]);

                if (tmp[1] < 0) {
                  k[this.toChar(ii)] = "(" + tmp[1] + ")";
                  prosub[ii] = prosub[ii] - tmp[1];
                }
              }
            }

            k["solved"] = count;
            var ttt =
              parseInt(t / 60 / 60) +
              ":" +
              parseInt((t / 60) % 60) +
              ":" +
              parseInt((t % 60) % 60);
            k["time"] = ttt;
            k["sorttime"] = t;

            data.push(k);
          }

          data.sort(this.sortByProperty("solved", "sorttime"));
          for (var i = 0; i < data.length; i++) {
            data[i]["rank"] = i + 1;
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

          for (var id = 0; id < this.problemcount; id++) {
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
            }
          }

          this.tableData = data;
        });
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
