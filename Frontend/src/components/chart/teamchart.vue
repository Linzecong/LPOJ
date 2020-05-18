<template>
  <center>
    <b>
      {{label.school}}
      <br>{{label.des}}
    </b>
    <div ref="myEchart" style="height:500px;width:100%"></div>
  </center>
</template>

<script>
import echarts from "./echarts";
export default {
  name: "teamchart",
  data() {
    return {
      label:{
        school:"Guangdong University of Foreign Studies ACM Training Team",
        des:"Real-time ranking of teams",
      },
      xNum: [],
      yNum: [],
      series: [] // 柱状图
    };
  },
  methods: {
    sortfun(obj1, obj2) {
      //核心代码
      if (obj1["score"] > obj2["score"]) return -1;
      else if (obj1["score"] < obj2["score"]) return 1;
      else if (obj1["score"] == obj2["score"]) {
        if (obj1["teammber"] < obj2["teammber"]) return -1;
        else if (obj1["teammber"] > obj2["teammber"]) return 1;
        else if (obj1["teammber"] == obj2["teammber"]) return 0;
      }
    },
    initChart() {
      let myChart = echarts.init(this.$refs.myEchart);
      myChart.setOption({
        color: ["#409EFF"],
        tooltip: {
          trigger: "axis",
          axisPointer: {
            // 坐标轴指示器，坐标轴触发有效
            type: "shadow" // 默认为直线，可选为：'line' | 'shadow'
          }
        },
        grid: {
          left: "3%",
          right: "4%",
          bottom: "3%",
          containLabel: true
        },
        xAxis: {
          type: "category",
          data: this.xNum,
          axisTick: {
            alignWithLabel: true
          },
          axisLabel: {
            interval: 0,
            rotate: -60
          }
        },
        yAxis: {
          type: "value",
          min: 0,
          interval: 300
        },
        series: this.series
      });
    }
  },
  mounted() {
  
  var sb = this.$store.state.sb
    if( sb ==undefined){
      this.$axios
      .get("/settingboard/")
      .then(res => {
        if (res.data.length > 0) this.label.school = res.data[0].schoolname;
        else this.label.school = "University";
        this.$store.state.sb = res.data
      })
      .catch(error => {
        this.$message.error(
          "服务器错误！" + "(" + JSON.stringify(error.response.data) + ")"
        );
      });
    }
    else{
      if (sb.length > 0) this.label.school = sb[0].schoolname;
        else this.label.school = "University";
    }
      
    this.$axios
      .get("/teamboard/")
      .then(response => {
        this.series.push({
          type: "bar",
          data: [],
          name: "得分：",
          barWidth: "50%"
        });
        var Xnames = new Set();

        for (var i = 0; i < response.data.length; i++) {
          Xnames.add(response.data[i]["teammember"]);
        }

        var data = [];

        for (var name2 of Xnames) {
          this.xNum.push(name2);
          this.series[0].data.push(0);
          data.push({ teammber: name2, score: 0 });
        }

        for (var i = 0; i < response.data.length; i++) {
          for (var j = 0; j < this.xNum.length; j++) {
            if (this.xNum[j] == response.data[i]["teammember"]) {
              data[j].score += response.data[i]["score"];
            }
          }
        }

        data.sort(this.sortfun);

        for (var i = 0; i < data.length; i++) {
          this.xNum[i] = data[i].teammber;
          this.series[0].data[i] = data[i].score;
        }

        let obj = this.$refs.myEchart;
        if (obj) {
          this.initChart();
        }
      })
      .catch(error => {
        this.$message.error(
          "服务器出错！" + JSON.stringify(error.response.data)
        );
      });
  }
};
</script>

<style  scoped>
</style>