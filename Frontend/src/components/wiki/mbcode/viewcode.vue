<template>
  <el-card>
    <h2>{{username + "的代码库"}}</h2>
    <p>选择要查看的代码</p>

    <el-autocomplete
      placeholder="请输入分组来筛选题目"
      v-model="group"
      :fetch-suggestions="queryGroup"
      @keyup.native.enter="search"
      style="width:300px;"
      @select="search"
    >
      <el-button slot="append" icon="el-icon-search" @click="search"></el-button>
    </el-autocomplete>

    <el-autocomplete
      placeholder="请输入标题来筛选题目"
      v-model="title"
      @keyup.native.enter="search"
      style="margin-left:30px;width:300px;"
      :fetch-suggestions="queryTitle"
      @select="search"
    >
      <el-button slot="append" icon="el-icon-search" @click="search"></el-button>
    </el-autocomplete>
    <el-table
      :data="tableData"
      @cell-click="userclick"
      :default-sort="{prop: 'group', order: 'descending'}"
    >
      <el-table-column type="index"></el-table-column>
      <el-table-column prop="username" label="User" :width="200"></el-table-column>
      <el-table-column prop="group" label="Group"></el-table-column>
      <el-table-column prop="title" label="Title">
        <template slot-scope="scope">
          <el-popover trigger="hover" placement="top" :width="500">
            <p>Des: {{ scope.row.des }}</p>
            <div slot="reference" class="name-wrapper">
              <b>{{ scope.row.title }}</b>
            </div>
          </el-popover>
        </template>
      </el-table-column>
      <el-table-column prop="time" label="Time"></el-table-column>
    </el-table>
  </el-card>
</template>

<script>
import moment from "moment";
export default {
  name: "mbcodedetail",
  data() {
    return {
      username: this.$route.params.username,
      group: "",
      title: "",
      tableData: [],
      titles: [],
      groups: []
    };
  },
  created() {
    this.$axios
      .get(
        "/mbcodedetailnocode/?username=" +
          this.username +
          "&group=" +
          this.group +
          "&title=" +
          this.title
      )
      .then(response => {
        for (let i = 0; i < response.data.length; i++)
          response.data[i].time = moment(response.data[i].time).format(
            "YYYY-MM-DD HH:mm:ss"
          );
        this.tableData = response.data;
      })
      .catch(error => {
        this.$message.error(
          "服务器错误！" + "(" + JSON.stringify(error.response.data) + ")"
        );
      });
  },
  methods: {
    uniq(array) {
      var temp = []; //一个新的临时数组
      for (var i = 0; i < array.length; i++) {
        if (temp.indexOf(array[i]) == -1) {
          temp.push(array[i]);
        }
      }
      return temp;
    },
    queryGroup(queryString, cb) {
      this.groups = [];
      this.$axios
        .get("/mbcodedetailnocode/?username=" + this.username)
        .then(response => {
          for (let i = 0; i < response.data.length; i++) {
            this.groups.push(response.data[i].group);
          }

          this.groups = this.uniq(this.groups);
          var groups = this.groups;
          var results = queryString
            ? groups.filter(this.createStateFilter(queryString))
            : groups;
          var res = [];
          for (let i = 0; i < results.length; i++)
            res.push({ value: results[i] });
          cb(res);
        })
        .catch(error => {
          this.$message.error(
            "服务器错误！" + "(" + JSON.stringify(error.response.data) + ")"
          );
        });
    },
    queryTitle(queryString, cb) {
      this.titles = [];
      this.$axios
        .get(
          "/mbcodedetailnocode/?username=" +
            this.username +
            "&group=" +
            this.group
        )
        .then(response => {
          for (let i = 0; i < response.data.length; i++) {
            this.titles.push(response.data[i].title);
          }

          this.titles = this.uniq(this.titles);
          var titles = this.titles;
          var results = queryString
            ? titles.filter(this.createStateFilter(queryString))
            : titles;
          var res = [];
          for (let i = 0; i < results.length; i++)
            res.push({ value: results[i] });
          cb(res);
        })
        .catch(error => {
          this.$message.error(
            "服务器错误！" + "(" + JSON.stringify(error.response.data) + ")"
          );
        });
    },
    createStateFilter(queryString) {
      return state => {
        return state.indexOf(queryString) === 0;
      };
    },
    search() {
      this.$axios
        .get(
          "/mbcodedetailnocode/?username=" +
            this.username +
            "&group=" +
            this.group +
            "&title=" +
            this.title
        )
        .then(response => {
          for (let i = 0; i < response.data.length; i++)
            response.data[i].time = moment(response.data[i].time).format(
              "YYYY-MM-DD HH:mm:ss"
            );
          this.tableData = response.data;
        })
        .catch(error => {
          this.$message.error(
            "服务器错误！" + "(" + JSON.stringify(error.response.data) + ")"
          );
        });
    },
    userclick: function(row, column, cell, event) {
      this.$router.push({
        name: "viewcodedetail",
        params: { codeID: row.id }
      });
    }
  }
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>
