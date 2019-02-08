<template>
  <div id="app">
    <el-col :span="24">
      <el-menu
        :default-active="activeIndex"
        mode="horizontal"
        @select="handleSelect"
        v-bind:router="true"
        id="nav"
      >
        <el-menu-item index="/" id="title">GDUFS Online Judge</el-menu-item>
        <el-menu-item index="/main">
          <i class="el-icon-star-off"></i>Home
        </el-menu-item>
        <el-menu-item index="/problem">
          <i class="el-icon-menu"></i>Problem
        </el-menu-item>
        <el-menu-item index="/statue">
          <i class="el-icon-tickets"></i>Status
        </el-menu-item>
        <el-menu-item index="/contest">
          <i class="el-icon-bell"></i>Contest
        </el-menu-item>
        <el-menu-item index="/rank">
          <i class="el-icon-star-on"></i>Rank
        </el-menu-item>
        <el-menu-item index="/blog">
          <i class="el-icon-edit-outline"></i>Blog
        </el-menu-item>
        <el-menu-item index="/about">
          <i class="el-icon-document"></i>About
        </el-menu-item>
      </el-menu>
    </el-col>
    <transition name="el-zoom-in-center" mode="out-in">
      <router-view id="route"></router-view>
    </transition>
  </div>
</template>

<script>
export default {
  name: "App",
  data() {
    return {
      activeIndex: "1"
    };
  },
  methods: {
    handleSelect(key, keyPath) {}
  }
};
</script>

<style scope>
#nav {
  position: fixed;
  left: 0px;
  top: 0px;
  width: 100%;
  z-index: 9999;
  box-shadow: 00px 0px 00px rgb(255, 255, 255),
    /*左边阴影*/ 0px 0px 10px rgb(255, 255, 255),
    /*上边阴影*/ 0px 0px 0px rgb(255, 255, 255),
    /*右边阴影*/ 1px 1px 0px rgb(218, 218, 218); /*下边阴影*/
}
#route {
  position: relative;
  top: 65px;
}
#title {
  font-size: 20px;
  font-weight: bold;
}
</style>
