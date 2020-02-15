<template>
  <el-row>
    <el-row>
      <el-form>
        <el-col>
          <el-form-item label="班级名称">
            <el-input v-model="form.className"
                      style="width:500px"></el-input>
          </el-form-item>
        </el-col>

        <el-col>
          <el-form-item label="班级总人数">
            <el-input v-model="form.classSize"
                      style="width:500px"></el-input>
          </el-form-item>
        </el-col>

        <el-col>
          <el-button round
                     @click="AddClass">增加班级</el-button>
        </el-col>
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
                         width="600">
          　　　　<template slot-scope="scope">
            　　　　　　<el-button type="primary"
                       size="small"
                       @click="CheckDetail(scope.row)">查看详情</el-button>
            　　　　　　
            　　　　　　<el-button type="danger"
                       size="small"
                       @click="DeleteClass(scope.row)">删除</el-button>

            <el-button type="success"
                       size="small"
                       @click="openClass(scope.row)">开放加入</el-button>

            <el-button type="warning"
                       size="small"
                       @click="closeClass(scope.row)">关闭加入</el-button>

          </template>
        </el-table-column>

        <el-table-column prop="canjoinclass"
                         label="开放状态"
                         width="300">
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
      cName: [],
      classCount: "",
      tmpform: [],
      cPeoplecount: [],
      form: {
        className: "",
        classSize: "",
      },
      deleteId: "",
    };
  },
  methods: {
    openClass (row) {
      this.tmpform = row;
      this.tmpform.canjoinclass = "open";

      var tmpsize = this.tmpform.classSize.split("/");
      this.tmpform.classSize = tmpsize[1];
      this.$axios.get("/classes/?className=" + row.className)
        .then(res => {
          var putId = res.data[0].id;
          this.$axios.put("/classes/" + putId + "/", this.tmpform)
            .then(res2 => {
              this.$message.success("已开放班级" + row.className);
            })
            .catch(error => {
              this.$message.error(
                "服务器错误！" + "(" + JSON.stringify(error.response.data) + ")"
              );
            });
        })

      this.tmpform.classSize = tmpsize[0] + "/" + tmpsize[1];

    },
    closeClass (row) {
      this.tmpform = row;
      this.tmpform.canjoinclass = "close";

      var tmpsize = this.tmpform.classSize.split("/");
      this.tmpform.classSize = tmpsize[1];

      this.$axios.get("/classes/?className=" + row.className)
        .then(res => {
          var putId = res.data[0].id;
          this.$axios.put("/classes/" + putId + "/", this.tmpform)
            .then(res2 => {
              this.$message.success("已关闭班级" + row.className);
            })
            .catch(error => {
              this.$message.error(
                "服务器错误！" + "(" + JSON.stringify(error.response.data) + ")"
              );
            });
        })


      this.tmpform.classSize = tmpsize[0] + "/" + tmpsize[1];
    },
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
    },
    DeleteClass (row) {
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
        this.classCount = response.data.length;
        this.tableData = response.data;
        for (var i = 0; i < response.data.length; i++) {
          this.cName.push(response.data[i].className);
        };
        (async () => {
          const dataArray = await Promise.all(
            this.cName.map(i => this.$axios.get(`/classStudent/?className=${i}`))
          );
          for (const { data } of dataArray) {
            if (typeof data === "object" && typeof data.length === "number") {
              this.cPeoplecount.push(JSON.stringify(data.length));
            }
          }
          console.log(this.cPeoplecount);
          for (var ii = 0; ii < this.classCount; ii++) {
            this.tableData[ii].classSize = this.cPeoplecount[ii] + "/" + this.tableData[ii].classSize;
          }
        })();
      })
  },
  mounted () {
  },
}
</script>


<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>
