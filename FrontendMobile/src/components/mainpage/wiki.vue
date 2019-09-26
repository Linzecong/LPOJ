<template>
  <el-card shadow="always" id="card">
    <center>
      <h1>欢迎来到某大型在线游戏攻略网站LPOJ Wiki</h1>
      <h2>在这里你可以找到算法竞赛的学习教程，代码模板，和算法试炼</h2>
      <h2>现在让我们开始吧！</h2>
    </center>
    <el-row :gutter="10">
      <el-col :span="8">
        <el-card>
          <div slot="header">
            <b>算法教程</b>
          </div>
          <div style=" margin-bottom: 18px;">在这里你可以找到最全的算法攻略</div>
          <div style=" margin-bottom: 18px;">在这里你可以编写自己的攻略</div>
          <div style=" margin-bottom: 18px;">在这里你可以查看别人编写的攻略</div>
          <div style=" margin-bottom: 18px;">
            <el-button @click="glClick" type="primary">查看攻略</el-button>
            <el-button @click="jiubanClick" type="text">进入旧版</el-button>
          </div>
        </el-card>
      </el-col>
      <el-col :span="8">
        <el-card>
          <div slot="header">
            <b>模板大全</b>
          </div>
          <div style=" margin-bottom: 18px;">在这里你可以找到最全的算法模板</div>
          <div style=" margin-bottom: 18px;">在这里你可以保存自己的模板</div>
          <div style=" margin-bottom: 18px;">在这里你可以查看别人编写的模板</div>
          <div style=" margin-bottom: 18px;">
            <el-button @click="mbClick" type="primary">查看模板</el-button>
          </div>
        </el-card>
      </el-col>
      <el-col :span="8">
        <el-card>
          <div slot="header">
            <b>LPOJ试炼谷</b>
          </div>
          <div style=" margin-bottom: 18px;">在这里你可以找到ACM的入门方法</div>
          <div style=" margin-bottom: 18px;">在这里你可以得到完整的历练</div>
          <div style=" margin-bottom: 18px;">在这里你可以看到自己变成大神的轨迹</div>
          <div style=" margin-bottom: 18px;">
            <el-button @click="trainningClick" type="primary">开始试炼</el-button>
          </div>
        </el-card>
      </el-col>
    </el-row>
  </el-card>
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
