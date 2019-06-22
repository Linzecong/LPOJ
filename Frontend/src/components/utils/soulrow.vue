<template>
  <el-row :gutter="10">
    <el-col :span="7">
      <el-card style="height:150px;">
        <div slot="header">
          <b style="color:#409EFF">Get into Valley of Trials</b>
        </div>
        <b>
          <el-button style="width:100%;" @click="trainningClick" type="primary">Start trial</el-button>
        </b>
      </el-card>
    </el-col>
    <el-col :span="7">
      <el-card style="height:150px;">
        <div slot="header">
          <b style="color:#409EFF">Fast search algorithm</b>
        </div>
        <b>
          <el-button style="width:100%;" icon="el-icon-search" @click="searchtitle">Search algorithm</el-button>
        </b>
      </el-card>
    </el-col>
    <el-col :span="10">
      <el-card style="height:150px;" :body-style="{ padding: '0px' }">
        <!-- <b style="font-size:14.5px">Sequential Construction of Persistent Line Segment Tree by DFS on Fail Tree of AC Automata</b>
        <br>
        <br>
        <b style="font-size:14.5px;">SG Functions on DAG Built by Next Pointer of Suffix Automata</b>-->

        <el-carousel height="150px" direction="vertical" arrow="never">
          <el-carousel-item v-for="item in tables" :key="item">
              <div style="margin:20px;" v-html="item.msg"></div>
          </el-carousel-item>
        </el-carousel>
      </el-card>
    </el-col>
  </el-row>
</template>

<script>
export default {
  name: "soulrow",
  data() {
    return {
      tables: []
    };
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
  },
  created() {
    this.$axios.get("/banner/").then(response => {
      this.tables = response.data;
    });
  }
};
</script>

<style  scoped>

.el-carousel__item:nth-child(2n) {
  background-color: #ffffff;
}

.el-carousel__item:nth-child(2n + 1) {
  background-color: #ffffff;
}
</style>