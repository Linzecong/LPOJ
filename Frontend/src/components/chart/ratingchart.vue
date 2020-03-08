<template>
  <center>
    <div ref="myEchart" style="height:500px;width:100%"></div>
  </center>
</template>

<script>
import moment from "moment";
import echarts from "./echarts";
export default {
  name: "ratingchart",
  data() {
    return {
      xNum: [],
      yNum: [],
      Xcontest:[],
      Xchange:[],
      Xid:[],
      series: [] // 折线图数据
    };
  },
  methods: {
    
    initChart() {
      let myChart = echarts.init(this.$refs.myEchart);
      let a= this.Xcontest
      let b= this.Xchange
      let c= this.Xid
      let router = this.$router
      myChart.on('click', function (params) {
        router.push({
          name: "contestdetail",
          params: { contestID: c[params.dataIndex] }
        });
      });
      myChart.setOption({
        tooltip: {
          trigger: "axis",
          confine: true,
          textStyle: {
            fontSize: 9
          },
          formatter: function(parmas) {
            //console.log(parmas)
            var res = parmas[0].name + "<br>"+a[parmas[0].dataIndex]+"<br>"+(b[parmas[0].dataIndex]>=0?"+":"")+b[parmas[0].dataIndex]+"<br><br>"+  parmas[0].value;
            return res;
          }
        },
        visualMap: {
            top: 10,
            right: 10,
            pieces: [{
                gt: 0,
                lte: 1200,
                color: '#303133'
            }, {
                gt: 1200,
                lte: 1350,
                color: '#909399'
            }, {
                gt: 1350,
                lte: 1500,
                color: '#67C23A'
            }, {
                gt: 1500,
                lte: 1700,
                color: '#227700'
            }, {
                gt: 1700,
                lte: 1900,
                color: '#007799'
            }, {
                gt: 1900,
                lte: 2050,
                color: '#0000AA'
            }, {
                gt: 2050,
                lte: 2200,
                color: '#930093'
            }, {
                gt: 2200,
                lte: 2600,
                color: '#E6A23C'
            }, {
                gt: 2600,
                lte: 3000,
                color: '#BB5E00'
            }, {
                gt: 3000,
                color: 'red'
            }],
            outOfRange: {
                color: '#303133'
            }
        },
        grid: {
          left: "11%",
          right: "11%",
          top: "5%",
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
          min:900,
          type: "value",
        },
        series: this.series
      });
    }
  },
  mounted() {
    var username = this.$route.query.username
    this.$axios
      .get("/contestratingchange/?user="+username)
      .then(response => {
        var Xnames = []
        var Ynames = new Set();

        for (var i = 0; i < response.data.length; i++) {
          Xnames.push(response.data[i]["contesttime"]);
          Ynames.add(response.data[i]["user"]);
        }

        for (var name1 of Ynames) {
          this.yNum.push(name1);
          this.series.push({ name: name1, type: "line", data: [],areaStyle: {}});
        }

        for (var i=0;i<Xnames.length;i++) {
          var name2=Xnames[i]
          var tname2 = moment(parseInt(name2)).format("YYYY-MM-DD");
          this.xNum.push(tname2);
        }

        for (var i = 0; i < response.data.length; i++) {
          for (var j = 0; j < this.series.length; j++) {
      
            if (this.series[j].name == response.data[i]["user"]) {
              this.series[j].data.push(response.data[i].currentrating)
              this.Xcontest.push(response.data[i].contestname)
              this.Xchange.push(response.data[i].ratingchange)
              this.Xid.push(response.data[i].contestid)
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