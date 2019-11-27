<template>
  <el-card>
    <div slot="header">
      <b>Calendar of All Competitions</b>
    </div>
    <el-table
      :data="tableData"
      @cell-click="contestclick"
      :default-sort="{prop: 'begintime', order: 'descending'}"
    >
      <el-table-column prop="ojName" label="OJ" :width="100"></el-table-column>
      <el-table-column prop="contestName" label="Title"></el-table-column>
      <el-table-column prop="startTime" label="Begin Time"></el-table-column>
      <el-table-column prop="endTime" label="End Time"></el-table-column>
    </el-table>
  </el-card>
</template>

<script>
import moment from "moment";
import contestVue from '../mainpage/contest.vue';
export default {
  name: "ratingrule",
  data() {
    return { tableData: [] };
  },
  created() {
    this.$axios
      .get("/contestcominginfo/"
      )
      .then(response => {
        console.log(response)
        var timestamp=new Date().getTime()
        for (var i = 0; i < response.data.length; i++) {
          if(response.data[i]["startTime"]<timestamp-77330000){
            i--;
            response.data.shift()
            continue;
          }

          response.data[i]["startTime"] = moment(
            response.data[i]["startTime"]
          ).format("YYYY-MM-DD HH:mm:ss");
          response.data[i]["endTime"] = moment(
            response.data[i]["endTime"]
          ).format("YYYY-MM-DD HH:mm:ss");

        }
        this.tableData = response.data;
      });
  },
  methods: {
    contestclick(row, column, cell, event) {
      window.open(row.link)
    }
  }
};
</script>

<style  scoped>
#leveltag {
  text-align: center;
  font-weight: bold;
}
</style>