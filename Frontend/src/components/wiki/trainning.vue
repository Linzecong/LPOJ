<template>
  <el-card>
    <center>
      <h2>欢迎来到试炼谷</h2>
      <h2>请选择你要挑战的章节</h2>
      <br>
      <el-row :gutter="40">
        <el-col :span="6">
          <el-card :body-style="{ padding: '0px' }" shadow="hover">
            <img
              src="https://www.lpoj.cn/1.png"
              class="image"
            >

            <div style="matgin:10px">
              <h2>
                新手村落
                <el-button type="primary" style="margin-left:20px;" @click="click(1)">进入章节</el-button>
              </h2>这里是新手村！在这里你可以学习到基本的编程支持，赶快上路吧！
            </div>
          </el-card>
        </el-col>
        <el-col :span="6">
          <el-card :body-style="{ padding: '0px' }" shadow="hover">
            <img
              src="https://www.lpoj.cn/2.png"
              class="image"
            >

            <div style="matgin:10px">
              <h2>
                蓝桥林地
                <el-button type="primary" style="margin-left:20px;" @click="click(2)">进入章节</el-button>
              </h2>蓝桥林地聚集了许许多多的小怪物！快去消灭它们吧！
            </div>
          </el-card>
        </el-col>
        <el-col :span="6">
          <el-card :body-style="{ padding: '0px' }" shadow="hover">
            <img src="https://www.lpoj.cn/3.png" class="image">

            <div style="matgin:10px">
              <h2>
                天梯孤岛
                <el-button type="primary" style="margin-left:20px;" @click="click(3)">进入章节</el-button>
              </h2>孤岛中有很多的小恶魔，快去征服他们吧！
            </div>
          </el-card>
        </el-col>
        <el-col :span="6">
          <el-card :body-style="{ padding: '0px' }" shadow="hover">
            <img
              src="https://www.lpoj.cn/4.png"
              class="image"
            >

            <div style="matgin:10px">
              <h2>
                省历练场
                <el-button type="primary" style="margin-left:20px;" @click="click(4)">进入章节</el-button>
              </h2>省历练场汇聚了许多精英，快来打败他们，参加国选吧！
            </div>
          </el-card>
        </el-col>
      </el-row>
      <el-row :gutter="40" style="margin-top:30px;">
        <el-col :span="6">
          <el-card :body-style="{ padding: '0px' }" shadow="hover">
            <img src="https://www.lpoj.cn/5.png" class="image">

            <div style="matgin:10px">
              <h2>
                国选营地
                <el-button type="primary" style="margin-left:20px;" @click="click(5)">进入章节</el-button>
              </h2>这里是国家选拔精英的地方，快快脱颖而出，一举成名吧！
            </div>
          </el-card>
        </el-col>
        <el-col :span="6">
          <el-card :body-style="{ padding: '0px' }" shadow="hover">
            <img src="https://www.lpoj.cn/6.png" class="image">

            <div style="matgin:10px">
              <h2>
                国斗兽场
                <el-button type="primary" style="margin-left:20px;" @click="click(6)">进入章节</el-button>
              </h2>在这里成为全国瞩目的编程小战士吧！打败他们，获取至高的荣耀!
            </div>
          </el-card>
        </el-col>
        <el-col :span="6">
          <el-card :body-style="{ padding: '0px' }" shadow="hover">
            <img
              src="https://www.lpoj.cn/7.png"
              class="image"
            >

            <div style="matgin:10px">
              <h2>
                遗忘之都
                <el-button type="primary" style="margin-left:20px;" @click="click(7)">进入章节</el-button>
              </h2>全球的精英通过筛选，都会来这里历练，你还等什么？
            </div>
          </el-card>
        </el-col>
        <el-col :span="6">
          <el-card :body-style="{ padding: '0px' }" shadow="hover">
            <img
              src="https://www.lpoj.cn/8.png"
              class="image"
            >
            <div style="matgin:10px">
              <h2>
                威风之城
                <el-button type="primary" style="margin-left:20px;" @click="click(8)">进入章节</el-button>
              </h2>Becoming world finalist...
            </div>
          </el-card>
        </el-col>
      </el-row>
    </center>
  </el-card>
</template>

<script>
export default {
  name: "trainning",
  data() {
    return {
      centerDialogVisible: false
    };
  },
  created() {},
  methods: {
    click: function(id) {
      this.$router.push({
        name: "trainningdetail",
        params: { trainningid: id }
      });
    }
  }
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.image {
  width: 100%;
  height: 280px;
  display: block;
}
</style>
