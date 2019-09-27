<template>
  <mu-container>
    <mu-card>
      <mu-card-header title="欢迎来到试炼谷" sub-title="请选择你要挑战的关卡">
  </mu-card-header>

      <mu-card-media>
        <img src="https://www.lpoj.cn/1.png" class="image" />
      </mu-card-media>
      <mu-card-title title="新手村落" sub-title="这里是新手村！在这里你可以学习到基本的编程支持，赶快上路吧！"></mu-card-title>

      <mu-card-actions>
        <mu-button color="primary" full-width @click="click(1)">进入关卡</mu-button>
      </mu-card-actions>
    </mu-card>
    <br>

    <mu-card>
      <mu-card-media>
        <img src="https://www.lpoj.cn/2.png" class="image" />
      </mu-card-media>
      <mu-card-title title="蓝桥林地" sub-title="蓝桥林地聚集了许许多多的小怪物！快去消灭它们吧！"></mu-card-title>

      <mu-card-actions>
        <mu-button color="primary" full-width @click="click(2)">进入关卡</mu-button>
      </mu-card-actions>
    </mu-card>
    <br>

    <mu-card>
      <mu-card-media>
        <img src="https://www.lpoj.cn/3.png" class="image" />
      </mu-card-media>
      <mu-card-title title="天梯孤岛" sub-title="孤岛中有很多的小恶魔，快去征服他们吧！"></mu-card-title>

      <mu-card-actions>
        <mu-button color="primary" full-width @click="click(3)">进入关卡</mu-button>
      </mu-card-actions>
    </mu-card>
    <br>

    <mu-card>
      <mu-card-media>
        <img src="https://www.lpoj.cn/4.png" class="image" />
      </mu-card-media>
      <mu-card-title title="省历练场" sub-title="省历练场汇聚了许多精英，快来打败他们，参加国选吧！"></mu-card-title>

      <mu-card-actions>
        <mu-button color="primary" full-width @click="click(4)">进入关卡</mu-button>
      </mu-card-actions>
    </mu-card>
    <br>

    <mu-card>
      <mu-card-media>
        <img src="https://www.lpoj.cn/5.png" class="image" />
      </mu-card-media>
      <mu-card-title title="国选营地" sub-title="这里是国家选拔精英的地方，快快脱颖而出，一举成名吧！"></mu-card-title>

      <mu-card-actions>
        <mu-button color="primary" full-width @click="click(5)">进入关卡</mu-button>
      </mu-card-actions>
    </mu-card>
    <br>

    <mu-card>
      <mu-card-media>
        <img src="https://www.lpoj.cn/6.png" class="image" />
      </mu-card-media>
      <mu-card-title title="国斗兽场" sub-title="在这里成为全国瞩目的编程小战士吧！打败他们，获取至高的荣耀"></mu-card-title>

      <mu-card-actions>
        <mu-button color="primary" full-width @click="click(6)">进入关卡</mu-button>
      </mu-card-actions>
    </mu-card>
    <br>

    <mu-card>
      <mu-card-media>
        <img src="https://www.lpoj.cn/7.png" class="image" />
      </mu-card-media>
      <mu-card-title title="遗忘之都" sub-title="全球的精英通过筛选，都会来这里历练，你还等什么？"></mu-card-title>

      <mu-card-actions>
        <mu-button color="primary" full-width @click="click(7)">进入关卡</mu-button>
      </mu-card-actions>
    </mu-card>
    <br>

    <mu-card>
      <mu-card-media>
        <img src="https://www.lpoj.cn/8.png" class="image" />
      </mu-card-media>
      <mu-card-title title="威风之城" sub-title="Becoming world finalist..."></mu-card-title>

      <mu-card-actions>
        <mu-button color="primary" full-width @click="click(8)">进入关卡</mu-button>
      </mu-card-actions>
    </mu-card>
    <br>
  </mu-container>
</template>

<script>
export default {
  name: "trainning",
  data() {
    return {
      centerDialogVisible: false
    };
  },
  created() {},
  methods: {
    click: function(id) {
      this.$router.push({
        name: "trainningdetail",
        params: { trainningid: id }
      });
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
</style>
