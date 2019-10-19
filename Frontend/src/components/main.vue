<template>
  <el-row :gutter="12">
    <el-col :span="6">
      <el-row :gutter="10">
        <welcomemessage></welcomemessage>
      </el-row>
      <el-row :gutter="10">
        <acrank></acrank>
      </el-row>
      <el-row :gutter="10">
        <topuser></topuser>
      </el-row>
      <el-row :gutter="10">
        <ojmessage></ojmessage>
      </el-row>
    </el-col>
    <el-col :span="18">
      <soulrow></soulrow>
      <!-- <el-row>
        <blogmini></blogmini>
      </el-row>-->
      <el-row>
        <el-tabs type="border-card">
          <el-tab-pane :label="label.des" >
            <description></description>
          </el-tab-pane>
          <el-tab-pane :label="label.rank" :lazy="true">
            <rankchart></rankchart>
          </el-tab-pane>
          <el-tab-pane :label="label.rule" :lazy="true">
            <ratingrule></ratingrule>
          </el-tab-pane>
        </el-tabs>
      </el-row>
      <!-- <el-row>
        <el-calendar>
          <template slot="dateCell" slot-scope="{date, data}">
            <center>
            <b>{{data.day}}</b>
            </center>
            <span :class="getclass1(data.day)">下午: {{anpai1[data.day]?anpai1[data.day]:'自习或讲题'}}</span><br>
            <span :class="getclass2(data.day)">晚上: {{anpai2[data.day]?anpai2[data.day]:'自习或讲题'}}</span>
          </template>
        </el-calendar>
      </el-row> -->
      <el-row>
        <contestmini></contestmini>
      </el-row>
    </el-col>
  </el-row>
</template>

<script>
import rankchart from "@/components/chart/rankchart";
import ojmessage from "@/components/utils/ojmessage";
import welcomemessage from "@/components/utils/welcomemessage";
import topuser from "@/components/utils/topuser";
import soulrow from "@/components/utils/soulrow";
import ratingrule from "@/components/utils/ratingrule";
import contestmini from "@/components/utils/contestmini";
import description from "@/components/utils/description";
import acrank from "@/components/utils/acrank";
export default {
  components: {
    rankchart,
    ojmessage,
    welcomemessage,
    topuser,
    soulrow,
    ratingrule,
    contestmini,
    acrank,
    description
  },
  name: "main",
  data() {
    return {
      label: {
        rank: "Rank",
        team: "Team",
        rule: "Rule",
        des: "Description"
      },

      // anpai1:{
      //   "2019-07-18":"牛客第一场",
      //   "2019-07-20":"牛客第二场",
      //   "2019-07-25":"牛客第三场",
      //   "2019-07-28":"牛客第四场",
      //   "2019-08-01":"牛客第五场",
      //   "2019-08-03":"牛客第六场",
      //   "2019-08-08":"牛客第七场",
      //   "2019-08-10":"牛客第八场",
      //   "2019-08-15":"牛客第九场",
      //   "2019-08-17":"牛客第十场",

      //   "2019-07-22":"多校第一场",
      //   "2019-07-24":"多校第二场",
      //   "2019-07-29":"多校第三场",
      //   "2019-07-31":"多校第四场",
      //   "2019-08-05":"多校第五场",
      //   "2019-08-07":"多校第六场",
      //   "2019-08-12":"多校第七场",
      //   "2019-08-14":"多校第八场",
      //   "2019-08-19":"多校第九场",
      //   "2019-08-21":"多校第十场",
      //   "2019-07-23":"可选择打计蒜客",
      //   "2019-07-30":"可选择打计蒜客",
      //   "2019-08-06":"可选择打计蒜客",
      //   "2019-08-13":"可选择打计蒜客",
      //   "2019-08-20":"可选择打计蒜客",
      //   "2019-08-24":"可选择打计蒜客",
      //   "2019-08-27":"可选择打计蒜客",
      //   "2019-08-31":"计蒜客（银川）",
      //   "2019-09-01":"计蒜客（南京）",
      //   "2019-09-07":"计蒜客（徐州）",
      //   "2019-09-08":"计蒜客（南昌）",
      //   "2019-09-14":"计蒜客（沈阳）",
      //   "2019-09-15":"计蒜客（上海）",
      // },
      // anpai2:{
      //   "2019-07-05":"打CF",
      //   "2019-07-06":"打牛客",
      //   "2019-08-17":"打百度之星初赛一",
      //   "2019-08-18":"打百度之星初赛二",
      // }
    };
  },
  mounted() {
    
  },
  methods: {
    // getclass1(data){
    //   data = this.anpai1[data]
    //   if(data==undefined)
    //     return ''
    //   if(data.indexOf("牛客")>=0){
    //     return "niuke";
    //   }
    //   if(data.indexOf("计蒜客")>=0){
    //     return "jisuanke";
    //   }
    //   if(data.indexOf("多校")>=0||data.indexOf("百度")>=0){
    //     return "duoxiao";
    //   }
    //   return ''
    // },
    // getclass2(data){
    //   data = this.anpai2[data]
    //   if(data==undefined)
    //     return ''
    //   if(data.indexOf("牛客")>=0){
    //     return "niuke";
    //   }
    //   if(data.indexOf("计蒜客")>=0){
    //     return "jisuanke";
    //   }
    //   if(data.indexOf("多校")>=0||data.indexOf("百度")>=0){
    //     return "duoxiao";
    //   }
    //   return ''
    // }
  }
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.el-row {
  margin-bottom: 12px;
}
/* .niuke {
  background: rgb(238, 169, 137)
}
.duoxiao {
  background: rgb(95, 170, 241)
}
.jisuanke {
  background: rgb(51, 167, 49)
} */
</style>
