<template>
  <el-row>
    <center>
      <h1>{{ contesttitle }}</h1>
    </center>
    <el-row :gutter="10">
      <el-table :data="tableData" :cell-style="cellstyle" border>
        <el-table-column prop="user" label="User"></el-table-column>
        <el-table-column prop="nickname" label="Nickname"></el-table-column>
        <el-table-column prop="solved" label="Solve"></el-table-column>
        <el-table-column prop="time" label="Time"></el-table-column>
        <el-table-column
          v-for="(item,index) in probleminfo"
          :key="index"
          :prop="item.prop"
          :label="item.label"
        ></el-table-column>
      </el-table>
    </el-row>
  </el-row>
</template>

<script>
export default {
  name: "contestrank",
  data() {
    return {
      problemcount: this.$store.state.contestproblemcount,
      contesttitle: this.$store.state.contesttitle,
      contestid: this.$route.params.contestID,
      probleminfo: [],
      tableData:[
        {
          user:404,
          nickname:404,
          solved:100,
          time:500,
          A:"(-1)",
          B:"(-2)",
          C:"(-3)",
          D:"(-4)",
        },
        {
          user:404,
          nickname:404,
          solved:90,
          time:500,
          A:"(-1)",
          B:"(-2)",
          C:"(-3)",
          D:"(-4)",
        }
      ]
    };
  },
  created() {
    //this.setproblemcount(this.$route.params.contestID);
  },
  methods: {
    sortByProperty (p1,p2){
     function sortfun (obj1,obj2){
　　//核心代码
          if (obj1[p1] > obj2[p1]) return -1
          else if (obj1[p1] < obj2[p1]) return 1
          else if (obj1[p1] == obj2[p1]) {
            if (obj1[p2] < obj2[p2]) return -1
            else if (obj1[p2] > obj2[p2]) return 1
            else if (obj1[p2] == obj2[p2]) return 0
          }
     }
     return sortfun
    },
    toChar(val) {
      var A = "A";
      return String.fromCharCode(val + A.charCodeAt());
    },
    cellstyle(data){
      var id = data.columnIndex-4;
      var str = this.toChar(id);
      if(id<0)
        return "background-color:white;text-align:center";
      if(data.row[str].indexOf("❤")>-1)
        return "background-color:green;text-align:center";
      if(data.row[str].indexOf("(")>-1)
        return "background-color:#F56C6C;text-align:center";
      if(data.row[str].indexOf(":")>-1)
        return "background-color:#67C23A;text-align:center";
      return "background-color:white";
    },
    setproblemcount(id) {
      this.contesttitle = this.$store.state.contesttitle;

      this.$axios
        .get(
          "http://" +
            this.$ip +
            ":" +
            this.$port +
            "/contestproblem/?contestid=" +
            id
        )
        .then(response3 => {
          this.$store.state.contestproblemcount = response3.data.length;
          this.problemcount = this.$store.state.contestproblemcount;
          this.probleminfo=[];
          for(var i = 0;i<response3.data.length;i++){
            this.probleminfo.push({prop:this.toChar(i),label:this.toChar(i)})
          }
          this.$axios
          .get(
            "http://" +
              this.$ip +
              ":" +
              this.$port +
              "/contestrank/?contestid=" +
              id
          )
          .then(response => {
            var data=[]
            // 读取所有有提交的用户
            console.log(this.$store.state.contestbegintime)

            for(var i = 0;i<response.data.length;i++){
              var k = {user:response.data[i]["username"],nickname:response.data[i]["user"],solved:0,time:0,sorttime:0};
              for(var j =0;j<this.probleminfo.length;j++){
                k[this.probleminfo[j].prop]="";
              }

              var li = response.data[i]["statue"].split("|");
              var count =0 ;
              var t=0;
              for(var ii =0;ii<li.length;ii++){
                li[ii]=parseInt(li[ii]);
                if(li[ii]>0){
                  count++;
                  var cha = parseInt((li[ii]-this.$store.state.contestbegintime)/1000);
                  t+=cha;
                  var tt =
                  parseInt(cha / 60 / 60) +
                  ":" +
                  parseInt((cha / 60) % 60) +
                  ":" +
                  parseInt((cha % 60) % 60);

                  k[this.toChar(ii)]= tt;
                }
                else{
                  if(li[ii]<0)
                    k[this.toChar(ii)]= "("+li[ii]+")";
                }
              }
              k["solved"]=count;
              var ttt =
                  parseInt(t / 60 / 60) +
                  ":" +
                  parseInt((t / 60) % 60) +
                  ":" +
                  parseInt((t % 60) % 60);
              k["time"]=ttt;
              k["sorttime"]=t;
              
              

              data.push(k)
            }
            data.sort(this.sortByProperty("solved","sorttime"));

            for(var id=0;id<this.problemcount;id++){
              var pro = this.toChar(id);
              var index=-1;
              var minn=100000000000000;
              for(var i=0;i<data.length;i++){
                  var li = data[i][pro].split(":");
                  var time = li[0]*3600+li[1]*60+li[2];
                  if(time<minn)
                  {
                    minn=time
                    index=i;
                  }
              }
              if(index!=-1){
                data[index][pro]="❤"+data[index][pro]
              }
            }


            this.tableData=data;
            
          });


        });
    }
  }
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
h1 {
  position: relative;
}
</style>
