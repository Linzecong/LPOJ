<template>
  <el-row :gutter="10">
    <el-col :span="8">
      <el-card>
        <div slot="header">
          <b style="color:#409EFF">进入LPOJ试炼谷</b>
        </div>
        <b>
          <el-button style="width:100%;" @click="trainningClick" type="primary">开始试炼</el-button>
        </b>
      </el-card>
    </el-col>
    <el-col :span="8">
      <el-card>
        <div slot="header">
          <b style="color:#409EFF">快速查算法</b>
        </div>
        <b>
          <el-button style="width:100%;" icon="el-icon-search" @click="searchtitle">点击此处搜索算法</el-button>
        </b>
      </el-card>
    </el-col>
    <el-col :span="8">
      <el-card>
        <div slot="header">
          <b style="font-size:14.5px">AC自动机Fail树上DFS序建可持久化线段树</b>
        </div>
        <b style="font-size:14.5px;margin-top:10px">后缀自动机Next指针建的DAG上跑SG函数</b>
        <h2></h2>
      </el-card>
    </el-col>
  </el-row>
</template>

<script>
export default {
  name: "soulrow",
  data() {
    return {};
  },
  methods: {
    trainningClick() {
      this.$router.push({
        name: "trainning"
      });
    },
    searchtitle() {
      this.$router.push({
        name: "wikidetail",
        params: { wikiid: "intro_index" }
      });
    }
  }
};
</script>

<style  scoped>
</style>