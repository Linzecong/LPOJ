<template>
  <el-row>
    <center>
      <h1>{{ contesttitle }}</h1>
    </center>
    <el-row :gutter="10">
      <el-table :data="tableData" :cell-style="cellstyle" border stripe>
        <el-table-column prop="rank" label="Rank" width="70px" fixed></el-table-column>
        <el-table-column prop="user" label="User" fixed></el-table-column>
        <el-table-column prop="nickname" label="Nickname" fixed></el-table-column>
        <el-table-column prop="solved" label="Solve" fixed></el-table-column>
        <el-table-column prop="time" label="Time"></el-table-column>
        <el-table-column
          v-for="(item,index) in probleminfo"
          :key="index"
          :prop="item.prop"
          :label="item.label"
          style="white-space: pre-line;"
        >
        <template slot-scope="scope">
          <div style="white-space:pre-line;">{{scope.row[item.prop]}}</div>
        </template>
        </el-table-column>
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
          //rank:1,
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
          //rank:2,
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
      var id = data.columnIndex-5;
      var str = this.toChar(id);
      if(id<0)
        return "background-color:white;text-align:center;";
      if(data.row[str].indexOf("❤")>-1)
        return "background-color:#009100;text-align:center;font-weight:bold";
      if(data.row[str].indexOf(":")>-1)
        return "background-color:#00EC00;text-align:center";
      if(data.row[str].indexOf("(")>-1)
        return "background-color:#F56C6C;text-align:center";
      
      return "background-color:white";
    },
    setproblemcount(id) {
      this.contesttitle = this.$store.state.contesttitle;

      this.$axios
        .get(
          "/api/contestproblem/?contestid=" +
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
            "/api/contestrank/?contestid=" +
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
                if(li[ii].indexOf("$")>=0){
                  count++;
                  var tmp = li[ii].split("$")
                  tmp[0]=parseInt(tmp[0])
                  tmp[1]=parseInt(tmp[1])
                  var cha = parseInt((tmp[0]-this.$store.state.contestbegintime)/1000);
                  t+=cha;
                  t+=(-tmp[1])*20*60;
                  var tt =
                  parseInt(cha / 60 / 60) +
                  ":" +
                  parseInt((cha / 60) % 60) +
                  ":" +
                  parseInt((cha % 60) % 60);

                  if(tmp[1]<0)
                    k[this.toChar(ii)]="("+tmp[1]+")\n"+ tt;
                  else
                    k[this.toChar(ii)]=tt;
                }
                
                else{
                  li[ii]=parseInt(li[ii]);
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
            for(var i=0;i<data.length;i++){
              data[i]["rank"]=i+1;
            }

            for(var id=0;id<this.problemcount;id++){
              var pro = this.toChar(id);
              var index=-1;
              var minn=100000000000000;
              for(var i=0;i<data.length;i++){
                  if(data[i][pro].indexOf(":")>0){
                    if(data[i][pro].indexOf("(")<0){
                      var li = data[i][pro].split(":");
                      var time = parseInt(li[0])*3600+parseInt(li[1])*60+parseInt(li[2]);
                      if(time<minn)
                      {
                        minn=time
                        index=i;
                      }
                    }
                    else{
                      var tmp = data[i][pro].split(")")
                      
                      var li = tmp[1].split(":");
                      var time = parseInt(li[0])*3600+parseInt(li[1])*60+parseInt(li[2]);
                      tmp = tmp[0].split("(");
                      if(time<minn)
                      {
                        minn=time
                        index=i;
                      }
                    }

                  }
              }
              if(index!=-1){
                data[index][pro]=data[index][pro]+"\n❤";
                console.log(data[index][pro])
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
