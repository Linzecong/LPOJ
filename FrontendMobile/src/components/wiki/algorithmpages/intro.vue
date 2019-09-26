<template>
  <div>
    <el-row>
      <el-col :span="4">
        <el-menu default-active="intro_index" @select="handleSelect">
          <el-menu-item index="intro_index">首页声明</el-menu-item>
          <el-menu-item index="intro_mode">赛事与赛制</el-menu-item>
          <el-menu-item index="intro_resource">学习资源</el-menu-item>
          <el-menu-item index="intro_mistake">常见错误</el-menu-item>
          <el-menu-item index="intro_trick">常见技巧</el-menu-item>
          <el-menu-item index="intro_nontraditional">非传统题</el-menu-item>
          <el-menu-item index="intro_about">关于OI Wiki</el-menu-item>
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
        <el-button style="width:100%;"  icon="el-icon-search" @click="searchtitle">点击此处搜索算法</el-button>
        <mavon-editor
        style="margin-top:15px;"
          :boxShadow="false"
          :value="introvalue"
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
  name: "code",
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
      introvalue: "",
      tableData: [],
      curTypeValue: "",
      curUserValue: "",
      loading:false,
      menulist: []
    };
  },
  created() {
    this.getdata("std", "intro_index");
    this.$axios
      .get("/wiki/?group=intro&std=1")
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
    introvalue: function() {
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
        this.introvalue = "";
        this.curUserValue = username;
        this.curTypeValue = type;
      } else return;
      this.loading=true
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
          this.introvalue = response.data.length>0?response.data[0].value:"# 暂无标准数据，请切换版本你想要的版本！";
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
    },
    searchtitle(){
      this.$router.push({
        name: "wikidetail",
        params: { wikiid: "intro_index" }
      });
    }
  }
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>
