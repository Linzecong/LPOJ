<template>
  <mu-container>
        <welcomemessage></welcomemessage>
        <br>
        <contestmini></contestmini>
        <br>
        <acrank></acrank>
  </mu-container>
</template>

<script>
import rankchart from "@/components/chart/rankchart";
import ojmessage from "@/components/utils/ojmessage";
import welcomemessage from "@/components/utils/welcomemessage";
import topuser from "@/components/utils/topuser";
import soulrow from "@/components/utils/soulrow";
import ratingrule from "@/components/utils/ratingrule";
import contestmini from "@/components/utils/contestmini";
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
    acrank
  },
  name: "main",
  data() {
    return {
      label: {
        rank: "Individual",
        team: "Team",
        rule: "Rule"
      },

    };
  },
  mounted() {
    
  },
  methods: {
  
  }
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.el-row {
  margin-bottom: 12px;
}
</style>
