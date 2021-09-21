<template>
  <mu-container>
    <mu-card>
      <mu-container>
        <mu-select label="Choose Algorithm..." v-model="editpage" @change="searchtitle" full-width>
          <algorithmselect></algorithmselect>
        </mu-select>
      </mu-container>
    </mu-card>
    <br />
    <mu-card>
    <iframe :src="algurl" frameborder="0" width="100%" height="880px"></iframe>
    <mu-divider></mu-divider>
    <center>Thanks for the mirror provided by Netease</center>
    </mu-card>
  </mu-container>
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
      algurl: "https://oi-wiki.org/"
    };
  },
  created() {
    var cururl = this.$route.params.wikiid;
    this.algurl =
      "https://oi-wiki.org/" + cururl.replace("_", "/") + "/";
    //console.log(this.algurl)
  },

  methods: {
    searchtitle() {
      this.$router.push({
        name: "wikidetail",
        params: { wikiid: this.editpage }
      });
      var cururl = this.$route.params.wikiid;
      this.algurl =
        "https://oi-wiki.org/" + cururl.replace("_", "/") + "/";
      //console.log(this.algurl)
    }
  }
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>
