<template>
  <el-column>
    <el-row>
      <center>
        <h1>{{className}}</h1>
        <br>
        <h2>目前共{{classPeopleCount}}人</h2>

      </center>
    </el-row>
    <el-row>
      <el-input placeholder="输入用户名/学号/姓名以搜索..."
                v-model="searchstudent"
                @keyup.native.enter="searchstu"
                style="float:right;width:300px;">
        <el-button slot="append"
                   icon="el-icon-search"
                   @click="searchstu"></el-button>
      </el-input>

      <el-table :data="TableData"
                style="width: 100%">
        <el-table-column prop="studentUserName"
                         label="用户名"
                         width="300">
        </el-table-column>
        <el-table-column prop="studentRealName"
                         label="真实姓名"
                         width="300">
        </el-table-column>
        <el-table-column prop="studentNumber"
                         label="学号"
                         width="300">
        </el-table-column>

        <el-table-column prop="Operate"
                         label="操作"
                         width="500">
          　　　　<template slot-scope="scope">
            　　　　　　
            　　　　　　<el-button type="primary"
                       size="small"
                       @click="DeleteStudent(scope.row)">删除</el-button>

            　　　　</template>
        </el-table-column>

      </el-table>
    </el-row>
  </el-column>
</template>

<script>
export default {
  data () {
    return {
      searchstudent: "",
      classPeopleCount: "",
      className: "",
      TableData: [],
    }
  },
  methods: {
    searchstu () {
      this.$axios
        .get(
          "/classStudent/?search=" +
          this.searchstudent
        )
        .then(response => {
          this.TableData = response.data;
        });
    },
    DeleteStudent (row) {
      this.$axios.get("/classStudent/?studentName=" + row.studentName + "&className=" + this.className)
        .then(
          response => {
            var deleteStudentId = response.data[0].id;
            this.$axios.delete("/classStudent/" + deleteStudentId + "/");
            this.$message.error("已删除");
          }
        )
    },
  },
  created () {
    console.log(this.className);
    this.className = this.$route.query.className;
    this.$axios.get("/classStudent/?className=" + this.className)
      .then(
        response => {

          console.log(response.data);
          this.classPeopleCount = response.data.length;
          this.TableData = response.data;
        }
      )

  },

}
</script>

<style scoped>
</style>
