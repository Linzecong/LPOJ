<template>
  <el-card>
    <div slot="header">
      <b>7 Days AC Rank</b>
    </div>
    <el-table
      :data="tableData"
      border
      style="width: 100%"
      @cell-click="userclick"
      size="mini"
      :default-sort="{prop: 'acnum', order: 'descending'}"
      :row-style="rowcolor"
    >
      <el-table-column type="index" width="40"></el-table-column>
      <el-table-column prop="user" label="User"></el-table-column>
      <el-table-column prop="acnum" label="AC"></el-table-column>
    </el-table>
  </el-card>
</template>

<script>
export default {
  name: "acrank",
  data() {
    return {tableData:[]};
  },
  methods: {
    sortfun(obj1, obj2) {
      if (obj1["acnum"] > obj2["acnum"]) return -1;
      else if (obj1["acnum"] < obj2["acnum"]) return 1;
      else if (obj1["acnum"] == obj2["acnum"]) {
        if (obj1["user"] < obj2["user"]) return -1;
        else if (obj1["user"] > obj2["user"]) return 1;
        else if (obj1["user"] == obj2["user"]) return 0;
      }
    },
    userclick(row, column, cell, event) {
      this.$router.push({
        name: "user",
        query: { username: row.user }
      });
    },
    rowcolor({ row, rowIndex }) {
      if (rowIndex == 0) return "color:red;font-weight: bold;";
      if (rowIndex == 1) return "color:#BB5E00;font-weight: bold;";
      if (rowIndex == 2) return "color:#E6A23C;font-weight: bold;";
      if (rowIndex == 3) return "color:#930093;font-weight: bold;";
      if (rowIndex == 4) return "color:#0000AA;font-weight: bold;";
      if (rowIndex == 5) return "color:#007799;font-weight: bold;";
      if (rowIndex == 6) return "color:#227700;font-weight: bold;";
      if (rowIndex == 7) return "color:#67C23A;font-weight: bold;";
      if (rowIndex == 8) return "color:#909399;font-weight: bold;";
      return "color:#303133;font-weight: bold;";
    },
  },
  created() {
    this.$axios
      .get("/acrank/")
      .then(response => {

        var mydata = {}
        var userac = {}
        for(var i=0;i<response.data.length;i++){
            mydata[response.data[i].user]=[]
            userac[response.data[i].user]=0
        }

        for(var i=0;i<response.data.length;i++){
            var flag=0;
            for(var j = 0;j<mydata[response.data[i].user].length;j++){
              if(mydata[response.data[i].user][j]==response.data[i]["problem"]){
                flag = 1;
                break;
              }
            }
           if(flag==0)
           {
              mydata[response.data[i].user].push(response.data[i]["problem"])
              userac[response.data[i].user] = userac[response.data[i].user] + 1
          }
        }
        console.log(mydata)


        var sorted = []
        for (var key in userac) {
        　　var item = userac[key];
            sorted.push({"user":key,"acnum":item})
        }
        sorted.sort(this.sortfun)
        
        console.log(sorted)

        for(var i=0;i<(sorted.length>=10?10:sorted.length);i++){
          this.tableData.push({"user":sorted[i]["user"],"acnum":sorted[i]["acnum"]})
        }


      });
  }
};
</script>

<style  scoped>
</style>