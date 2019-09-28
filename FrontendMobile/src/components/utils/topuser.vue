<template>
  <mu-card>
    <mu-card-title title="Top User"></mu-card-title>

    <mu-card-text>
      <mu-data-table
        :columns="columns"
        :data="tableData"
        @row-click="userclick"
        :rowStyle="ratingcolor"
      >
        <template slot-scope="scope">
          <td>{{scope.row.username}}</td>
          <td>{{scope.row.rating}}</td>
        </template>
      </mu-data-table>
    </mu-card-text>
  </mu-card>
</template>

<script>
export default {
  name: "topuser",
  data() {
    return {
      columns: [
        { title: "UserName", name: "username" },
        { title: "Rating", name: "rating" }
      ],
      tableData: []
    };
  },
  methods: {
    ratingcolor(rowIndex, row) {
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
    userclick(index, row) {
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
      })
      .catch(error => {
        this.$toast.error(
          "服务器错误！" + "(" + JSON.stringify(error.response.data) + ")"
        );
      });
  }
};
</script>

<style  scoped>
</style>