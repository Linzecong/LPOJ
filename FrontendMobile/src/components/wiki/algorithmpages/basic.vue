<template>
  <div>
    <el-row>
      <el-col :span="4">
        <el-menu default-active="basic_index" @select="handleSelect">
          <el-menu-item index="basic_index">基础简介</el-menu-item>
          <el-menu-item index="basic_enumerate">枚举</el-menu-item>
          <el-menu-item index="basic_simulate">模拟</el-menu-item>
          <el-menu-item index="basic_divideandconquer">递归与分治</el-menu-item>
          <el-menu-item index="basic_greedy">贪心</el-menu-item>
          <el-submenu index="1">
            <template slot="title">排序</template>
            <el-menu-item-group>
              <el-menu-item index="basic_sortintro">排序简介</el-menu-item>
              <el-menu-item index="basic_selectionsort">选择排序</el-menu-item>
              <el-menu-item index="basic_bubblesort">冒泡排序</el-menu-item>
              <el-menu-item index="basic_insertion_sort">插入排序</el-menu-item>
              <el-menu-item index="basic_bucketsort">计数排序</el-menu-item>
              <el-menu-item index="basic_quicksort">快速排序</el-menu-item>
              <el-menu-item index="basic_mergesort">归并排序</el-menu-item>
              <el-menu-item index="basic_heapsort">堆排序</el-menu-item>
              <el-menu-item index="basic_radixsort">基数排序</el-menu-item>
              <el-menu-item index="basic_shellsort">希尔排序</el-menu-item>
              <el-menu-item index="basic_stlsort">排序相关 STL</el-menu-item>
              <el-menu-item index="basic_useofsort">排序应用</el-menu-item>
            </el-menu-item-group>
          </el-submenu>
          <el-menu-item index="basic_expression">表达式求值</el-menu-item>
          <el-menu-item index="basic_binary">二分与三分</el-menu-item>
          <el-menu-item index="basic_construction">构造</el-menu-item>
          <el-menu-item index="basic_prefixsum">前缀和 & 差分</el-menu-item>
          <el-menu-item index="basic_fileoperation">文件操作</el-menu-item>

          <el-submenu index="2">
            <template slot="title">其他（额外添加）</template>
            <el-menu-item-group>
              <el-menu-item
                :key="index"
                v-for="(item,index) in menulist"
                :index="item.type"
              >{{item.title}}</el-menu-item>
            </el-menu-item-group>
          </el-submenu>
        </el-menu>
      </el-col>
      <el-col :span="20">
        <mavon-editor
          :boxShadow="false"
          :value="basicvalue"
          :subfield="prop.subfield"
          :defaultOpen="prop.defaultOpen"
          :toolbarsFlag="prop.toolbarsFlag"
          :editable="prop.editable"
          :scrollStyle="prop.scrollStyle"
          :autofocus="false"
          v-loading="loading"
          :key="basicvalue"
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
  name: "basic",
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
      basicvalue: "",
      tableData: [],
      curTypeValue: "",
      curUserValue: "",
      loading: false,
      menulist: []
    };
  },
  created() {
    this.getdata("std", "basic_index");

    this.$axios
      .get("/wiki/?group=basic&std=1")
      .then(response => {
        this.menulist = response.data;
      })
      .catch(error => {
        this.$message.error(
          "服务器错误！" + "(" + JSON.stringify(error.response.data) + ")"
        );
      });
  },
  watch: {
    basicvalue: function() {
      console.log('data changed');
      this.$nextTick().then(()=>{
        this.reRender();
      });
    }
  },
  methods: {
    reRender() {
      if(window.MathJax) {
        console.log('rendering mathjax');
        MathJax.Hub.Config({
            tex2jax: {
                inlineMath: [ ['$','$'], ["\\(","\\)"] ],
                displayMath: [ ['$$','$$'], ["\\[","\\]"] ]
            }
        });
        window.MathJax.Hub.Queue(["Typeset", window.MathJax.Hub], () => console.log('done'));
      }
    },
    handleSelect(key, keyPath) {
      this.getdata("std", key);
    },
    getdata(username, type) {
      if (this.curUserValue != username || this.curTypeValue != type) {
        this.basicvalue = "";
        this.curUserValue = username;
        this.curTypeValue = type;
      } else return;
      this.loading = true;
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
          this.basicvalue =
            response.data.length > 0 ? response.data[0].value : "# 暂无标准数据，请切换版本你想要的版本！";
          this.loading = false;
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
