<template>
  <el-row>
    <el-row>
      <el-form>
        <el-column>
          <el-form-item label="班级名称">
            <el-input v-model="form.className"
                      style="width:500px"></el-input>
          </el-form-item>
        </el-column>

        <el-column>
          <el-form-item label="班级总人数">
            <el-input v-model="form.classSize"
                      style="width:500px"></el-input>
          </el-form-item>
        </el-column>

        <el-column>
          <el-button round
                     @click="AddClass">增加班级</el-button>
        </el-column>
      </el-form>

    </el-row>
    <el-row>
      <el-table :data="tableData"
                style="width: 100%">
        <el-table-column prop="className"
                         label="班级"
                         width="300">
        </el-table-column>
        <el-table-column prop="classSize"
                         label="人数"
                         width="300">
        </el-table-column>

        <el-table-column prop="Operate"
                         label="操作"
                         width="500">
          　　　　<template slot-scope="scope">
            　　　　　　<el-button type="primary"
                       size="small"
                       @click="CheckDetail(scope.row)">查看详情</el-button>
            　　　　　　
            　　　　　　<el-button type="primary"
                       size="small"
                       @click="DeleteClass(scope.row)">删除</el-button>

            　　　　</template>
        </el-table-column>

      </el-table>
    </el-row>
  </el-row>
</template>

<script>
export default {
  name: "adminclassmanage",
  data () {
    return {
      dialogFormVisible: false,


      tableData: [],
      tableData2: [],
      form: {
        className: "",
        classSize: "",
      },
      deleteId: "",
    };
  },
  methods: {
    AddClass () {
      console.log(this.form);
      this.$axios.post("/ADDclasses/", this.form)
        .then(
          response => {
            this.$message({
              message: "添加班级成功！",
              type: "success"
            });
          }
        )
    },
    CheckDetail (row) {
      window.open("/classdetail?className=" + row.className);
      console.log(row.className);
    },
    DeleteClass (row) {
      console.log(row.className);
      this.$confirm(
        "确定删除" + row.className + "吗?",
        {
          confirmButtonText: "确定",
          cancelButtonText: "取消",
          type: "warning"
        }
      ).then(() => {
        this.$axios.delete("/DeleteClass/",
          {
            data: {
              className: row.className
            }
          })
          .then(response => {

            if (response.data == "AlreadyDelete") {
              this.$message.error("已删除班级");
              return;
            }
            if (response.data == "DeleteFail") {
              this.$message.error("删除班级失败（" + response + "）");
              return;
            }
            if (response.data == "DeleteOk") {
              this.$message({
                message: "已删除班级" + this.form.className,
                type: "success"
              });
            }
          })
      })
    },
  },
  created () {

    this.$axios.get("/classes/")
      .then(response => {
        console.log(response.data),
          this.tableData = response.data;
      })
// this.$set(this.tableData);



  },
  mounted () {
  },
}
</script>


<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>
