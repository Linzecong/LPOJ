<template>
  <mu-container>
    <mu-card>
      <mu-dialog :title="dialogdata.title" scrollable :open.sync="dialogVisible">
        <center>
          <p>{{'关卡' + dialogdata.group+'-'+dialogdata.num+', 共 '+dialogdata.totnum+' 道题' }}</p>
          </center>
          <b>任务说明：</b>
          {{dialogdata.des}}
          <br /><br />
      <mu-divider></mu-divider>
          <p>你可以先阅读下面教程：</p>
          <p v-for="pro in dialogdata.tiplist" :key="pro">
            <a :href="'/wikidetail/'+pro+'/'" target="_blank" :class="'wa'">
              <i :class="'el-icon-success'"></i>
              {{' 教程 - '+pro}}
            </a>
          </p>
        
        <br />
        <mu-divider></mu-divider>
        
          <p>要完成这个任务，你需要完成下面这几道题：</p>
          
          <h3>
            <p v-for="pro in dialogdata.prolist" :key="pro">
              <a
                :href="'/problemdetail?problemID='+pro"
                target="_blank"
                :class="dialogdata[pro]==true?'ac':'wa'"
              >
                <i :class="dialogdata[pro]==true?'el-icon-success':'el-icon-question'"></i>
                {{' LPOJ - '+pro}}
              </a>
            </p>
          </h3>
        
      </mu-dialog>

      <mu-card-title :title="title" :sub-title="des"></mu-card-title>

      <mu-divider></mu-divider>
      <mu-card-text>
        <mu-linear-progress mode="determinate" :value="per" :size="15" color="green"></mu-linear-progress>
        <center color="grey">{{donepro + ' / '+totalpro +' 达成'}}</center>
      </mu-card-text>

      <mu-card-text :key="i" v-for="(item,i) in totalpro" raised>
        <mu-card>
          <mu-card-title :title="trainningdata[i].title" :sub-title="trainningdata[i].des"></mu-card-title>

          <mu-card-text>
            <mu-linear-progress mode="determinate" :value="trainper[i]" :size="10"></mu-linear-progress>
            <center
              color="grey"
            >{{'关卡' + trainningdata[i].group+'-'+trainningdata[i].num+', 共 '+trainningdata[i].totnum+' 道题' }}</center>
          </mu-card-text>

          <mu-card-text>
            <mu-button
              :color="trainper[i]==100?'success':'primary'"
              full-width
              @click="goclick(i)"
            >{{trainper[i]==100?'你已完成':'进入关卡'}}</mu-button>
          </mu-card-text>
        </mu-card>
      </mu-card-text>
    </mu-card>
  </mu-container>
</template>

<script>
export default {
  name: "trainningdeatild",
  data() {
    return {
      title: "新手村",
      des: "这里是新手村！在这里你可以学习到基本的编程支持，赶快上路吧！",
      donepro: 0,
      totalpro: 0,
      per: 0,
      group: this.$route.params.trainningid,

      rownum: 0,

      trainningdata: [],
      trainper: [1, 2, 3, 4, 5, 6, 7, 8, 9, 0, 9, 8, 7, 6],
      dialogdata: {},
      dialogVisible: false
    };
  },
  mounted() {
    if (parseInt(this.$route.params.trainningid) == 1) {
      this.title = "新手村落";
      this.des = "这里是新手村！在这里你可以学习到基本的编程支持，赶快上路吧！";
    }
    if (parseInt(this.$route.params.trainningid) == 2) {
      this.title = "蓝桥林地";
      this.des = "蓝桥林地聚集了许许多多的小怪物！快去消灭它们吧！";
    }
    if (parseInt(this.$route.params.trainningid) == 3) {
      this.title = "天梯孤岛";
      this.des = "孤岛中有很多的小恶魔，快去征服他们吧！";
    }
    if (parseInt(this.$route.params.trainningid) == 4) {
      this.title = "省历练场";
      this.des = "省历练场汇聚了许多精英，快来打败他们，参加国选吧！";
    }
    if (parseInt(this.$route.params.trainningid) == 5) {
      this.title = "国选营地";
      this.des = "这里是国家选拔精英的地方，快快脱颖而出，一举成名吧！";
    }
    if (parseInt(this.$route.params.trainningid) == 6) {
      this.title = "国斗兽场";
      this.des = "在这里成为全国瞩目的编程小战士吧！打败他们，获取至高的荣耀";
    }
    if (parseInt(this.$route.params.trainningid) == 7) {
      this.title = "遗忘之都";
      this.des = "全球的精英通过筛选，都会来这里历练，你还等什么？";
    }
    if (parseInt(this.$route.params.trainningid) == 8) {
      this.title = "威风之城";
      this.des = "Becoming world finalist...";
    }

    this.$axios
      .get("/trainning/?group=" + this.$route.params.trainningid)
      .then(response => {
        this.totalpro = response.data.length;
        var acpro = this.$store.state.acpro;
        if (acpro == undefined) acpro = "";
        for (let i = 0; i < this.totalpro; i++) {
          var proli = response.data[i].problem.split("|");
          if (proli[0] == "") proli = [];
          response.data[i]["acnum"] = 0;
          response.data[i]["totnum"] = proli.length;
          response.data[i]["prolist"] = proli;
          response.data[i]["tiplist"] = response.data[i].tips.split("|");
          if (response.data[i]["tiplist"][0] == "")
            response.data[i]["tiplist"] = [];
          for (let j = 0; j < proli.length; j++) {
            response.data[i][proli[j]] = false;
            if (acpro.indexOf(proli[j]) != -1) {
              response.data[i]["acnum"]++;
              response.data[i][proli[j]] = true;
            }
          }
          if (response.data[i]["totnum"] == 0) this.trainper[i] = 0;
          else
            this.trainper[i] = parseInt(
              ((response.data[i]["acnum"] * 1.0) / response.data[i]["totnum"]) *
                1.0 *
                100
            );
          if (
            response.data[i]["totnum"] == response.data[i]["acnum"] &&
            response.data[i]["totnum"] != 0
          )
            this.donepro++;
        }

        this.rownum =
          parseInt(this.totalpro / 4) + (this.totalpro % 4 == 0 ? 0 : 1);
        this.trainningdata = response.data;

        this.per = parseInt(((this.donepro * 1.0) / this.totalpro) * 100);
      })
      .catch(error => {
        this.$toast.error(
          "服务器错误！" + JSON.stringify(error.response.data)
        );
        return;
      });
  },
  methods: {
    goclick(id) {
      this.dialogdata = this.trainningdata[id];
      this.dialogVisible = true;
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
.box-card {
  height: auto;
}

.ac {
  text-decoration: none;
  color: greenyellow;
}

.wa {
  text-decoration: none;
  color: gray;
}
</style>
