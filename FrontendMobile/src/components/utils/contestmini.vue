<template>
  <mu-card>
    <mu-card-title title="Calendar of All Competitions"></mu-card-title>
    <mu-card-text>
      <mu-data-table :columns="columns" :data="tableData" @row-click="contestclick">
        <template slot-scope="scope">
          <td>{{scope.row.contestName}}</td>
          <td>{{scope.row.startTime}}</td>
          <td>{{scope.row.endTime}}</td>
        </template>
      </mu-data-table>
    </mu-card-text>
  </mu-card>
</template>

<script>
import moment from "moment";
import contestVue from '../mainpage/contest.vue';
export default {
  name: "ratingrule",
  data() {
    return { 
      tableData: [],
    columns: [
          { title: 'Title', name: 'contestName',width:200 },
          { title: 'Begin Time', name: 'startTime',width:200 },
          { title: 'End Time', name: 'endTime',width:200},
      ],
  };
  },
  created() {
    this.$axios
      .get("/contestcominginfo/"
      )
      .then(response => {
        var timestamp=new Date().getTime()
        for (var i = 0; i < response.data.length; i++) {
          if(response.data[i]["startTime"]<timestamp-77330000){
            i--;
            response.data.shift()
            continue;
          }

          response.data[i]["startTime"] = moment(
            response.data[i]["startTime"]
          ).format("MM-DD HH:mm:ss");
          response.data[i]["endTime"] = moment(
            response.data[i]["endTime"]
          ).format("MM-DD HH:mm:ss");

        }
        this.tableData = response.data;
      })
      .catch(error => {
        this.$toast.error(
          "服务器错误！" + "(" + JSON.stringify(error.response.data) + ")"
        );
      });
  },
  methods: {
    contestclick(index, row, event) {
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