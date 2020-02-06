<template>
  <el-card>
    <el-table :data="tableData"
              @cell-click="contestclick"
              size="small">
      <el-table-column prop="id"
                       label="ID"
                       :width="100"></el-table-column>
      <el-table-column prop="title"
                       label="作业"
                       :width="300"></el-table-column>
      <el-table-column prop="begintime"
                       label="布置时间"></el-table-column>
      <el-table-column prop="type"
                       label="类型"></el-table-column>
      <el-table-column prop="classes"
                       label="班级"></el-table-column>
    </el-table>
  </el-card>

</template>

<script>
export default {
  data () {
    return {
      username: "",
      className: "",
      currentpage: 1,
      pagesize: 30,
      totalcontest: 10,
      tableData: [],
      tableData2: [],
      loading: true,
      searchform: {
        type: "",
        title: ""
      }
    };
  },

  methods: {
    contestclick: function (row, column, cell, event) {
      this.$router.push({
        name: "contestdetail",
        params: { contestID: row.id }
      });
    },
    // getfinish: function (cid) {
    //   console.log(cid);
    //   var hwcount = "0";
    //   var account = "0";
    //   var fini = "0";
    //   this.$axios.get("/contestproblem/?contestid=" + cid)
    //     .then(
    //       response => {
    //         hwcount = response.data.length;
    //         this.$axios.get("/contestboard/?contestid=" + cid + "&username=" + this.username)
    //           .then(
    //             response2 => {
    //               account = response2.data.length;
    //               console.log(account);
    //               fini = String(account) + "/" + String(hwcount);
    //               console.log(String(account) + "/" + String(hwcount));
    //               console.log(fini);
    //               row.finish = fini;
    //               // return fini;
    //             }
    //           )
    //       }
    //     )
    //   console.log(fini);
    // },
  },
  created () {
    this.username = sessionStorage.username;
    console.log(this.username);
    this.className = this.$route.query.className;
    console.log(this.className);

    this.$axios
      .get("/contestinfo/?type=Homework&classes=" + this.className)
      .then(response => {
        console.log(response.data);

        this.tableData = response.data;
        this.totalcontest = response.data.length;
        this.loading = false;
        console.log(this.tableData);
      })
      .catch(error => {
        this.$message.error(
          "服务器错误！" + "(" + JSON.stringify(error.response.data) + ")"
        );
      });
  }

}
</script>


<style scoped>
</style>
