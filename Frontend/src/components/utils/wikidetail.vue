<template>
  <el-row>
    <el-select
      @keyup.native.enter="searchtitle"
      v-model="editpage"
      placeholder="请输入要查看的算法"
      @change="searchtitle"
      filterable
      style="width:100%;"
    >
      <algorithmselect></algorithmselect>
    </el-select>
    <mavon-editor
      style="margin-top:15px;"
      :boxShadow="false"
      :value="value"
      :subfield="prop.subfield"
      :defaultOpen="prop.defaultOpen"
      :toolbarsFlag="prop.toolbarsFlag"
      :editable="prop.editable"
      :scrollStyle="prop.scrollStyle"
      :autofocus="false"
      v-loading="loading"
    ></mavon-editor>
    <el-row style="margin-left:15px">
      <br>
      <p>选择其他版本</p>
      <el-table :data="tableData" @cell-click="userclick" style="float:left;width:100%;">
        <el-table-column type="index"></el-table-column>
        <el-table-column prop="username" label="User" :width="200"></el-table-column>
        <el-table-column prop="time" label="Last Edit Time"></el-table-column>
      </el-table>
    </el-row>
  </el-row>
</template>

<script>
import moment from "moment";
import { mavonEditor } from "mavon-editor";
import "mavon-editor/dist/css/index.css";
import algorithmselect from "@/components/utils/algorithmselect";
export default {
  name: "wikidetail",
  components: {
    mavonEditor,
    algorithmselect
  },
  computed: {
    prop() {
      let data = {
        subfield: false, // 单双栏模式
        defaultOpen: "preview", //edit： 默认展示编辑区域 ， preview： 默认展示预览区域
        editable: false,
        toolbarsFlag: false,
        scrollStyle: true
      };
      return data;
    }
  },
  data() {
    return {
      value: "",
      searchtext: "",
      editpage: "",
      tableData: [],
      loading:false,
      username:"",
      curtype:"",
    };
  },
  created() {
    this.getdata("std", this.$route.params.wikiid);
  },
  methods: {
    getdata(username, type) {
      if(type=="")
        return
      if(this.username==username&&this.curtype==type)
        return
      this.username=username
      this.curtype=type
      this.loading = true;
      this.$axios
        .get("/wikicount/?type=" + type)
        .then(response2 => {
          console.log(response2)
          for (let i = 0; i < response2.data.length; i++)
            response2.data[i].time = moment(response2.data[i].time).format(
              "YYYY-MM-DD HH:mm:ss"
            );
          this.tableData = response2.data;
        })
        .catch(error => {
          this.$message.error(
            "服务器错误！" + "(" + JSON.stringify(error.response.data) + ")"
          );
        });

      this.$axios
        .get("/wiki/?username=" + username + "&type=" + type)
        .then(response => {
          this.value =
            response.data.length > 0
              ? response.data[0].value
              : "# 暂无标准数据，请切换版本你想要的版本！";
          this.loading = false;
        })
        .catch(error => {
          this.$message.error(
            "服务器错误！" + "(" + JSON.stringify(error.response.data) + ")"
          );
        });
    },
    searchtitle() {
      this.$router.push({
        name: "wikidetail",
        params: { wikiid: this.editpage }
      });
      this.getdata("std", this.$route.params.wikiid);
    },
    userclick(row, column, cell, event) {
      this.getdata(row.username, this.$route.params.wikiid);
    }
  }
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>
