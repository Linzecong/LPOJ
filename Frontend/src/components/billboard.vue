<template>
<el-card>
  
    <el-dialog title="申报" :visible.sync="dialogVisible">
      <el-form :model="form">
        <el-row :gutter="10">
          <el-col :span="3">
            <div style="text-align:center;margin:5px;">姓名</div>
          </el-col>
          <el-col :span="12">
            <el-input v-model="form.username" placeholder="真实姓名"></el-input>
          </el-col>
        </el-row>
        <el-row :gutter="10">
          <el-col :span="3">
            <div style="text-align:center;margin:5px;">申请AC题目数</div>
          </el-col>
          <el-col :span="12">
            <el-input v-model="form.count" placeholder="添整数"></el-input>
          </el-col>
        </el-row>
        <el-row :gutter="10">
          <el-col :span="3">
            <div style="text-align:center;margin:5px;">证明</div>
          </el-col>
          <el-col :span="12">
            <el-input v-model="form.msg" placeholder="填入必要的证明，如比赛网址和你的比赛ID"></el-input>
          </el-col>
        </el-row>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="dialogVisible = false">取 消</el-button>
        <el-button type="primary" @click="PushOtherClick">确 定</el-button>
      </div>
    </el-dialog>

    <center>
      <h3>广东外语外贸大学 ACM集训队排名<el-button @click="dialogVisible = true" type="primary" style="float:right;margin:10px;">其他申报</el-button></h3>
    </center>

      <el-table :data="tableData" border stripe>
        <el-table-column prop="username" label="User" fixed></el-table-column>
        
        <!-- <el-table-column prop="classes" label="Class" fixed></el-table-column> -->
        <el-table-column prop="number" label="Number" fixed></el-table-column>
        <el-table-column
          v-for="(item,index) in boardinfo"
          :key="index"
          :prop="item.prop"
          :label="item.label"
          style="white-space: pre-line;"
        >
          <template slot-scope="scope">
            <div style="white-space:pre-line;">{{scope.row[item.prop]}}</div>
          </template>
        </el-table-column>

        <el-table-column prop="total" label="AC/Submit" fixed></el-table-column>
      </el-table>
   
  
</el-card>
</template>

<script>
export default {
  name: "billboard",
  data() {
    return {
      dialogVisible:false,
      ojcount: 3,
      boardinfo: [],
      tableData: [{}],
      form:{
          username:"",
          count:0,
          msg:""
      }
    };
  },
  created() {
    this.setdata();
  },
  methods: {
      PushOtherClick(){
           this.$axios.post("/otherssubmit/",this.form).then(response => {
               this.dialogVisible=false
               this.$message({
          message: "提交成功！",
          type: "success"
        });
           }).catch(error=>{
               this.$message.error("服务器错误！请联系管理员！"+error)
           });

      },
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

    setdata() {
      this.$axios.get("/board/").then(response => {
        this.ojcount = response.data[0]["OJCount"];

        this.boardinfo = [];
        var oj = response.data[0]["OJ"];
        var props = oj.split("|");
        for (var i = 0; i < props.length; i++) {
          this.boardinfo.push({ prop: props[i], label: props[i] });
        }
        var data = []
        for (var i = 0; i < response.data.length; i++) {
          var k = {
            username: response.data[i]["username"],
            number: response.data[i]["number"],
            classes: response.data[i]["classes"],
            ac: 0,
            total: "0/0"
          };

          for (var j = 0; j < this.boardinfo.length; j++) {
            k[this.boardinfo[j].prop] = "";
          }

          var acnum = 0;
          var subnum = 0;
          var acli = response.data[i]["acnum"].split("|");
          var subli = response.data[i]["submitnum"].split("|");
          for (var jj = 0; jj < this.boardinfo.length; jj++) {
            k[this.boardinfo[jj].prop] = acli[jj] + "/" + subli[jj];
            acnum = acnum + parseInt(acli[jj]);
            subnum = subnum + parseInt(subli[jj]);
          }
          k["ac"] = acnum;
          k["sub"] = subnum;
          k["total"] = acnum + "/" + subnum;

          data.push(k);
        }
        data.sort(this.sortByProperty("ac", "sub"));

        this.tableData = data;
      });
    }
  }
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>
