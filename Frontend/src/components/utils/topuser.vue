<template>
  <el-card>
    <div slot="header">
      <b>Top User</b>
    </div>
    <el-table
      :data="tableData"
      border
      style="width: 100%"
      @cell-click="userclick"
      size="mini"
      :row-style="ratingcolor"
    >
      <el-table-column type="index" width="40"></el-table-column>
      <el-table-column prop="username" label="User"></el-table-column>
      <el-table-column prop="rating" label="Score"></el-table-column>
    </el-table>
  </el-card>
</template>

<script>
export default {
  name: "topuser",
  data() {
    return {tableData:[]};
  },
  methods: {
    ratingcolor({ row, rowIndex }) {
      if (row.rating >= 3000) return "color:red;font-weight: bold;";
      if (row.rating >= 2600) return "color:#BB5E00;font-weight: bold;";
      if (row.rating >= 2200) return "color:#E6A23C;font-weight: bold;";
      if (row.rating >= 2050) return "color:#930093;font-weight: bold;";
      if (row.rating >= 1900) return "color:#0000AA;font-weight: bold;";
      if (row.rating >= 1700) return "color:#007799;font-weight: bold;";
      if (row.rating >= 1500) return "color:#227700;font-weight: bold;";
      if (row.rating >= 1350) return "color:#67C23A;font-weight: bold;";
      if (row.rating >= 1200) return "color:#909399;font-weight: bold;";
      return "color:#303133;font-weight: bold;";
    },
    userclick(row, column, cell, event) {
      this.$router.push({
        name: "user",
        query: { username: row.username }
      });
    }
  },
  created() {
    this.$axios
      .get("/userdata/?limit=10&offset=0")
      .then(response => {
        this.tableData = response.data.results;
      });
  }
};
</script>

<style  scoped>
</style>