<template>
  <statue ref="statue"></statue>
</template>

<script>
import statue from "@/components/mainpage/statue";
export default {
  name: "contestsubmit",
  data() {
    return {
      
    };
  },
  components: {
    statue
  },
  created() {},
  methods: {
    creattimer(){
      console.log(this.$refs)
      this.$refs.statue.creattimer();
    }
  }
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
h1 {
  position: relative;
}
</style>
