<template>
  <div>
    <el-tabs type="border-card">
      <el-tab-pane label="简介">
        <intro/>
      </el-tab-pane>
      <el-tab-pane label="基础算法" :lazy="true">
        <basic/>
      </el-tab-pane>
      <el-tab-pane label="搜索" :lazy="true">
        <search/>
      </el-tab-pane>
      <el-tab-pane label="动态规划" :lazy="true">
        <dp/>
      </el-tab-pane>
      <el-tab-pane label="字符串" :lazy="true">
        <string/>
      </el-tab-pane>
      <el-tab-pane label="数学" :lazy="true">
        <mymath/>
      </el-tab-pane>
      <el-tab-pane label="数据结构" :lazy="true">
        <ds/>
      </el-tab-pane>
      <el-tab-pane label="图论" :lazy="true">
        <graph/>
      </el-tab-pane>
      <el-tab-pane label="计算几何" :lazy="true">
        <geometry/>
      </el-tab-pane>
      <el-tab-pane label="杂项" :lazy="true">
        <misc/>
      </el-tab-pane>
      <el-tab-pane label="编辑词条" :lazy="true">
        <editalgorithm/>
      </el-tab-pane>
    </el-tabs>
  </div>
</template>

<script>
import intro from "@/components/wiki/algorithmpages/intro";
import basic from "@/components/wiki/algorithmpages/basic";
import dp from "@/components/wiki/algorithmpages/dp";
import ds from "@/components/wiki/algorithmpages/ds";
import geometry from "@/components/wiki/algorithmpages/geometry";
import graph from "@/components/wiki/algorithmpages/graph";
import mymath from "@/components/wiki/algorithmpages/math";
import misc from "@/components/wiki/algorithmpages/misc";
import search from "@/components/wiki/algorithmpages/search";
import string from "@/components/wiki/algorithmpages/string";
import editalgorithm from "@/components/wiki/algorithmpages/editalgorithm";
export default {
  name: "algorithm",
  components: {
    intro,
    basic,
    dp,
    ds,
    geometry,
    graph,
    mymath,
    misc,
    search,
    string,
    editalgorithm
  },
  data() {
    return {};
  },
  created() {},
  methods: {
    
  }
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>
