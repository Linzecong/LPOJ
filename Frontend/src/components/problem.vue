<template>
  <el-row :gutter="15">
    <el-col :span="19">
      <el-card shadow="always">
        <el-table
          :data="tableData"
          :row-class-name="tableRowClassName"
          @cell-mouse-enter="changestatistices"
          @cell-click="problemclick"
        >
          <el-table-column prop="id" label="ID" :width="100"></el-table-column>
          <el-table-column prop="title" label="Title"></el-table-column>
          <el-table-column prop="level" label="Level">
            <template slot-scope="scope1">
              <el-tag
                id="leveltag"
                size="medium"
                :type="problemlevel(scope1.row.level)"
                disable-transitions
                hit
              >{{ scope1.row.level }}</el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="rate" label="AC/Submittion"></el-table-column>
          <el-table-column prop="tag" label="Tag">
            <template slot-scope="scope">
              <el-tag
                id="protag"
                v-for="(name,index) in scope.row.tag"
                :key="index"
                size="medium"
                disable-transitions
                hit
              >{{ name }}</el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="score" label="Score"></el-table-column>
        </el-table>
        <el-pagination
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
          :current-page="currentpage"
          :page-sizes="[10, 20, 30, 50]"
          :page-size="pagesize"
          layout="total, sizes, prev, pager, next, jumper"
          :total="totalproblem"
        ></el-pagination>
      </el-card>
    </el-col>
    <el-col :span="5">
      <el-row :gutter="15">
        <el-col>
          <el-card shadow="always">
            <h2>Tags</h2>
            <el-tag
              id="tag"
              v-for="(name,index) in tagnames"
              :key="index"
              size="medium"
              type="info"
              disable-transitions
              hit
            >{{ name }}</el-tag>
          </el-card>
        </el-col>
      </el-row>
      <el-row :gutter="15">
        <el-col>
          <el-card shadow="always">
            <h2>{{title}}</h2>

            <el-row :gutter="10">
              <el-col :span="3">
                <b>AC:</b>
              </el-col>
              <el-col :span="21">
                <el-progress
                  :text-inside="true"
                  :stroke-width="18"
                  :percentage="ac"
                  status="success"
                ></el-progress>
              </el-col>
            </el-row>

            <el-row :gutter="10">
              <el-col :span="3">
                <b>WA:</b>
              </el-col>
              <el-col :span="21">
                <el-progress
                  :text-inside="true"
                  :stroke-width="18"
                  :percentage="wa"
                  status="exception"
                ></el-progress>
              </el-col>
            </el-row>
            <el-row :gutter="10">
              <el-col :span="3">
                <b>PE:</b>
              </el-col>
              <el-col :span="21">
                <el-progress
                  :text-inside="true"
                  :stroke-width="18"
                  :percentage="pe"
                  color="#FF9800"
                ></el-progress>
              </el-col>
            </el-row>
            <el-row :gutter="10">
              <el-col :span="3">
                <b>TLE:</b>
              </el-col>
              <el-col :span="21">
                <el-progress
                  :text-inside="true"
                  :stroke-width="18"
                  :percentage="tle"
                  color="#FF9800"
                ></el-progress>
              </el-col>
            </el-row>
            <el-row :gutter="10">
              <el-col :span="3">
                <b>RTE:</b>
              </el-col>
              <el-col :span="21">
                <el-progress
                  :text-inside="true"
                  :stroke-width="18"
                  :percentage="rte"
                  color="#FF9800"
                ></el-progress>
              </el-col>
            </el-row>
            <el-row :gutter="10">
              <el-col :span="3">
                <b>MLE:</b>
              </el-col>
              <el-col :span="21">
                <el-progress
                  :text-inside="true"
                  :stroke-width="18"
                  :percentage="mle"
                  color="#795548"
                ></el-progress>
              </el-col>
            </el-row>

            <el-row :gutter="10">
              <el-col :span="3">
                <b>CE:</b>
              </el-col>
              <el-col :span="21">
                <el-progress
                  :text-inside="true"
                  :stroke-width="18"
                  :percentage="ce"
                  color="#FFC107"
                ></el-progress>
              </el-col>
            </el-row>

            <el-row :gutter="10">
              <el-col :span="3">
                <b>SE:</b>
              </el-col>
              <el-col :span="21">
                <el-progress
                  :text-inside="true"
                  :stroke-width="18"
                  :percentage="se"
                  status="exception"
                ></el-progress>
              </el-col>
            </el-row>
          </el-card>
        </el-col>
      </el-row>
    </el-col>
  </el-row>
</template>

<style scope>
#leveltag {
  text-align: center;
  font-weight: bold;
}
#protag {
  text-align: center;
  font-weight: bold;
  margin-right: 13px;
}
#tag {
  text-align: center;
  font-weight: bold;
  margin-right: 13px;
  margin-bottom: 13px;
}
.el-row {
  margin-bottom: 20px;
}
</style>

<script>
import problemdetail from "@/components/problemdetail";
export default {
  methods: {
    handleSizeChange(val) {
      this.pagesize = val;

      this.$axios
        .get(
          "http://" +
            this.$ip +
            ":" +
            this.$port +
            "/problemdata/?limit=" +
            this.pagesize +
            "&offset=" +
            (this.currentpage - 1) * this.pagesize
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
          "http://" +
            this.$ip +
            ":" +
            this.$port +
            "/problemdata/?limit=" +
            this.pagesize +
            "&offset=" +
            (this.currentpage - 1) * this.pagesize
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
    tableRowClassName({ row, rowIndex }) {
      return "";
    },
    problemlevel: function(type) {
      if (type == "Easy") return "info";
      if (type == "Medium") return "success";
      if (type == "Hard") return "";
      if (type == "VeryHard") return "warning";
      if (type == "ExtremelyHard") return "danger";
    },
    changestatistices: function(row, column, cell, event) {
      if (row.submission == 0) {
        this.ac = 0;
        this.mle = 0;
        this.tle = 0;
        this.rte = 0;
        this.pe = 0;
        this.ce = 0;
        this.wa = 0;
        this.se = 0;
      } else {
        this.ac = parseFloat(((row.ac * 100) / row.submission).toFixed(2));
        this.mle = parseFloat(((row.mle * 100) / row.submission).toFixed(2));
        this.tle = parseFloat(((row.tle * 100) / row.submission).toFixed(2));
        this.rte = parseFloat(((row.rte * 100) / row.submission).toFixed(2));
        this.pe = parseFloat(((row.pe * 100) / row.submission).toFixed(2));
        this.ce = parseFloat(((row.ce * 100) / row.submission).toFixed(2));
        this.wa = parseFloat(((row.wa * 100) / row.submission).toFixed(2));
        this.se = parseFloat(((row.se * 100) / row.submission).toFixed(2));
      }
      this.title = row.title;
    },
    problemclick: function(row, column, cell, event) {
      this.$router.push({
        name: "problemdetail",
        params: { problemID: row.id }
      });
    }
  },
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
      title: "Statistics"
    };
  },
  created() {
    this.$axios
      .get(
        "http://" +
          this.$ip +
          ":" +
          this.$port +
          "/problemdata/?limit=10&offset=0"
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

    this.$axios
      .get("http://" + this.$ip + ":" + this.$port + "/problemtag/")
      .then(response => {
        for (var i = 0; i < response.data.length; i++)
          this.tagnames.push(response.data[i]["tagname"]);
      });
  }
};
</script>