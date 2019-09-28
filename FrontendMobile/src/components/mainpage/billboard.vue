<template>
  <mu-card>
    <mu-card-title :title="'ACM Training Team Ranking of '+school"></mu-card-title>

    <mu-card-text>
      <mu-data-table :columns="columns" :data="tableData">
        <template slot-scope="scope">
          <td>{{scope.row.username}}</td>
          <td>{{scope.row.total}}</td>
        </template>
      </mu-data-table>
    </mu-card-text>
  </mu-card>
</template>

<script>
export default {
  name: "billboard",
  data() {
    return {
      school: "",
      dialogVisible: false,
      ojcount: 3,
      boardinfo: [],
      tableData: [{}],
      form: {
        username: "",
        count: 0,
        msg: ""
      },
      loading: true,
      columns: [
        { title: "UserName", name: "username" },
        { title: "Total", name: "total" }
      ]
    };
  },
  created() {
    this.setdata();
    this.$axios
      .get("/settingboard/")
      .then(res => {
        if (res.data.length > 0) this.school = res.data[0].schoolname;
        else this.school = "University";
      })
      .catch(error => {
        this.$toast.error(
          "服务器错误！" + "(" + JSON.stringify(error.response.data) + ")"
        );
      });
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
        var data = [];
        for (var i = 0; i < response.data.length; i++) {
          var k = {
            username: response.data[i]["username"],
            number: response.data[i]["number"],
            classes: response.data[i]["classes"],
            ac: 0,
            total: "0/0"
          };

          for (var j = 0; j < this.boardinfo.length; j++) {
            k[this.boardinfo[j].prop] = "";
          }

          var acnum = 0;
          var subnum = 0;
          var acli = response.data[i]["acnum"].split("|");
          var subli = response.data[i]["submitnum"].split("|");
          for (var jj = 0; jj < this.boardinfo.length; jj++) {
            k[this.boardinfo[jj].prop] = acli[jj] + "/" + subli[jj];
            acnum = acnum + parseInt(acli[jj]);
            subnum = subnum + parseInt(subli[jj]);
          }
          k["ac"] = acnum;
          k["sub"] = subnum;
          k["total"] = acnum + "/" + subnum;

          data.push(k);
        }
        data.sort(this.sortByProperty("ac", "sub"));

        this.tableData = data;
      });
    }
  },
  mounted() {
    this.loading = false;
  }
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>
