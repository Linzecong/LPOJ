<template>
  <el-card>
    <el-dialog :visible.sync="dialogVisible">
      <el-row :gutter="10">
        <el-col :span="3">
          <div style="text-align:center;margin:5px;">留言</div>
        </el-col>
        <el-col :span="18">
          <el-input v-model="msg" autocomplete="off" type="textarea"></el-input>
        </el-col>
        <el-col :span="3">
          <el-button size="mini" @click="addcomment" type="primary">提交</el-button>
        </el-col>
      </el-row>
    </el-dialog>
        <div slot="header">
            <b>留言与建议板</b>
          </div>
    
    <el-table :data="tableData" border style="width: 100%" size="mini" :row-style="ratingcolor">
      <el-table-column prop="username" label="User"></el-table-column>
      <el-table-column prop="msg" align="right">
        <template slot="header" slot-scope="scrop">
          <el-button size="mini" @click="dialogVisible = true" type="primary">留言</el-button>
        </template>
      </el-table-column>
    </el-table>
    <el-pagination
      @size-change="handleSizeChange"
      @current-change="handleCurrentChange"
      :current-page="currentpage"
      :page-sizes="[10, 20, 30, 50]"
      :page-size="pagesize"
      layout="total,pager"
      :total="totalmsg"
    ></el-pagination>
  </el-card>
</template>

<script>
import moment from "moment";
export default {
  name: "ojmessage",
  data() {
    return {
      msg:"",
      tableData: [],
      currentpage: 1,
      pagesize: 10,
      totalmsg: 10,
      dialogVisible: false
    };
  },
  created() {
    this.getdata();
  },
  methods: {
    ratingcolor({row, rowIndex}){
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
    addcomment() {
      if(localStorage.username==""){
        this.$message.error("请先登录！");
        return
      }
      this.$axios
        .post(
          "/ojmessage/",{
            username:localStorage.username,
            msg:this.msg,
            rating: parseInt(localStorage.rating)
          }
        )
        .then(response => {
          this.$message.success("提交成功！");
          this.dialogVisible = false;
          this.getdata()
        })
        .catch(error => {
          this.$message.error("服务器错误！" + error);
        });
    },
    handleSizeChange(val) {
      this.pagesize = val;
    },
    handleCurrentChange(val) {
      this.currentpage = val;
      this.getdata();
    },
    getdata() {
      this.$axios
        .get(
          "/ojmessage/" +
            "?limit=" +
            this.pagesize +
            "&offset=" +
            (this.currentpage - 1) * this.pagesize
        )
        .then(response => {
          this.tableData = response.data.results;
          this.totalmsg = response.data.count;
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
