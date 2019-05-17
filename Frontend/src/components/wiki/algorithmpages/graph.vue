<template>
  <div>
    <el-row>
      <el-col :span="4">
        <el-menu default-active="graph_index" @select="handleSelect">
          <el-menu-item index="graph_index">图论简介</el-menu-item>
          <el-menu-item index="graph_basic">图论基础</el-menu-item>
          <el-menu-item index="graph_traverse">图的遍历</el-menu-item>
          <el-submenu index="1">
            <template slot="title">树上问题</template>
            <el-menu-item-group>
              <el-menu-item index="graph_treebasic">树基础</el-menu-item>
              <el-menu-item index="graph_lca">最近公共祖先</el-menu-item>
              <el-menu-item index="graph_dfsorder">DFS 序</el-menu-item>
              <el-menu-item index="graph_treemisc">树重心</el-menu-item>
              <el-menu-item index="graph_treehash">树哈希</el-menu-item>
              <el-menu-item index="graph_heavylightdecomposition">树链剖分</el-menu-item>
              <el-menu-item index="graph_treedivide">树分治</el-menu-item>
              <el-menu-item index="graph_dynamictreedivide">动态树分治</el-menu-item>
              <el-menu-item index="graph_virtualtree">虚树</el-menu-item>
              <el-menu-item index="graph_dsuontree">树上启发式合并</el-menu-item>
            </el-menu-item-group>
          </el-submenu>

          <el-menu-item index="graph_matrixtree">矩阵树定理</el-menu-item>
          <el-menu-item index="graph_dag">有向无环图</el-menu-item>
          <el-menu-item index="graph_topo">拓扑排序</el-menu-item>
          <el-menu-item index="graph_mst">最小生成树</el-menu-item>
          <el-menu-item index="graph_mdst">最小树形图</el-menu-item>
          <el-menu-item index="graph_shortestpath">最短路</el-menu-item>
          <el-menu-item index="graph_differentialconstraints">差分约束</el-menu-item>
          <el-menu-item index="graph_kthpath">K 短路</el-menu-item>

          <el-submenu index="2">
            <template slot="title">连通性问题</template>
            <el-menu-item-group>
              <el-menu-item index="graph_scc">强连通分量</el-menu-item>
              <el-menu-item index="graph_bcc">双连通分量</el-menu-item>
              <el-menu-item index="graph_bridge">割点和桥</el-menu-item>
              <el-menu-item index="graph_2sat">2-SAT</el-menu-item>
            </el-menu-item-group>
          </el-submenu>

          <el-menu-item index="graph_euler">欧拉图</el-menu-item>
          <el-menu-item index="graph_hamilton">哈密顿图</el-menu-item>
          <el-menu-item index="graph_bigraph">二分图</el-menu-item>
          <el-menu-item index="graph_mincircle">最小环</el-menu-item>
          <el-menu-item index="graph_planar">平面图</el-menu-item>
          <el-menu-item index="graph_color">图的着色</el-menu-item>

          <el-submenu index="3">
            <template slot="title">网络流</template>
            <el-menu-item-group>
              <el-menu-item index="graph_flow">网络流简介</el-menu-item>
              <el-menu-item index="graph_maxflow">最大流</el-menu-item>
              <el-menu-item index="graph_flownode">拆点</el-menu-item>
              <el-menu-item index="graph_mincut">最小割</el-menu-item>
              <el-menu-item index="graph_mincost">费用流</el-menu-item>
              <el-menu-item index="graph_flowbound">上下界网络流</el-menu-item>
            </el-menu-item-group>
          </el-submenu>

          <el-menu-item index="graph_misc">图论杂项</el-menu-item>
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
          :value="graphvalue"
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
  name: "graph",
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
      graphvalue: "",
      tableData: [],
      curTypeValue: "",
      curUserValue: "",
      loading:false,
      menulist: []
    };
  },
  created() {
    this.getdata("std", "graph_index");
    this.$axios
      .get("/wiki/?group=graph&std=1")
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
    graphvalue: function() {
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
        this.graphvalue = "";
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
          this.graphvalue = response.data.length>0?response.data[0].value:"# 暂无标准数据，请切换版本你想要的版本！";
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
