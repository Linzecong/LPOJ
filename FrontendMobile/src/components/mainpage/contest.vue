<template>
  <mu-container>
    <mu-card>
      <mu-data-table :data="tableData" :columns="columns" :hover="false">
        <template slot="expand" slot-scope="prop">
          <mu-container>
            <mu-flex justify-content="center">
              <mu-button style="margin: 8px;" color="primary">{{ prop.row.begintime }}</mu-button>

              <mu-button style="margin: 8px;" color="success">{{ prop.row.lasttime }}</mu-button>
            </mu-flex>

            <mu-flex justify-content="center">
              <mu-button
                style="margin: 8px;"
                :color="contestlevel(prop.row.level)"
              >{{ prop.row.level }}</mu-button>
            </mu-flex>

            <br />
            <mu-flex justify-content="center">
              <mu-chip :color="contestauth(prop.row.auth)">{{ prop.row.auth }}</mu-chip>

              <mu-chip style="margin-left:15px;" :color="contestauth(prop.row.auth)">{{ prop.row.type }}</mu-chip>
            </mu-flex>

            <br />
            <mu-button full-width color="success" @click="contestclick(prop.row.id)">Go To Contest!</mu-button>
            <br />
            <br />
          </mu-container>
        </template>

        <template slot-scope="scope">
          <td>{{scope.row.id}}</td>
          <td>{{scope.row.title}}</td>
        </template>
      </mu-data-table>
    </mu-card>
    <br />
    <mu-flex justify-content="center">
      <mu-pagination
        raised
        :page-count="5"
        :total="totalcontest"
        :current.sync="currentpage"
        @change="handleCurrentChange"
      ></mu-pagination>
    </mu-flex>
  </mu-container>
</template>

<script>
import moment from "moment";
export default {
  name: "contest",
  data() {
    return {
      currentpage: 1,
      pagesize: 10,
      totalcontest: 10,
      tableData: [],
      loading: true,
      searchform: {
        type: "",
        title: ""
      },
      columns: [
        { title: "ID", name: "id", width: 80 },
        { title: "Title", name: "title" }
      ]
    };
  },
  methods: {
    contestclick: function(row) {
      this.$router.push({
        name: "contestdetail",
        params: { contestID: row }
      });
    },
    contestlevel: function(type) {
      if (type == "Easy") return "info";
      if (type == "Medium") return "success";
      if (type == "Hard") return "";
      if (type == "VeryHard") return "warning";
      if (type == "ExtremelyHard") return "error";
    },
    contestauth: function(type) {
      if (type == "Public") return "success";
      if (type == "Protect") return "warning";
      if (type == "Private") return "error";
    },
    searchcontest(val) {
      this.currentpage = 1;
      this.$axios
        .get(
          "/contestinfo/?limit=" +
            this.pagesize +
            "&offset=" +
            (this.currentpage - 1) * this.pagesize +
            "&search=" +
            this.searchform.title +
            "&type=" +
            this.searchform.type
        )
        .then(response => {
          for (var i = 0; i < response.data.results.length; i++) {
            if (response.data.results[i]["level"] == "1")
              response.data.results[i]["level"] = "Easy";
            if (response.data.results[i]["level"] == "2")
              response.data.results[i]["level"] = "Medium";
            if (response.data.results[i]["level"] == "3")
              response.data.results[i]["level"] = "Hard";
            if (response.data.results[i]["level"] == "4")
              response.data.results[i]["level"] = "VeryHard";
            if (response.data.results[i]["level"] == "5")
              response.data.results[i]["level"] = "ExtremelyHard";
            response.data.results[i]["begintime"] = moment(
              response.data.results[i]["begintime"]
            ).format("YYYY-MM-DD HH:mm:ss");
            response.data.results[i]["lasttime"] =
              parseInt(response.data.results[i]["lasttime"] / 60 / 60) +
              ":" +
              parseInt((response.data.results[i]["lasttime"] / 60) % 60) +
              ":" +
              parseInt((response.data.results[i]["lasttime"] % 60) % 60);

            if (response.data.results[i]["auth"] == "1")
              response.data.results[i]["auth"] = "Public";
            if (response.data.results[i]["auth"] == "2")
              response.data.results[i]["auth"] = "Private";
            if (response.data.results[i]["auth"] == "0")
              response.data.results[i]["auth"] = "Protect";
          }
          this.tableData = response.data.results;
          this.totalcontest = response.data.count;
        })
        .catch(error => {
          this.$toast.error(
            "服务器错误！" + "(" + JSON.stringify(error.response.data) + ")"
          );
        });
    },
    
    handleCurrentChange(val) {
      this.currentpage = val;

      this.$axios
        .get(
          "/contestinfo/?limit=" +
            this.pagesize +
            "&offset=" +
            (this.currentpage - 1) * this.pagesize +
            "&search=" +
            this.searchform.title +
            "&type=" +
            this.searchform.type
        )
        .then(response => {
          for (var i = 0; i < response.data.results.length; i++) {
            if (response.data.results[i]["level"] == "1")
              response.data.results[i]["level"] = "Easy";
            if (response.data.results[i]["level"] == "2")
              response.data.results[i]["level"] = "Medium";
            if (response.data.results[i]["level"] == "3")
              response.data.results[i]["level"] = "Hard";
            if (response.data.results[i]["level"] == "4")
              response.data.results[i]["level"] = "VeryHard";
            if (response.data.results[i]["level"] == "5")
              response.data.results[i]["level"] = "ExtremelyHard";

            response.data.results[i]["begintime"] = moment(
              response.data.results[i]["begintime"]
            ).format("YYYY-MM-DD HH:mm:ss");
            response.data.results[i]["lasttime"] =
              parseInt(response.data.results[i]["lasttime"] / 60 / 60) +
              ":" +
              parseInt((response.data.results[i]["lasttime"] / 60) % 60) +
              ":" +
              parseInt((response.data.results[i]["lasttime"] % 60) % 60);

            if (response.data.results[i]["auth"] == "1")
              response.data.results[i]["auth"] = "Public";
            if (response.data.results[i]["auth"] == "2")
              response.data.results[i]["auth"] = "Private";
            if (response.data.results[i]["auth"] == "0")
              response.data.results[i]["auth"] = "Protect";
          }
          this.tableData = response.data.results;
          this.totalcontest = response.data.count;
        })
        .catch(error => {
          this.$toast.error(
            "服务器错误！" + "(" + JSON.stringify(error.response.data) + ")"
          );
        });
    }
  },
  created() {
    this.$axios
      .get("/contestinfo/?limit=10&offset=0")
      .then(response => {
        for (var i = 0; i < response.data.results.length; i++) {
          if (response.data.results[i]["level"] == "1")
            response.data.results[i]["level"] = "Easy";
          if (response.data.results[i]["level"] == "2")
            response.data.results[i]["level"] = "Medium";
          if (response.data.results[i]["level"] == "3")
            response.data.results[i]["level"] = "Hard";
          if (response.data.results[i]["level"] == "4")
            response.data.results[i]["level"] = "VeryHard";
          if (response.data.results[i]["level"] == "5")
            response.data.results[i]["level"] = "ExtremelyHard";

          response.data.results[i]["begintime"] = moment(
            response.data.results[i]["begintime"]
          ).format("YYYY-MM-DD HH:mm:ss");
          response.data.results[i]["lasttime"] =
            parseInt(response.data.results[i]["lasttime"] / 60 / 60) +
            ":" +
            parseInt((response.data.results[i]["lasttime"] / 60) % 60) +
            ":" +
            parseInt((response.data.results[i]["lasttime"] % 60) % 60);

          if (response.data.results[i]["auth"] == "1")
            response.data.results[i]["auth"] = "Public";
          if (response.data.results[i]["auth"] == "2")
            response.data.results[i]["auth"] = "Private";
          if (response.data.results[i]["auth"] == "0")
            response.data.results[i]["auth"] = "Protect";
        }
        this.tableData = response.data.results;
        this.totalcontest = response.data.count;
        this.loading = false;
      })
      .catch(error => {
        this.$toast.error(
          "服务器错误！" + "(" + JSON.stringify(error.response.data) + ")"
        );
      });
  }
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
#leveltag {
  text-align: center;
  font-weight: bold;
}
.el-row {
  margin-bottom: 20px;
}
</style>
