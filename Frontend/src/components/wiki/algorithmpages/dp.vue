<template>
  <div>
    <el-row>
      <el-col :span="4">
        <el-menu default-active="dp_index" @select="handleSelect">
          <el-menu-item index="dp_index">动态规划简介</el-menu-item>
          <el-menu-item index="dp_memo">记忆化搜索</el-menu-item>
          <el-menu-item index="dp_knapsack">背包 DP</el-menu-item>
          <el-menu-item index="dp_interval">区间 DP</el-menu-item>
          <el-menu-item index="dp_dag">DAG 上的 DP</el-menu-item>
          <el-menu-item index="dp_tree">树形 DP</el-menu-item>
          <el-menu-item index="dp_state">状压 DP</el-menu-item>
          <el-menu-item index="dp_number">数位 DP</el-menu-item>
          <el-menu-item index="dp_plug">插头 DP</el-menu-item>
          <el-submenu index="1">
            <template slot="title">DP 优化</template>
            <el-menu-item-group>
              <el-menu-item index="dp_binaryknapsack">二进制分组解多重背包</el-menu-item>
              <el-menu-item index="dp_monotonousqueuestack">单调队列/单调栈优化</el-menu-item>
              <el-menu-item index="dp_convexhulloptimization">斜率优化</el-menu-item>
              <el-menu-item index="dp_knuthyaoquadrangleinequality">四边形不等式优化</el-menu-item>
              <el-menu-item index="dp_stateoptimization">状态设计优化</el-menu-item>
            </el-menu-item-group>
          </el-submenu>
          <el-menu-item index="dp_misc">其他 DP</el-menu-item>
        </el-menu>
      </el-col>
      <el-col :span="20">
        <mavon-editor
          :boxShadow="false"
          :value="dpvalue"
          :subfield="prop.subfield"
          :defaultOpen="prop.defaultOpen"
          :toolbarsFlag="prop.toolbarsFlag"
          :editable="prop.editable"
          :scrollStyle="prop.scrollStyle"
          :autofocus="false"
        ></mavon-editor>
      </el-col>
    </el-row>
    <el-row style="margin-left:15px">
      <br>
      <p>选择其他版本</p>
      <el-table :data="tableData" @cell-click="userclick" style="float:left;width:40%;">
        <el-table-column type="index"></el-table-column>
        <el-table-column prop="username" label="User" :width="200"></el-table-column>
        <el-table-column prop="time" label="Last Edit Time"></el-table-column>
      </el-table>
    </el-row>
  </div>
</template>

<script>
import moment from "moment";
import { mavonEditor } from "mavon-editor";
import "mavon-editor/dist/css/index.css";
export default {
  name: "dp",
  components: {
    mavonEditor
  },
  computed: {
    prop() {
      let data = {
        subfield: false, // 单双栏模式
        defaultOpen: "preview", //edit： 默认展示编辑区域 ， preview： 默认展示预览区域
        editable: false,
        toolbarsFlag: false,
        scrollStyle: true
      };
      return data;
    }
  },
  data() {
    return {
      dpvalue: "",
      tableData: [],
      curTypeValue: "",
      curUserValue: ""
    };
  },
  created() {
    this.getdata("std", "dp_index");
  },
  methods: {
    handleSelect(key, keyPath) {
      this.getdata("std", key);
    },
    getdata(username, type) {
      if (this.curUserValue != username || this.curTypeValue != type) {
        this.dpvalue = "";
        this.curUserValue = username;
        this.curTypeValue = type;
      } else return;

      this.$axios
        .get("/wikicount/?type=" + type)
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

      this.$axios
        .get("/wiki/?username=" + username + "&type=" + type)
        .then(response => {
          this.dpvalue = response.data.length>0?response.data[0].value:"# 暂无数据";
        })
        .catch(error => {
          this.$message.error(
            "服务器错误！" + "(" + JSON.stringify(error.response.data) + ")"
          );
        });
    },
    userclick(row, column, cell, event) {
      this.getdata(row.username, this.curTypeValue);
    }
  }
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>
