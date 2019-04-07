<template>
  <el-row :gutter="15">
    <el-col :span="18">
      <el-card shadow="always">
        <center>
        <el-pagination
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
          :current-page="currentpage"
          :page-sizes="[10, 20, 30, 50]"
          :page-size="pagesize"
          layout="total, sizes, prev, pager, next, jumper"
          :total="totalproblem"
        ></el-pagination>
        </center>
        <el-table
          :data="tableData"
          :row-class-name="tableRowClassName"
          @cell-mouse-enter="changestatistices"
          @cell-click="problemclick"
          size="small"
        >
          <el-table-column prop="problem" label="ID" :width="70"></el-table-column>
          <el-table-column prop="title" label="Title" :width="200"></el-table-column>
          <el-table-column prop="level" label="Level" :width="170">
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
          <el-table-column prop="tag" label="Tag" :width="350">
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
        <center>
        <el-pagination
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
          :current-page="currentpage"
          :page-sizes="[10, 20, 30, 50]"
          :page-size="pagesize"
          layout="total, sizes, prev, pager, next, jumper"
          :total="totalproblem"
        ></el-pagination>
        </center>
      </el-card>
    </el-col>
    <el-col :span="6">
      <el-row :gutter="15">
        <el-col>
          <el-card shadow="always">
            <h3>{{title}}</h3>

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
      <el-row :gutter="15" >
        <el-col>
          <el-card shadow="always">
            <h4>Tags (点击以筛选)</h4>
            <el-button
              id="tag"
              v-for="(name,index) in tagnames"
              :key="index"
              size="mini"
              @click="tagclick(name)"
              :ref="name"
            >{{ name }}</el-button>
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
#protag{
  text-align: center;
  font-weight: bold;
  margin-right: 7px;
  margin-bottom: 7px;
}
#tag {
  text-align: center;
  font-weight: bold;
  margin-left: 2px;
  margin-bottom: 5px;
}
.el-row {
  margin-bottom: 20px;
}
</style>

<script>
import problemdetail from "@/components/problemdetail";
export default {
  methods: {
    tagclick(name){
      

      if(this.currenttag.indexOf(name)>=0){
        this.$refs[name][0].type='default'
        var li=this.currenttag.split("+");
        for(var i=0;i<li.length;i++){
          if(li[i]==name){
            li.splice(i,1);
            break;
          }
        }
        this.currenttag=li.join("+");
      }
      else{
        this.$refs[name][0].type='primary'
        var li=this.currenttag.split("+");
        li.push(name)
        this.currenttag=li.join("+");
      }
      

      this.$axios
        .get(
          "/problemdata/?limit=" +
            this.pagesize +
            "&offset=" +
            (this.currentpage - 1) * this.pagesize+"&auth=1&search="+this.currenttag
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
    handleSizeChange(val) {
      this.pagesize = val;

      this.$axios
        .get(
          "/problemdata/?limit=" +
            this.pagesize +
            "&offset=" +
            (this.currentpage - 1) * this.pagesize+"&auth=1"
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
            (this.currentpage - 1) * this.pagesize+"&auth=1"
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
        query: { problemID: row.problem }
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
      title: "Statistics",
      currenttag:"",

      isdesktop:true
    };
  },
  mounted() {
		//可用于设置自适应屏幕，根据获得的可视宽度（兼容性）判断是否显示
		let w = document.documentElement.offsetWidth || document.body.offsetWidth;
		if(w < 1000){
      this.isdesktop = false;
    }
	},
  created() {
    this.$axios
      .get(
        "/problemdata/?limit=10&offset=0"+"&auth=1"
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
      .get("/problemtag/")
      .then(response => {
        for (var i = 0; i < response.data.length; i++)
          this.tagnames.push(response.data[i]["tagname"]);
      });
  }
};
</script>