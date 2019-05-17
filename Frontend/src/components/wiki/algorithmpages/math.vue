<template>
  <div>
    <el-row>
      <el-col :span="4">
        <el-menu default-active="math_index" @select="handleSelect">
          <el-menu-item index="math_index">数学简介</el-menu-item>
          <el-menu-item index="math_base">进制</el-menu-item>
          <el-menu-item index="math_bit">位运算</el-menu-item>
          <el-menu-item index="math_bignum">高精度</el-menu-item>
          <el-menu-item index="math_quickpow">快速幂</el-menu-item>
          <el-submenu index="1">
            <template slot="title">素数相关</template>
            <el-menu-item-group>
              <el-menu-item index="math_prime">素数</el-menu-item>
              <el-menu-item index="math_gcd">最大公约数</el-menu-item>
              <el-menu-item index="math_euler">欧拉函数</el-menu-item>
              <el-menu-item index="math_sieve">筛法</el-menu-item>
              <el-menu-item index="math_fermat">费马小定理</el-menu-item>
            </el-menu-item-group>
          </el-submenu>
          <el-submenu index="2">
            <template slot="title">同余方程</template>
            <el-menu-item-group>
              <el-menu-item index="math_bezouts">裴蜀定理</el-menu-item>
              <el-menu-item index="math_inverse">乘法逆元</el-menu-item>
              <el-menu-item index="math_linearequation">线性同余方程</el-menu-item>
              <el-menu-item index="math_crt">中国剩余定理</el-menu-item>
              <el-menu-item index="math_bsgs">BSGS</el-menu-item>
              <el-menu-item index="math_primitiveroot">原根</el-menu-item>
            </el-menu-item-group>
          </el-submenu>
          <el-submenu index="3">
            <template slot="title">线性代数</template>
            <el-menu-item-group>
              <el-menu-item index="math_matrix">矩阵</el-menu-item>
              <el-menu-item index="math_gauss">高斯消元</el-menu-item>
              <el-menu-item index="math_basis">线性基</el-menu-item>
            </el-menu-item-group>
          </el-submenu>
          <el-menu-item index="math_complex">复数</el-menu-item>
          <el-menu-item index="math_dictionary">分段打表</el-menu-item>
          <el-submenu index="4">
            <template slot="title">数论函数相关</template>
            <el-menu-item-group>
              <el-menu-item index="math_mobius">莫比乌斯反演</el-menu-item>
              <el-menu-item index="math_dusieves">杜教筛</el-menu-item>
            </el-menu-item-group>
          </el-submenu>
          <el-submenu index="5">
            <template slot="title">多项式相关</template>
            <el-menu-item-group>
              <el-menu-item index="math_polyintro">多项式部分简介</el-menu-item>
              <el-menu-item index="math_lagrangepoly">拉格朗日插值</el-menu-item>
              <el-menu-item index="math_fft">快速傅里叶变换</el-menu-item>
              <el-menu-item index="math_ntt">快速数论变换</el-menu-item>
              <el-menu-item index="math_fwt">快速沃尔什变换</el-menu-item>
              <el-menu-item index="math_sqrt">多项式开方</el-menu-item>
              <el-menu-item index="math_inv">多项式求逆</el-menu-item>
              <el-menu-item index="math_divmod">多项式除法|取模</el-menu-item>
              <el-menu-item index="math_lnexp">多项式对数函数|指数函数</el-menu-item>
              <el-menu-item index="math_newton">多项式牛顿迭代</el-menu-item>
              <el-menu-item index="math_multipointevalinterpolation">多项式多点求值|快速插值</el-menu-item>
              <el-menu-item index="math_trifunc">多项式三角函数</el-menu-item>
              <el-menu-item index="math_invtrifunc">多项式反三角函数</el-menu-item>
            </el-menu-item-group>
          </el-submenu>

          <el-submenu index="6">
            <template slot="title">组合数学</template>
            <el-menu-item-group>
              <el-menu-item index="math_combination">排列组合</el-menu-item>
              <el-menu-item index="math_catalan">卡特兰数</el-menu-item>
              <el-menu-item index="math_stirling">斯特林数</el-menu-item>
              <el-menu-item index="math_cantor">康托展开</el-menu-item>
              <el-menu-item index="math_inclusionexclusionprinciple">容斥原理</el-menu-item>
              <el-menu-item index="math_drawerprinciple">抽屉原理</el-menu-item>
            </el-menu-item-group>
          </el-submenu>

          <el-menu-item index="math_expectation">概率和期望</el-menu-item>
          <el-menu-item index="math_permutationgroup">置换群</el-menu-item>
          <el-menu-item index="math_integral">数值积分</el-menu-item>
          <el-menu-item index="math_linearprogramming">线性规划</el-menu-item>
          <el-menu-item index="math_gametheory">博弈论</el-menu-item>
          <el-submenu index="8">
            <template slot="title">其他（额外添加）</template>
            <el-menu-item-group>
              <el-menu-item
                :key="index"
                v-for="(item,index) in menulist"
                :index="item.type"
              >{{item.title}}</el-menu-item>
            </el-menu-item-group>
          </el-submenu>
        </el-menu>
      </el-col>
      <el-col :span="20">
        <mavon-editor
          :boxShadow="false"
          :value="mathvalue"
          :subfield="prop.subfield"
          :defaultOpen="prop.defaultOpen"
          :toolbarsFlag="prop.toolbarsFlag"
          :editable="prop.editable"
          :scrollStyle="prop.scrollStyle"
          :autofocus="false"
          v-loading="loading"
        ></mavon-editor>
      </el-col>
    </el-row>
    <el-row style="margin-left:15px">
      <br>
      <p>选择其他版本</p>
      <el-table :data="tableData" @cell-click="userclick" style="float:left;width:40%;">
        <el-table-column type="index"></el-table-column>
        <el-table-column prop="username" label="User" :width="200"></el-table-column>
        <el-table-column prop="time" label="Last Edit Time"></el-table-column>
      </el-table>
    </el-row>
  </div>
</template>

<script>
import moment from "moment";
import { mavonEditor } from "mavon-editor";
import "mavon-editor/dist/css/index.css";
export default {
  name: "math",
  components: {
    mavonEditor
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
      mathvalue: "",
      tableData: [],
      curTypeValue: "",
      curUserValue: "",
      loading:false,
      menulist: []
    };
  },
  created() {
    this.getdata("std", "math_index");
    this.$axios
      .get("/wiki/?group=math&std=1")
      .then(response => {
        this.menulist = response.data;
      })
      .catch(error => {
        this.$message.error(
          "服务器错误！" + "(" + JSON.stringify(error.response.data) + ")"
        );
      });
  },
  watch: {
    mathvalue: function() {
      console.log('data changed');
      this.$nextTick().then(()=>{
        this.reRender();
      });
    }
  },
  methods: {
    reRender() {
      if(window.MathJax) {
        console.log('rendering mathjax');
        MathJax.Hub.Config({
            tex2jax: {
                inlineMath: [ ['$','$'], ["\\(","\\)"] ],
                displayMath: [ ['$$','$$'], ["\\[","\\]"] ]
            }
        });
        window.MathJax.Hub.Queue(["Typeset", window.MathJax.Hub], () => console.log('done'));
      }
    },
    handleSelect(key, keyPath) {
      this.getdata("std", key);
    },
    getdata(username, type) {
      if (this.curUserValue != username || this.curTypeValue != type) {
        this.mathvalue = "";
        this.curUserValue = username;
        this.curTypeValue = type;
      } else return;
      this.loading=true
      this.$axios
        .get("/wikicount/?type=" + type)
        .then(response => {
          for (let i = 0; i < response.data.length; i++)
            response.data[i].time = moment(response.data[i].time).format(
              "YYYY-MM-DD HH:mm:ss"
            );
          this.tableData = response.data;
        })
        .catch(error => {
          this.$message.error(
            "服务器错误！" + "(" + JSON.stringify(error.response.data) + ")"
          );
        });

      this.$axios
        .get("/wiki/?username=" + username + "&type=" + type)
        .then(response => {
          this.mathvalue =
            response.data.length > 0 ? response.data[0].value : "# 暂无标准数据，请切换版本你想要的版本！";
            this.loading=false
        })
        .catch(error => {
          this.$message.error(
            "服务器错误！" + "(" + JSON.stringify(error.response.data) + ")"
          );
        });
    },
    userclick(row, column, cell, event) {
      this.getdata(row.username, this.curTypeValue);
    }
  }
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>
