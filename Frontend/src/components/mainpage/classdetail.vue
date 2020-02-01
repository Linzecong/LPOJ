<template>
  <el-column>
    <el-row>
      <center>
        <h1>{{className}}</h1>

      </center>
    </el-row>
    <el-row>
      <el-table :data="TableData"
                style="width: 100%">
        <el-table-column prop="studentName"
                         label="姓名"
                         width="300">
        </el-table-column>
        <el-table-column prop="studentNumber"
                         label="学号"
                         width="300">
        </el-table-column>
      </el-table>
    </el-row>
  </el-column>
</template>

<script>
export default {
  data () {
    return {
      className: "",
      TableData: [],
    }
  },
  created () {
    console.log(this.className);
    this.className = this.$route.query.className;
    this.$axios.get("/classStudent/?className=" + this.className)
      .then(
        response => {

          console.log(response.data);
          this.TableData = response.data;
        }
      )

  },
}
</script>

<style scoped>
</style>
