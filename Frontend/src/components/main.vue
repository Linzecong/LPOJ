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
      <el-row :gutter="10">
        <cfrate></cfrate>
      </el-row>
    </el-col>
    <el-col :span="18">
      <soulrow></soulrow>
    
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
import cfrate from "@/components/utils/cfrate";
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
    description,
    cfrate
  },
  name: "homepage",
  data() {
    return {
      label: {
        rank: "Rank",
        team: "Team",
        rule: "Rule",
        des: "Description"
      },

    };
  },
  mounted() {

  },
  methods: {
 
  }
};
</script>

<style scoped>
.el-row {
  margin-bottom: 12px;
}

</style>
