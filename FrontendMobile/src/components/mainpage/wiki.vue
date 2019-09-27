<template>
<mu-container>
  <mu-card>
     <mu-card-text>
    <center>
      <h1>欢迎来到某大型在线游戏攻略网站LPOJ Wiki</h1>
      <h2>在这里你可以找到算法竞赛的学习教程，代码模板，和算法试炼</h2>
      <h2>现在让我们开始吧！</h2>
    </center>
     </mu-card-text>
     <mu-card-text>
    <mu-expansion-panel :expand="true">
          <div slot="header">
            <center><b>算法教程</b></center>
          </div>
          <div style=" margin-bottom: 18px;">在这里你可以找到最全的算法攻略</div>
          <div style=" margin-bottom: 18px;">在这里你可以编写自己的攻略</div>
          <div style=" margin-bottom: 18px;">在这里你可以查看别人编写的攻略</div>
          <div style=" margin-bottom: 18px;">
            <mu-button @click="glClick" color="primary" full-width>查看攻略</mu-button>
          </div>
    </mu-expansion-panel>
    <br>

      <mu-expansion-panel :expand="true">
        
          <div slot="header">
            <b>LPOJ试炼谷</b>
          </div>
          <div style=" margin-bottom: 18px;">在这里你可以找到ACM的入门方法</div>
          <div style=" margin-bottom: 18px;">在这里你可以得到完整的历练</div>
          <div style=" margin-bottom: 18px;">在这里你可以看到自己变成大神的轨迹</div>
          <div style=" margin-bottom: 18px;">
            <mu-button @click="trainningClick" color="primary" full-width>开始试炼</mu-button>
          </div>
        </mu-expansion-panel>
  <br>
     </mu-card-text>
  </mu-card>
</mu-container>
</template>

<script>
export default {
  name: "wiki",
  data() {
    return {};
  },
  methods: {
    glClick(){
      this.$router.push({
          name: "newalgorithm"
      });
    },
    jiubanClick(){
      this.$router.push({
          name: "algorithm"
      });
    },
    mbClick(){
      this.$router.push({
          name: "mbcode"
      });
    },
    trainningClick(){
      this.$router.push({
          name: "trainning"
      });
    }
  },
  created() {}
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>
