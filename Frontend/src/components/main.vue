<template>
  <el-row :gutter="12">
    <el-col :span="6">
      <el-row :gutter="10">
        <el-card>
          <h3>{{ msg }}</h3>
          <h3>当前版本：1.1</h3>
          <h3>支持语言：C/C++/Java</h3>
        </el-card>
        <el-card style="margin-top:10px">
          <h3>Top User</h3>
          <el-table :data="tableData" border style="width: 100%" @cell-click="userclick" size="mini" :row-style="rankcolor">
            <el-table-column type="index" width="40"></el-table-column>
            <el-table-column prop="username" label="User"></el-table-column>
            <el-table-column prop="score" label="Score"></el-table-column>
          </el-table>
        </el-card>
      </el-row>
    </el-col>
    <el-col :span="18">
      <el-card>
        <rankchart></rankchart>
      </el-card>
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
    </el-col>
  </el-row>
</template>

<script>
import moment from "moment";
import rankchart from "@/components/rankchart";
export default {
  components: {
    rankchart
  },
  name: "main",
  data() {
    return {
      msg: "欢迎来到LPOJ",
      tableData: [],
      tableData2: []
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
      .get("/contestcominginfo/")
      .then(response => {
        for(var i = 0 ;i<response.data.length;i++){
          response.data[i]["begintime"] = moment(
              response.data[i]["begintime"]
            ).format("YYYY-MM-DD HH:mm:ss");
            response.data[i]["lasttime"] =
             parseInt(response.data[i]["lasttime"] / 60 / 60) +
              ":" +
              parseInt(((response.data[i]["lasttime"] / 60) % 60)) +
              ":" +
              parseInt(((response.data[i]["lasttime"] % 60) % 60));

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
    rankcolor({row,rowIndex}){
      if(rowIndex==0)
        return "color:red;font-weight: bold;"
      if(rowIndex==1)
        return "color:#BB5E00;font-weight: bold;"
      if(rowIndex==2)
        return "color:#E6A23C;font-weight: bold;"
      if(rowIndex==3)
        return "color:#930093;font-weight: bold;"
      if(rowIndex==4)
        return "color:#409EFF;font-weight: bold;"
      if(rowIndex==5)
        return "color:#00CACA;font-weight: bold;"
      if(rowIndex==6)
        return "color:#02DF82;font-weight: bold;"
      if(rowIndex==7)
        return "color:#67C23A;font-weight: bold;"
      if(rowIndex==8)
        return "color:#909399;font-weight: bold;"
      return "color:#303133;font-weight: bold;"
      
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
