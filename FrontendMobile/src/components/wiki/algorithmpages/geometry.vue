<template>
  <div>
    <el-row>
      <el-col :span="4">
        <el-menu default-active="geometry_index" @select="handleSelect">
          <el-menu-item index="geometry_index">计算几何简介</el-menu-item>
          <el-menu-item index="geometry_2d">二维计算几何基础</el-menu-item>
          <el-menu-item index="geometry_3d">三维计算几何基础</el-menu-item>
          <el-menu-item index="geometry_distance">距离</el-menu-item>
          <el-menu-item index="geometry_pick">Pick 定理</el-menu-item>
          <el-menu-item index="geometry_triangulation">三角剖分</el-menu-item>
          <el-menu-item index="geometry_convexhull">凸包</el-menu-item>
          <el-menu-item index="geometry_scanning">扫描线</el-menu-item>
          <el-menu-item index="geometry_rotatingcalipers">旋转卡壳</el-menu-item>
          <el-menu-item index="geometry_halfplaneintersection">半平面交</el-menu-item>
          <el-menu-item index="geometry_nearestpoints">平面最近点对</el-menu-item>
          <el-menu-item index="geometry_magic">计算几何杂项</el-menu-item>
          <el-submenu index="8">
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
          :value="geometryvalue"
          :subfield="prop.subfield"
          :defaultOpen="prop.defaultOpen"
          :toolbarsFlag="prop.toolbarsFlag"
          :editable="prop.editable"
          :scrollStyle="prop.scrollStyle"
          :autofocus="false"
          v-loading="loading"
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
  name: "geometry",
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
      geometryvalue: "",
      tableData: [],
      curTypeValue: "",
      curUserValue: "",
      loading: false,
      menulist: []
    };
  },
  created() {
    this.getdata("std", "geometry_index");
    this.$axios
      .get("/wiki/?group=geometry&std=1")
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
    geometryvalue: function() {
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
        this.geometryvalue = "";
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
          this.geometryvalue =
            response.data.length > 0 ? response.data[0].value : "# 暂无标准数据，请切换版本你想要的版本！";
            this.loading=false
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
