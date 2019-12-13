<template>
  <el-card>
    <div slot="header">
      <b>Codeforces Ratings</b>
    </div>
    <el-table
      :data="tableData"
      border
      style="width: 100%"
      size="mini"
      :row-style="ratingcolor"
    >
      <el-table-column type="index" width="40"></el-table-column>
      <el-table-column prop="username" label="User" width="100"></el-table-column>
      <el-table-column prop="cfratestr" label="Rate"></el-table-column>
    </el-table>
  </el-card>
</template>

<script>
export default {
  name: "topuser",
  data() {
    return {tableData:[]};
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
    ratingcolor({ row, rowIndex }) {
      if (row.cfrate >= 2400) return "color:red;font-weight: bold;";
      if (row.cfrate >= 2300) return "color:#BB5E00;font-weight: bold;";
      if (row.cfrate >= 2100) return "color:#E6A23C;font-weight: bold;";
      if (row.cfrate >= 1900) return "color:#930093;font-weight: bold;";
      if (row.cfrate >= 1600) return "color:#0000AA;font-weight: bold;";
      if (row.cfrate >= 1400) return "color:#007799;font-weight: bold;";
      if (row.cfrate >= 1200) return "color:#227700;font-weight: bold;";
      return "color:#909399;font-weight: bold;";
    }
  },
  created() {
    this.$axios
      .get("/board/")
      .then(response => {

        var tot = 0
        for(let i =0;i<response.data.length;i++){
          var ls = response.data[i].cfrate.split("|")
          tot = tot + parseInt(ls[2])
          response.data[i]["cfratestr"] = ""
        }
        tot = parseInt(tot / response.data.length)

        if(tot>0)
          tot = 0

        for(let i =0;i<response.data.length;i++){
          var ls = response.data[i].cfrate.split("|")

          var score = parseInt(ls[0])

          response.data[i].cfrate = score
          
          response.data[i]["cfratestr"] = score
          
          
        }
            
        
        response.data.sort(this.sortByProperty("cfrate", "username"));

        this.tableData = response.data;
      });
  }
};
</script>

<style  scoped>
</style>