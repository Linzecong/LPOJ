<template>
  <el-card shadow="always" id="card">
    <center>
      <h1 :style="color">{{username}}</h1>
      <h4 :style="color">{{ des }}</h4>
      <h4 :style="color">Rating: {{ rating }}</h4>
    </center>

    <ratingchart></ratingchart>

    <center>
      <h1 :style="color">{{ name }}</h1>
    </center>

    <el-row>
      <el-col :span="8">
        <center>
          <h2 :style="color">Submittion</h2>
          <h3 :style="color">{{ submittion }}</h3>
        </center>
      </el-col>
      <el-col :span="8">
        <center>
          <h2 :style="color">AC</h2>
          <h3 :style="color">{{ ac }}</h3>
        </center>
      </el-col>
      <el-col :span="8">
        <center>
          <h2 :style="color">Score</h2>
          <h3 :style="color">{{ score }}</h3>
        </center>
      </el-col>
    </el-row>

    <center>
      <h2 :style="color">AC Problems</h2>
      <br>
    </center>
    <el-button
      id="tag"
      v-for="(name,index) in acpro"
      :key="index"
      size="small"
      @click="problemclick(name)"
      type="success"
      style="width:70px;"
    >{{ name }}</el-button>
  </el-card>
</template>

<script>
import ratingchart from "@/components/chart/ratingchart";
export default {
  name: "user",
  components: {
    ratingchart
  },
  data() {
    return {
      username: "",
      name: "",
      des: "",
      ac: "",
      submittion: "",
      score: "",
      rating: "",
      acpro: [],
      color: ""
    };
  },
  methods: {
    ratingcolor({ row, rowIndex }) {
      if (row.rating >= 3000) return "color:red;";
      if (row.rating >= 2600) return "color:#BB5E00;";
      if (row.rating >= 2200) return "color:#E6A23C;";
      if (row.rating >= 2050) return "color:#930093;";
      if (row.rating >= 1900) return "color:#0000AA;";
      if (row.rating >= 1700) return "color:#007799;";
      if (row.rating >= 1500) return "color:#227700;";
      if (row.rating >= 1350) return "color:#67C23A;";
      if (row.rating >= 1200) return "color:#909399;";
      return "color:#303133;font-weight: bold;";
    },

    problemclick(name) {
      this.$router.push({
        name: "problemdetail",
        query: { problemID: name }
      });
    }
  },
  created() {
    this.username = this.$route.query.username;
    if (this.username) {
      this.$axios.get("/user/?username=" + this.username).then(response => {
        this.name = response.data[0].name;
      });

      this.$axios.get("/userdata/?username=" + this.username).then(response => {
        this.ac = response.data[0].ac;
        this.submittion = response.data[0].submit;
        this.des = response.data[0].des;
        this.score = response.data[0].score;
        this.rating = response.data[0].rating;

        this.acpro = response.data[0].acpro.split("|");
        this.acpro.shift();

        var style = "";
        if (this.rating >= 3000) style = "color:red;font-weight: bold;";
        else if (this.rating >= 2600)
          style = "color:#BB5E00;font-weight: bold;";
        else if (this.rating >= 2200)
          style = "color:#E6A23C;font-weight: bold;";
        else if (this.rating >= 2050)
          style = "color:#930093;font-weight: bold;";
        else if (this.rating >= 1900)
          style = "color:#0000AA;font-weight: bold;";
        else if (this.rating >= 1700)
          style = "color:#007799;font-weight: bold;";
        else if (this.rating >= 1500)
          style = "color:#227700;font-weight: bold;";
        else if (this.rating >= 1350)
          style = "color:#67C23A;font-weight: bold;";
        else if (this.rating >= 1200)
          style = "color:#909399;font-weight: bold;";
        else style = "color:#303133;font-weight: bold;";
        this.color = style;
      });
    }
  }
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
#card {
  margin: 200px;
  padding: 200px;
}
#tag {
  text-align: center;
  font-weight: bold;
  margin-left: 7px;
  margin-bottom: 7px;
}
</style>
