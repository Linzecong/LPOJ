<template>
  <div>
    <h3>基于艾洛积分系统（Elo Rating System）修改</h3>
            <h4>1、所有队伍初始得分为1500</h4>
            <h4>2、每场比赛后计算一个排名得分S （ S=（比赛得分线性归一化后）*比赛队伍数 ）（线性归一化函数: x = (x-min)/(max-min)）</h4>
            <h4>3、每场比赛后计算一个期望得分E （ E=sum(1/(1+10^((Rb-Ra)/400)))</h4>
            <h4>其中Ra代表你当前积分，Rb代表每一队伍的得分</h4>
            <h4>4、为了鼓励思考，计算一个系数K，K=（本次比赛得分/平均分）</h4>
            <h4>5、为了鼓励新人，计算一个系数P，P=（开始比赛前的积分排名/总人数）</h4>
            <h4>6、计算积分的变化 D = 20*(K+P+S-E)</h4>
            <el-table
              :data="RatingData"
              border
              style="width: 70%"
              size="mini"
              :row-style="rankcolor"
            >
              <el-table-column prop="name" label="Name"></el-table-column>
              <el-table-column prop="rating" label="Score"></el-table-column>
              <el-table-column prop="color" label="Color"></el-table-column>
            </el-table>

            <h3>每场比赛排名怎么算?</h3>
            <h3>LPOJ个人赛：</h3>
            <h4>每道题目有一个积分，每分钟衰减(0.7/i)%，i为题号 1~26,比赛一般为120分钟。每道题分数按顺序为1000 1500 1600 2000 2000 2000往后都为2000</h4>
            <h4>每一次失败提交-20分，一血加分为 题目积分/10</h4>
            <br>
            <br>
            <h2>每场比赛结果都会保存，所以如果积分系统崩了的话，可以用其他方式计算，保证公平性</h2>
  </div>
</template>

<script>
export default {
  name: "ratingrule",
  data() {
    return {RatingData: [
        { name: "Legendary Grandmaster", rating: "3000+", color: "红色" },
        {
          name: "International Grandmaster",
          rating: "2600 ~ 2999",
          color: "褐色"
        },
        { name: "Grandmaster", rating: "2200 ~ 2599", color: "橙色" },
        { name: "International master", rating: "2050 ~ 2199", color: "紫色" },
        { name: "Master", rating: "1900 ~ 2049", color: "蓝色" },
        { name: "Candidate master", rating: "1700 ~ 1899", color: "青色" },
        { name: "Expert", rating: "1500 ~ 1699", color: "绿色" },
        { name: "Specialist", rating: "1350 ~ 1499", color: "草绿色" },
        { name: "Pupil", rating: "1200 ~ 1349", color: "灰色" },
        { name: "Newbie", rating: "0 ~ 1199", color: "黑色" }
      ]};
  },
  methods:{
      rankcolor({ row, rowIndex }) {
      if (rowIndex == 0) return "color:red;font-weight: bold;";
      if (rowIndex == 1) return "color:#BB5E00;font-weight: bold;";
      if (rowIndex == 2) return "color:#E6A23C;font-weight: bold;";
      if (rowIndex == 3) return "color:#930093;font-weight: bold;";
      if (rowIndex == 4) return "color:#0000AA;font-weight: bold;";
      if (rowIndex == 5) return "color:#007799;font-weight: bold;";
      if (rowIndex == 6) return "color:#227700;font-weight: bold;";
      if (rowIndex == 7) return "color:#67C23A;font-weight: bold;";
      if (rowIndex == 8) return "color:#909399;font-weight: bold;";
      return "color:#303133;font-weight: bold;";
    },
  }
};
</script>

<style  scoped>
</style>