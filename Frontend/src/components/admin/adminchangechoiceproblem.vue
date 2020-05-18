<template>
  <el-row>
    <el-input placeholder="输入题目信息以搜索..."
              v-model="searchchoicepro"
              @keyup.native.enter="searchpro"
              style="float:right;width:300px;">
      <el-button slot="append"
                 icon="el-icon-search"
                 @click="searchpro"></el-button>
    </el-input>

    <el-table :data="tabledata">
      <el-table-column property="ChoiceProblemId"
                       label="ID"
                       width="70"></el-table-column>

      <el-table-column property="des"
                       label="题面"
                       width="400"></el-table-column>

      <el-table-column property="choiceA"
                       label="选项A"
                       width="300"></el-table-column>

      <el-table-column property="choiceB"
                       label="选项B"
                       width="300"></el-table-column>

      <el-table-column property="choiceC"
                       label="选项C"
                       width="300"></el-table-column>

      <el-table-column property="choiceD"
                       label="选项D"
                       width="300"></el-table-column>

      <el-table-column
                       label="操作"
                      >
        <template slot-scope="scope">
          <el-button @click="EditChoiceProblem(scope.row)"
                     type="primary"
                     size="small">编辑</el-button>
          <el-button @click="DeleteChoiceProblem(scope.row)"
                     type="danger"
                     size="small">删除</el-button>
        </template>
      </el-table-column>

    </el-table>

    <el-dialog title="修改题目"
               :visible.sync="dialogTableVisible"
               width="85%">
      <el-form :model="choiceproblemform"
               label-position="right">

        <el-form-item label="选择题题目编号：">
          <el-input v-model="choiceproblemform.ChoiceProblemId"
                    style="width:400px;"
                    readonly></el-input>
        </el-form-item>

        <el-form-item label="选择题题目：">
          <el-input type="textarea"
                    v-model="choiceproblemform.des"
                    autosize
                    style="width:800px;"></el-input>
        </el-form-item>

        <el-form-item label="选项A：">
          <el-input type="textarea"
                    v-model="choiceproblemform.choiceA"
                    autosize
                    style="width:800px;"></el-input>
        </el-form-item>

        <el-form-item label="选项B：">
          <el-input type="textarea"
                    v-model="choiceproblemform.choiceB"
                    autosize
                    style="width:800px;"></el-input>
        </el-form-item>

        <el-form-item label="选项C：">
          <el-input type="textarea"
                    v-model="choiceproblemform.choiceC"
                    autosize
                    style="width:800px;"></el-input>
        </el-form-item>

        <el-form-item label="选项D：">
          <el-input type="textarea"
                    v-model="choiceproblemform.choiceD"
                    autosize
                    style="width:800px;"></el-input>
        </el-form-item>
        <el-form-item>
          <el-button type="success"
                     @click="AddChoiceProblemSubmit"
                     style="float:left;">修改题目</el-button>
        </el-form-item>
      </el-form>

    </el-dialog>
  </el-row>

</template>
<script>
export default {
  name: "adminchangechoiceproblem",
  data () {
    return {
      changechoiceproblemid: "",
      searchchoicepro: "",
      dialogTableVisible: false,
      tabledata: [],
      choiceproblemform: {
        ChoiceProblemId: "",
        des: "",
        choiceA: "",
        choiceB: "",
        choiceC: "",
        choiceD: "",
      }
    }
  },

  methods: {
    searchpro () {
      this.$axios
        .get(
          "/choiceproblem/?search=" +
          this.searchchoicepro
        )
        .then(response => {
          this.tabledata = response.data;
        });
    },
    AddChoiceProblemSubmit () {
      console.log(this.choiceproblemform);
      this.$confirm(
        "确定修改吗？本次修改将会用新数据覆盖旧数据",
        {
          confirmButtonText: "确定",
          cancelButtonText: "取消",
          type: "warning"
        }
      ).then(() => {
        this.$axios.get("/choiceproblem/?ChoiceProblemId=" + this.choiceproblemform.ChoiceProblemId + "&des=" + this.choiceproblemform.des)
          .then(
            response => {
              var updateProblemId = response.data[0].id;
              this.$axios.put("/choiceproblem/" + updateProblemId + "/", this.choiceproblemform);
              this.$message.success("已更新");
            }
          )
      });
    },
    DeleteChoiceProblem (row) {
      this.$confirm(
        "确定要删除题目：【" + row.des + "】吗？",
        {
          confirmButtonText: "确定",
          cancelButtonText: "取消",
          type: "warning"
        }
      ).then(() => {
        this.$axios.get("/choiceproblem/?ChoiceProblemId=" + row.ChoiceProblemId + "&des=" + row.des)
          .then(
            response => {
              var deleteProblemId = response.data[0].id;
              this.$axios.delete("/choiceproblem/" + deleteProblemId + "/");
              this.$message.error("已删除");
            }
          )
      });

    },
    ChoiceProblemChange (ProId) {
      console.log(ProId);
      this.$axios
        .get("/choiceproblem/?ChoiceProblemId=" + ProId)
        .then(response => {
          this.choiceproblemform = response.data[0];
          console.log(this.choiceproblemform);
        })
      // .catch(error => {
      //   this.$message.error(
      //     "服务器错误！" + JSON.stringify(error.response.data)
      //   );
      //   this.choiceproblemform = {};
      // });

    },
    EditChoiceProblem (row) {
      this.changechoiceproblemid = row.ChoiceProblemId;
      this.choiceproblemform.ChoiceProblemId = row.ChoiceProblemId;
      this.ChoiceProblemChange(row.ChoiceProblemId);
      this.dialogTableVisible = true;
    },

  },
  created () {
    this.$axios
      .get("/choiceproblem/")
      .then(response => {
        this.tabledata = response.data;
      })
      .catch(error => {
        this.$message.error(
          "服务器错误！" + JSON.stringify(error.response.data)
        );
      });

  }
}
</script>
<style scoped>
</style>
