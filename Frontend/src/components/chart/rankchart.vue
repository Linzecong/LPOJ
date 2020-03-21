<template>
  <center>
    <b>
      {{label.school}}
      <br>{{label.des}}
    </b>
    <h2></h2>
    <el-button size="mini" @click="seeall" type="primary">{{label.seeall}}</el-button><el-button style="margin-left:15px;" size="mini" @click="seeallblog" type="primary">{{label.viewblog}}</el-button>
    <h2></h2>
    <div ref="myEchart" style="height:550px;width:100%"></div>
  </center>
</template>

<script>
import echarts from "./echarts";

export default {
  name: "rankchart",
  data() {
    return {
      label:{
        school:"Guangdong University of Foreign Studies ACM Training Team",
        des:"New AC statistics in 10 days",

        seeall:"View all",
        viewblog:"View Blog"
      },
      xNum: [],
      yNum: [],
      series: [] // 折线图数据
    };
  },
  methods: {
    seeallblog(){
      this.$router.push({
        name: "blog"
      });
    },
    seeall() {
      this.$router.push({
        name: "billboard"
      });
    },
    initChart() {
      let myChart = echarts.init(this.$refs.myEchart);
      myChart.setOption({
        tooltip: {
          trigger: "axis",
          confine: true,
          textStyle: {
            fontSize: 8
          },
          formatter: function(parmas) {
            var func = function sortfun(obj1, obj2) {
              //核心代码
              if (obj1["value"] > obj2["value"]) return -1;
              else if (obj1["value"] < obj2["value"]) return 1;
              else if (obj1["value"] == obj2["value"]) {
                if (obj1["name"] < obj2["name"]) return -1;
                else if (obj1["name"] > obj2["name"]) return 1;
                else if (obj1["name"] == obj2["name"]) return 0;
              }
            };
            parmas.sort(func);
            var res = "   " + parmas[0].name + "<br>";
            for (var i = 0; i < parmas.length; i++) {
              res +=
                '<font color="' +
                parmas[i].color +
                '">●</font> ' +
                parmas[i].seriesName +
                ": " +
                parmas[i].value +
                "<br>";
            }
            return res;
          }
        },
        legend: {
          data: this.yNum
        },
        grid: {
          left: "2%",
          right: "2%",
          top: "15%",
          containLabel: true
        },
        xAxis: {
          type: "category",
          boundaryGap: false,
          data: this.xNum,
          axisLabel: {
            interval: 0,
            rotate: -80
          }
        },
        yAxis: {
          type: "value",
          min: 0,
          interval: 5
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
      .get("/dailyboard/")
      .then(response => {
        var Xnames = new Set();
        var Ynames = new Set();

        for (var i = 0; i < response.data.length; i++) {
          Xnames.add(response.data[i]["collecttime"]);
          Ynames.add(response.data[i]["username"]);
        }

        for (var name1 of Ynames) {
          this.yNum.push(name1);
          this.series.push({ name: name1, type: "line", data: [] });
        }

        for (var name2 of Xnames) {
          this.xNum.push(name2);
        }

        var first = {};

        for (var i = 0; i < response.data.length; i++) {
          for (var j = 0; j < this.series.length; j++) {
            if (this.series[j].name == response.data[i]["username"]) {
              if (this.series[j].data.length == 0) {
                first[this.series[j].name] = response.data[i]["account"];
                this.series[j].data.push(0);
              } else
                this.series[j].data.push(
                  response.data[i]["account"] - first[this.series[j].name]
                );
              break;
            }
          }
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