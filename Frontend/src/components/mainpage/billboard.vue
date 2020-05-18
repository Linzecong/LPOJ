<template>
  <el-card v-loading="loading">
    <center>
      <h3>
        ACM Training Team Ranking of {{school}}
      </h3>
    </center>

    <el-table :data="tableData" border stripe size="small">
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
      school:"",
      dialogVisible: false,
      ojcount: 3,
      boardinfo: [],
      tableData: [{}],
      form: {
        username: "",
        count: 0,
        msg: ""
      },
      loading:true
    };
  },
  created() {
    this.setdata();
    var sb = this.$store.state.sb
    if(sb==undefined){
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

    setdata() {
      this.$axios.get("/board/").then(response => {
        this.ojcount = response.data[0]["OJCount"];

        this.boardinfo = [];
        var oj = response.data[0]["OJ"];
        var props = oj.split("|");
        for (var i = 0; i < props.length; i++) {
          this.boardinfo.push({ prop: props[i], label: props[i] });
        }
        this.boardinfo.push({ prop: 'cfrate', label: 'CFRate' });

        var data = [];

        for (var i = 0; i < response.data.length; i++) {
          var k = {
            username: response.data[i]["username"],
            number: response.data[i]["number"],
            classes: response.data[i]["classes"],
            ac: 0,
            total: "0/0",
            cfrate:0
          };

          for (var j = 0; j < this.boardinfo.length; j++) {
            k[this.boardinfo[j].prop] = "";
          }

          var acnum = 0;
          var subnum = 0;
          var acli = response.data[i]["acnum"].split("|");
          var subli = response.data[i]["submitnum"].split("|");
          for (var jj = 0; jj < this.boardinfo.length-1; jj++) {
            k[this.boardinfo[jj].prop] = acli[jj] + "/" + subli[jj];
            acnum = acnum + parseInt(acli[jj]);
            subnum = subnum + parseInt(subli[jj]);
          }
          k["ac"] = acnum;
          k["sub"] = subnum;
          k["total"] = acnum + "/" + subnum;
          k["cfrate"] = response.data[i]["cfrate"].split("|")[0];

          data.push(k);
        }
        data.sort(this.sortByProperty("ac", "sub"));

        this.tableData = data;
      });
    }
  },
  mounted(){
    this.loading=false
  }
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>
