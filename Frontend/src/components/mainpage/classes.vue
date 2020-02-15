
<template>
  <el-tabs v-model="activeName"
           type="border-card">
    <el-tab-pane label="加入班级"
                 name="JoinClass">
      <template>
        <el-table :data="tableData"
                  style="width: 100%">
          <el-table-column prop="className"
                           label="班级"
                           width="400"
                           align="center">
          </el-table-column>
          <el-table-column prop="classSize"
                           label="人数"
                           width="200"
                           align="center">
          </el-table-column>
          <el-table-column label="操作"
                           align="center"
                           min-width="200">
            　　　　<template slot-scope="scope">
              　　　　　　<el-button type="primary"
                         size="small"
                         round
                         @click="JoinClick(scope.row)">加入</el-button>
              　　　　</template>
            　　</el-table-column>
        </el-table>
      </template>

    </el-tab-pane>
    <el-tab-pane label="我的班级"
                 name="MyClass">

      <template>
        <el-table :data="tableData2"
                  style="width: 100%">
          <el-table-column prop="className"
                           label="班级"
                           width="400"
                           align="center">
          </el-table-column>

          <el-table-column label="操作"
                           align="center"
                           min-width="200">
            　　　　<template slot-scope="scope">
              <el-button type="primary"
                         size="small"
                         round
                         @click="homework(scope.row)">作业</el-button>
            </template>
            　　</el-table-column>

          <el-table-column label="操作"
                           align="center"
                           min-width="200">
            　　　　<template slot-scope="scope">

              　　　　　　<el-button type="primary"
                         size="small"
                         round
                         @click="QuitClick(scope.row)">退出</el-button>
              　　　　
            </template>
            　　</el-table-column>

        </el-table>
      </template>

    </el-tab-pane>
  </el-tabs>
</template>

<script>
export default {
  name: "classes",
  data () {
    return {

      cName: [],
      classCount: "",
      cPeoplecount: [],

      tableData: [],
      tableData2: [],
      form: {
        className: "",
        studentUserName: "",
        studentNumber: "",
        studentRealName: "",
      },
      deleteId: "",
    };
  },
  methods: {
    homework (row) {
      window.open("/homework?className=" + row.className);
    },
    JoinClick (row) {
      this.$axios.get("/classes/?className=" + row.className)
        .then(res => {
          if (res.data[0].canjoinclass === "close") {
            this.$message.error(row.className + "目前不开放加入");
            return;
          }
          else {
            this.$confirm(
              "确定加入" + row.className + "吗?",
              {
                confirmButtonText: "确定",
                cancelButtonText: "取消",
                type: "warning"
              }
            ).then(() => {
              this.form.className = row.className;
              this.$axios.get("/user/?username=" + sessionStorage.username)
                .then(
                  response => {
                    this.form.studentUserName = response.data[0].username;
                    this.form.studentRealName = response.data[0].realname;
                    this.form.studentNumber = response.data[0].number;
                  }
                ).catch(function (error) {
                  console.log(error);
                });
              this.$axios.post("/AddClass/", this.form)
                .then(response => {
                  if (response.data == "JoinOk") {
                    this.$message.success("加入成功！");

                    return;
                  }
                  if (response.data == "RepeatJoin") {
                    this.$message.error("请不要重复加入同一班级！");
                    return;
                  }
                  if (response.data == "JoinFail") {
                    this.$message.error("加入班级失败（" + response + "）");
                    return;
                  }
                  this.$message({
                    message: "加入班级成功！",
                    type: "success"
                  });
                }
                );
            })
          }
        }).catch(error => {
          this.$message.error(
            "服务器错误！" + "(" + JSON.stringify(error.response.data) + ")"
          );
        });

    },

    QuitClick (row) {
      this.$confirm(
        "确定退出" + row.className + "吗?",
        {
          confirmButtonText: "确定",
          cancelButtonText: "取消",
          type: "warning"
        }
      ).then(() => {
        //获取学号
        // this.$axios.get("/user/?username=" + sessionStorage.username)
        //   .then(
        //     response => {
        //       this.form.studentNumber = response.data[0].number;
        //     }
        //   ).catch(function (error) {
        //     console.log(error);
        //   });
        // this.form.className = row.className;

        this.$axios.get("/classStudent/?studentUserName=" + sessionStorage.username + "&className=" + row.className)
          .then(
            response => {

              var deleteId = response.data[0].id;
              this.$axios.delete("/classStudent/" + deleteId + "/");
              this.$message("已退出班级");
            }
          ).catch(function (error) {
            console.log(error);
          });


        // this.$axios.delete("/QuitClass/",
        //   {
        //     data: {
        //       studentNumber: this.form.studentNumber,
        //       studentUserName: this.form.studentUserName,
        //       studentRealName: this.form.studentRealName,
        //       className: row.className
        //     }
        //   })
        //   .then(response => {
        //     if (response.data == "QuitOk") {
        //       this.$message.success("已退出班级");
        //       return;
        //     }
        //     if (response.data == "AlreadyQuit") {
        //       this.$message.error("已退出班级");
        //       return;
        //     }
        //     if (response.data == "QuitFail") {
        //       this.$message.error("退出班级失败（" + response + "）");
        //       return;
        //     }
        //     // if (response.data == "QuitOk") {
        //     //   this.$message({
        //     //     message: "已退出班级" + this.form.className,
        //     //     type: "success"
        //     //   });
        //     // }
        //   })
      })
    },
  },
  created () {
    this.form.studentUserName = sessionStorage.username;

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
    this.$axios.get("/classStudent/?studentUserName=" + sessionStorage.username)
      .then(response => {
        this.tableData2 = response.data;
      })
  },
}
</script>

<style scoped>
h1 {
  position: relative;
}
</style>
