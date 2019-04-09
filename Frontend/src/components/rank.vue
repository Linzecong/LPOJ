<template>
    <el-card>
      <el-row :gutter="15">
        <el-carousel :interval="2000" type="card">
          <el-carousel-item v-for="(item,index) in carouselData" :key="index">
            <center>
            <h1>{{ index+1 }}</h1>
            <h2> {{ item.username }}</h2>
            <h2> {{ item.des }}</h2>
            <h5>Score: {{ item.score }}</h5>
            <h5>Rating: {{ item.rating }}</h5>
            <h5>AC: {{ item.ac }}</h5>
            <h5>Submittion: {{ item.submit }}</h5>
            </center>
          </el-carousel-item>
        </el-carousel>
      </el-row>
      <el-row>
        <el-table
      :data="tableData"
      @cell-click="userclick"
      :default-sort="{prop: 'rating', order: 'descending'}"
      size="small"
      :row-style="ratingcolor"
    >
      <el-table-column prop="username" label="User"></el-table-column>
      <el-table-column prop="des" label="Mood"></el-table-column>
      <el-table-column prop="score" label="Score"></el-table-column>
      <el-table-column prop="rating" label="Rating"></el-table-column>
      <el-table-column prop="ac" label="AC"></el-table-column>
      <el-table-column prop="submit" label="Submit"></el-table-column>
      <el-table-column prop="rate" label="AC/Submit"></el-table-column>
    </el-table>
    <el-pagination
      @size-change="handleSizeChange"
      @current-change="handleCurrentChange"
      :current-page="currentpage"
      :page-sizes="[10, 20, 30, 50]"
      :page-size="pagesize"
      layout="total, sizes, prev, pager, next, jumper"
      :total="totaluser"
    ></el-pagination>
      </el-row>
    </el-card>
</template>

<script>
export default {
  name: 'rank',
  data () {
    return {
      currentpage: 1,
      pagesize: 20,
      totaluser: 10,
      tableData: [],
      carouselData:[]
    }
  },
  methods: {
    ratingcolor({row, rowIndex}){
      if (row.rating >= 3000) return "color:red;font-weight: bold;";
      if (row.rating >= 2600) return "color:#BB5E00;font-weight: bold;";
      if (row.rating >= 2200) return "color:#E6A23C;font-weight: bold;";
      if (row.rating >= 2050) return "color:#930093;font-weight: bold;";
      if (row.rating >= 1900) return "color:#0000AA;font-weight: bold;";
      if (row.rating >= 1700) return "color:#007799;font-weight: bold;";
      if (row.rating >= 1500) return "color:#227700;font-weight: bold;";
      if (row.rating >= 1350) return "color:#67C23A;font-weight: bold;";
      if (row.rating >= 1200) return "color:#909399;font-weight: bold;";
      return "color:#303133;font-weight: bold;";
    },
    userclick(row, column, cell, event){
      this.$router.push({
          name: "user",
          query: { username: row.username }
        });
    },
    
    getData(limit,offset){
      this.$axios
      .get(
        "/userdata/?limit="+limit+"&offset="+offset
      )
      .then(response => {
        //console.log(response.data.results[0])
        for(var i=0;i<response.data.results.length;i++){
          //console.log(response.data.results[i]["ac"])
          response.data.results[i]["rate"]= ((response.data.results[i]["ac"]/ response.data.results[i]["submit"])*100).toFixed(2)+"%";
          
          if(response.data.results[i]["submit"]==0){
            response.data.results[i]["rate"]="00.00%"
          }
          if(i<3)
          this.carouselData.push(response.data.results[i])
        }
        this.tableData = response.data.results;
        this.totaluser = response.data.count;
        
      })
      .catch(error => {
        this.$message.error("服务器错误！" + "(" + error + ")");
      });
    },
    handleSizeChange(val){
      this.pagesize = val;
      this.getData(this.pagesize,(this.currentpage - 1) * this.pagesize)
    },
    handleCurrentChange(val){
      this.currentpage = val;
      this.getData(this.pagesize,(this.currentpage - 1) * this.pagesize)
    },
  },
  created(){
    this.getData(20,0);
  }

  
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.el-carousel__item:nth-child(2n) {
    background-color: #baf1af;
  }
  
  .el-carousel__item:nth-child(2n+1) {
    background-color: #bcffa7;
  }

</style>
