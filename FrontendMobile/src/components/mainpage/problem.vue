<template>
  <mu-container>
    <mu-card>
      <mu-data-table
        :hover="false"
        :data="tableData"
        :rowClassName="tableRowClassName"
        :columns="columns"
      >
        <template slot="header" slot-scope="scope">
          <tr>
            <th>ID</th>
            <th>
              <mu-row style="margin-top:16px;" gutter>
                <mu-col span="9">
                  <mu-text-field
                    style="width:150px"
                    v-model="searchtext"
                    @keyup.native.enter="searchtitle"
                    placeholder="Search..."
                    action-icon="search"
                    :action-click="searchtitle"
                  ></mu-text-field>
                </mu-col>
                <mu-col span="3" offset=".">
                  <mu-button fab small color="primary" @click="dialogVisible=true">
                    <mu-icon value="build"></mu-icon>
                  </mu-button>
                </mu-col>
              </mu-row>
            </th>
          </tr>
        </template>

        <template slot="expand" slot-scope="prop">
          <mu-container>
            <mu-flex justify-content="center">
              <mu-button style="margin: 8px;" color="primary">{{ prop.row.rate }}</mu-button>

              <mu-button style="margin: 8px;" color="success">{{ prop.row.score }}</mu-button>
            </mu-flex>
            <mu-flex justify-content="center">
              <mu-button
                style="margin: 8px;"
                :color="problemlevel(prop.row.level)"
              >{{ prop.row.level }}</mu-button>
            </mu-flex>

            <br />
            <mu-flex justify-content="center">
              <mu-chip
                id="protag"
                color="info"
                v-for="(name,index) in prop.row.tag"
                :key="index"
              >{{ name }}</mu-chip>
            </mu-flex>
            <br />
            <mu-button full-width color="success" @click="problemclick(prop.row.problem)">Do It Now!</mu-button>
            <br />
            <br />
          </mu-container>
        </template>

        <template slot-scope="scope">
          <td>{{scope.row.problem}}</td>
          <td>{{scope.row.title}}</td>
        </template>
      </mu-data-table>
    </mu-card>
    <br />
    <mu-flex justify-content="center">
      <mu-pagination
        raised
        :page-count="5"
        :total="totalproblem"
        :current.sync="currentpage"
        @change="handleCurrentChange"
      ></mu-pagination>
    </mu-flex>

    <mu-dialog title="Click to filter" scrollable :open.sync="dialogVisible">

      <mu-switch v-model="islpoj" :label="'Only LPOJ: ' + islpoj" @change="statuechange"></mu-switch>
      <br>
      <mu-button
        id="tag"
        v-for="(name,index) in tagnames"
        :key="index"
        @click="tagclick(name)"
        :color="filtercolor[name]"
      >{{ name }}</mu-button>
      <mu-button slot="actions" flat color="primary" @click="dialogVisible=false">OK</mu-button>
    </mu-dialog>
  </mu-container>
</template>

<script>
export default {
  data() {
    return {
      currentpage: 1,
      pagesize: 10,
      totalproblem: 10,
      tableData: [],
      tagnames: [],
      ac: 100,
      mle: 100,
      tle: 100,
      rte: 100,
      pe: 100,
      ce: 100,
      wa: 100,
      se: 100,
      title: "Statistics",
      currenttag: "",
      searchtext: "",
      searchoj: "LPOJ",
      dialogVisible: false,
      islpoj:true,
      columns: [
        { title: "ID", name: "problem", width: 80 },
        { title: "Title", name: "title" }
      ],

      filtercolor: {}
    };
  },
  methods: {
    statuechange(val) {
      if (val == true) {
        this.searchoj = "LPOJ";
      } else {
        this.searchoj = "";
      }
      this.searchtitle();
    },
    searchtitle() {
      this.currentpage = 1;
      this.$axios
        .get(
          "/problemdata/?limit=" +
            this.pagesize +
            "&offset=" +
            (this.currentpage - 1) * this.pagesize +
            "&auth=1&search=" +
            this.searchtext+
            "&oj="+this.searchoj
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

            response.data.results[i]["rate"] =
              response.data.results[i]["ac"] +
              "/" +
              response.data.results[i]["submission"];

            if (response.data.results[i]["tag"] == null)
              response.data.results[i]["tag"] = ["无"];
            else
              response.data.results[i]["tag"] = response.data.results[i][
                "tag"
              ].split("|");
          }
          this.tableData = response.data.results;
          this.totalproblem = response.data.count;
        });
    },
    tagclick(name) {
      if (this.currenttag.indexOf(name) >= 0) {
        this.filtercolor[name] = "";
        var li = this.currenttag.split("+");
        for (var i = 0; i < li.length; i++) {
          if (li[i] == name) {
            li.splice(i, 1);
            break;
          }
        }
        this.currenttag = li.join("+");
      } else {
        this.filtercolor[name] = "primary";
        var li = this.currenttag.split("+");
        li.push(name);
        this.currenttag = li.join("+");
      }
      this.searchtext = this.currenttag;
      this.currentpage = 1;
      this.$axios
        .get(
          "/problemdata/?limit=" +
            this.pagesize +
            "&offset=" +
            (this.currentpage - 1) * this.pagesize +
            "&auth=1&search=" +
            this.searchtext+
            "&oj="+this.searchoj
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

            response.data.results[i]["rate"] =
              response.data.results[i]["ac"] +
              "/" +
              response.data.results[i]["submission"];

            if (response.data.results[i]["tag"] == null)
              response.data.results[i]["tag"] = ["无"];
            else
              response.data.results[i]["tag"] = response.data.results[i][
                "tag"
              ].split("|");
          }
          this.tableData = response.data.results;
          this.totalproblem = response.data.count;
        });
    },

    handleCurrentChange(val) {
      this.currentpage = val;
      this.$axios
        .get(
          "/problemdata/?limit=" +
            this.pagesize +
            "&offset=" +
            (this.currentpage - 1) * this.pagesize +
            "&auth=1&search=" +
            this.searchtext+
            "&oj="+this.searchoj
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

            response.data.results[i]["rate"] =
              response.data.results[i]["ac"] +
              "/" +
              response.data.results[i]["submission"];

            if (response.data.results[i]["tag"] == null)
              response.data.results[i]["tag"] = ["无"];
            else
              response.data.results[i]["tag"] = response.data.results[i][
                "tag"
              ].split("|");
          }
          this.tableData = response.data.results;
          this.totalproblem = response.data.count;
        });
    },
    tableRowClassName(rowIndex, row) {
      var acpro = this.$store.state.acpro;
      if (acpro)
        if (acpro.indexOf(row.problem + "") != -1) {
          return "acrow";
        }
      return "";
    },
    problemlevel: function(type) {
      if (type == "Easy") return "info";
      if (type == "Medium") return "success";
      if (type == "Hard") return "secondary";
      if (type == "VeryHard") return "warning";
      if (type == "ExtremelyHard") return "error";
    },

    problemclick: function(problem) {
      this.$router.push({
        name: "problemdetail",
        query: { problemID: problem }
      });
    }
  },
  mounted() {
    this.$axios
      .get("/problemdata/?limit=10&offset=0&auth=1&oj=LPOJ")
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

          response.data.results[i]["rate"] =
            response.data.results[i]["ac"] +
            "/" +
            response.data.results[i]["submission"];

          if (response.data.results[i]["tag"] == null)
            response.data.results[i]["tag"] = ["无"];
          else
            response.data.results[i]["tag"] = response.data.results[i][
              "tag"
            ].split("|");
        }
        this.tableData = response.data.results;
        this.totalproblem = response.data.count;
      });

    this.$axios.get("/problemtag/").then(response => {
      for (var i = 0; i < response.data.length; i++)
        this.tagnames.push(response.data[i]["tagname"]);
    });
  }
};
</script>


<style scope>
#leveltag {
  text-align: center;
  font-weight: bold;
}
#protag {
  text-align: center;
  font-weight: bold;
  margin-right: 5px;
  margin-bottom: 3px;
}
#tag {
  font-size: 12px;
  text-align: center;
  margin: 4px;
}
.el-row {
  margin-bottom: 20px;
}
.acrow {
  background: #c7ffb8;
}
</style>