<template>
  <div>
    <el-row>
      <el-col :span="4">
        <el-menu default-active="ds_index" @select="handleSelect">
          <el-menu-item index="ds_index">数据结构简介</el-menu-item>
            <el-submenu index="1">
            <template slot="title">STL</template>
            <el-menu-item-group>
              <el-menu-item index="ds_stl">STL 简介</el-menu-item>
              <el-menu-item index="ds_vector">vector</el-menu-item>
              <el-menu-item index="ds_priorityqueue">priority_queue</el-menu-item>
              <el-menu-item index="ds_map">map</el-menu-item>
              <el-menu-item index="ds_bitset">bitset</el-menu-item>
            </el-menu-item-group>
          </el-submenu>

          <el-submenu index="2">
            <template slot="title">pb_ds</template>
            <el-menu-item-group>
              <el-menu-item index="ds_pbds">pb-ds</el-menu-item>
              <el-menu-item index="ds_pbdspriorityqueue">__gnu_pbds::priority_queue</el-menu-item>
            </el-menu-item-group>
          </el-submenu>

          <el-menu-item index="ds_stack">栈</el-menu-item>
          <el-menu-item index="ds_queue">队列</el-menu-item>
          <el-menu-item index="ds_linkedlist">链表</el-menu-item>
          <el-menu-item index="ds_hash">哈希表</el-menu-item>
          <el-menu-item index="ds_dsu">并查集</el-menu-item>
          <el-submenu index="3">
            <template slot="title">堆</template>
            <el-menu-item-group>
              <el-menu-item index="ds_heap">堆简介</el-menu-item>
              <el-menu-item index="ds_binaryheap">二叉堆</el-menu-item>
              <el-menu-item index="ds_pairingheap">配对堆</el-menu-item>
            </el-menu-item-group>
          </el-submenu>
          <el-submenu index="4">
            <template slot="title">块状数据结构</template>
            <el-menu-item-group>
              <el-menu-item index="ds_squarerootdecomposition">分块思想</el-menu-item>
              <el-menu-item index="ds_blocklist">块状链表</el-menu-item>
              <el-menu-item index="ds_blockarray">块状数组</el-menu-item>
              <el-menu-item index="ds_treedecompose">树分块</el-menu-item>
            </el-menu-item-group>
          </el-submenu>
            <el-menu-item index="ds_monotonousstack">单调栈</el-menu-item>
          <el-menu-item index="ds_monotonousqueue">单调队列</el-menu-item>
          <el-menu-item index="ds_sparsetable">倍增</el-menu-item>
          <el-menu-item index="ds_bit">树状数组</el-menu-item>
          <el-menu-item index="ds_segment">线段树</el-menu-item>
            <el-menu-item index="ds_dividing">划分树</el-menu-item>

          <el-submenu index="5">
            <template slot="title">平衡树</template>
            <el-menu-item-group>
              <el-menu-item index="ds_bst">二叉搜索树简介</el-menu-item>
              <el-menu-item index="ds_treap">Treap</el-menu-item>
              <el-menu-item index="ds_splay">Splay</el-menu-item>
              <el-menu-item index="ds_wblt">WBLT</el-menu-item>
              <el-menu-item index="ds_sbt">Size Balanced Tree</el-menu-item>
              <el-menu-item index="ds_avl">AVL 树</el-menu-item>
              <el-menu-item index="ds_scapegoat">替罪羊树</el-menu-item>
            </el-menu-item-group>
          </el-submenu>

          <el-submenu index="6">
            <template slot="title">树套树</template>
            <el-menu-item-group>
              <el-menu-item index="ds_seginseg">线段树套线段树</el-menu-item>
              <el-menu-item index="ds_seginbalanced">平衡树套线段树</el-menu-item>
              <el-menu-item index="ds_balancedinseg">线段树套平衡树</el-menu-item>
              <el-menu-item index="ds_persistentinbit">树状数组套主席树</el-menu-item>
            </el-menu-item-group>
          </el-submenu>
            <el-menu-item index="ds_kdtree">K-Dtree</el-menu-item>

          <el-submenu index="7">
            <template slot="title">可持久化数据结构</template>
            <el-menu-item-group>
              <el-menu-item index="ds_persistent">可持久化数据结构简介</el-menu-item>
              <el-menu-item index="ds_persistentseg">可持久化线段树</el-menu-item>
              <el-menu-item index="ds_persistentblockarray">可持久化块状数组</el-menu-item>
              <el-menu-item index="ds_persistentbalanced">可持久化平衡树</el-menu-item>
              <el-menu-item index="ds_persistenttrie">可持久化字典树</el-menu-item>
            </el-menu-item-group>
          </el-submenu>


          <el-menu-item index="ds_odt">珂朵莉树</el-menu-item>
          <el-menu-item index="ds_lct">Link Cut Tree</el-menu-item>
          <el-menu-item index="ds_ett">Euler Tour Tree</el-menu-item>
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
          :value="dsvalue"
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
  name: "ds",
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
      dsvalue: "",
      tableData: [],
      curTypeValue: "",
      curUserValue: "",
      loading:false,
      menulist: []
    };
  },
  created() {
    this.getdata("std", "ds_index");
    this.$axios
      .get("/wiki/?group=ds&std=1")
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
    dsvalue: function() {
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
        this.dsvalue = "";
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

          this.dsvalue = response.data.length>0?response.data[0].value:"# 暂无标准数据，请切换版本你想要的版本！";
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
