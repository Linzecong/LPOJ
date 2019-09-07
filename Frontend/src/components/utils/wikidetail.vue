<template>
  <el-row>
    <el-select
      @keyup.native.enter="searchtitle"
      v-model="editpage"
      placeholder="Please enter the algorithm to view..."
      @change="searchtitle"
      filterable
      style="width:100%;"
    >
      <algorithmselect></algorithmselect>
    </el-select>

    <el-card style="margin-top:20px;">
      <iframe :src="algurl" frameborder="0" scrolling="0" width="100%" height="880px"></iframe>
      <el-divider>Thanks for the mirror provided by Netease</el-divider>
    </el-card>
    
  </el-row>
</template>

<script>
import moment from "moment";

import algorithmselect from "@/components/utils/algorithmselect";
export default {
  name: "wikidetail",
  components: {
    algorithmselect
  },
  data() {
    return {
      editpage: "",
      algurl:"https://oi-wiki.io.netease.com/"
      
    };
  },
  created(){
    var cururl = this.$route.params.wikiid
    this.algurl = "https://oi-wiki.io.netease.com/" + cururl.replace("_","/") +"/"
    //console.log(this.algurl)
  },

  methods: {
  
    searchtitle() {
      this.$router.push({
        name: "wikidetail",
        params: { wikiid: this.editpage }
      });
      var cururl = this.$route.params.wikiid
      this.algurl = "https://oi-wiki.io.netease.com/" + cururl.replace("_","/") +"/"
      //console.log(this.algurl)
    },
  }
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>
