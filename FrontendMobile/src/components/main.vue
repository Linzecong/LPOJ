<template>
  <mu-container>
        <welcomemessage></welcomemessage>
        <br>
        <mu-button color="primary" to="/wiki" full-width>Go to Wiki</mu-button>
        <br>
        <br>
        <contestmini></contestmini>
        <br>
        <acrank></acrank>
        <br>
        <topuser></topuser>
  </mu-container>
</template>

<script>
import welcomemessage from "@/components/utils/welcomemessage";
import contestmini from "@/components/utils/contestmini";
import acrank from "@/components/utils/acrank";
import topuser from "@/components/utils/topuser";
export default {
  components: {
    welcomemessage,
    contestmini,
    acrank,
    topuser
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

</style>
