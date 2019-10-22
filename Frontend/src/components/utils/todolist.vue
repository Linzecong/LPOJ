<template>
  <div>
    <el-row type="flex" justify="space-around">
      <el-col :span="5">
        <draggable
          :list="notelist"
          group="people"
          @change="notechange"
          draggable=".item"
          :sort="false"
          @start="ismoving = true"
          @end="ismoving = false"
        >
          <mu-expansion-panel
            v-for="e in notelist"
            :key="e.title"
            style="margin-top: 5px;"
            class="item"
          >
            <h3 slot="header" style="word-break: break-all;white-space: normal;">{{e.title}}</h3>
            <pre>{{e.detail}}</pre>
            <el-button slot="action" type="danger" @click="delnode(e)">删除</el-button>
            <el-button
              slot="action"
              type="success"
              @click="curid=e.id;form=e;expandnote=true;expandwarning=false;expandnormal=false;notetitle='修改便签';warningtitle='待补题';normaltitle='日常事项'"
            >编辑</el-button>
          </mu-expansion-panel>

          <mu-expansion-panel
            slot="header"
            style="background-color:#c8e6c9"
            @change="clearform();expandwarning=false;expandnormal=false;"
            :expand.sync="expandnote"
          >
            <h3 slot="header">{{notetitle}}</h3>
            <el-form ref="form" :model="form" label-width="80px">
              <el-form-item label="标题">
                <el-input v-model="form.title"></el-input>
              </el-form-item>
              <el-form-item label="标签内容">
                <el-input type="textarea" autosize v-model="form.detail"></el-input>
              </el-form-item>
            </el-form>
            <el-button
              slot="action"
              style="background-color:#c8e6c9;border:0px;"
              @click="expandnote=false;notetitle='便签'"
            >取消</el-button>
            <el-button
              slot="action"
              type="success"
              @click="addnote(1,1)"
              v-show="notetitle=='便签'"
            >添加</el-button>
            <el-button
              slot="action"
              type="success"
              @click="editnote(1,1)"
              v-show="notetitle!='便签'"
            >修改</el-button>
          </mu-expansion-panel>
        </draggable>
      </el-col>
      <el-col :span="6">
        <draggable
          :list="normallisttodo"
          group="people"
          @change="normallisttodochange"
          draggable=".item"
          :sort="false"
          @start="ismoving = true"
          @end="ismoving = false"
        >
          <mu-expansion-panel
            v-for="e in normallisttodo"
            :key="e.detail"
            style="margin-top: 5px;"
            class="item"
          >
            <h3 slot="header" style="word-break: break-all;white-space: normal;">{{e.title}}</h3>
            <pre>{{e.detail}}</pre>
            <br />
            <b>
              截止时间：
              <el-date-picker type="datetime" :value="e.deadtime" readonly />
            </b>
            <el-button slot="action" type="danger" @click="delnode(e)">删除</el-button>
            <el-button
              slot="action"
              type="warning"
              @click="curid=e.id;form=e;expandnormal=true;expandnote=false;expandwarning=false;normaltitle='修改日常事项';notetitle='便签';warningtitle='待补题'"
            >编辑</el-button>
          </mu-expansion-panel>

          <mu-expansion-panel
            slot="header"
            style="background-color:#ffecb3"
            @change="clearform();expandwarning=false;expandnote=false;"
            :expand.sync="expandnormal"
          >
            <h3 slot="header">{{normaltitle}}</h3>
            <el-form ref="form" :model="form" label-width="80px">
              <el-form-item label="标题">
                <el-input v-model="form.title"></el-input>
              </el-form-item>
              <el-form-item label="截止时间">
                <el-date-picker
                  v-model="form.deadtime"
                  type="datetime"
                  placeholder="选择日期时间"
                  align="right"
                  :picker-options="pickerOptions"
                ></el-date-picker>
              </el-form-item>
              <el-form-item label="内容">
                <el-input type="textarea" autosize v-model="form.detail"></el-input>
              </el-form-item>
            </el-form>
            <el-button
              slot="action"
              style="background-color:#ffecb3;border:0px;"
              @click="expandnormal=false;normaltitle='日常事项'"
            >取消</el-button>
            <el-button
              slot="action"
              type="warning"
              @click="addnote(1,2);expandnormal=false"
              v-show="normaltitle=='日常事项'"
            >添加</el-button>
            <el-button
              slot="action"
              type="warning"
              @click="editnote(1,2)"
              v-show="normaltitle!='日常事项'"
            >修改</el-button>
          </mu-expansion-panel>
        </draggable>
      </el-col>
      <el-col :span="8">
        <draggable
          :list="warninglisttodo"
          group="people"
          @change="warninglisttodochange"
          draggable=".item"
          :sort="false"
          @start="ismoving = true"
          @end="ismoving = false"
        >
          <mu-expansion-panel
            v-for="e in warninglisttodo"
            :key="e.title"
            style="margin-top: 5px;"
            class="item"
          >
            <h3 slot="header" style="word-break: break-all;white-space: normal;">{{e.title}}</h3>
            <pre>{{e.detail}}</pre>
            <br />
            <b style="color:red">
              截止时间：
              <el-date-picker type="datetime" :value="e.deadtime" readonly />
            </b>
            <el-button slot="action" type="danger" @click="delnode(e)">删除</el-button>
            <el-button
              slot="action"
              type="danger"
              @click="pageScroll();curid=e.id;form=e;expandwarning=true;expandnote=false;expandnormal=false;warningtitle='修改待补题';notetitle='便签';normaltitle='日常事项'"
            >编辑</el-button>
          </mu-expansion-panel>
          <mu-expansion-panel
            slot="header"
            style="background-color:#ffcdd2"
            @change="clearform();expandnote=false;expandnormal=false;"
            :expand.sync="expandwarning"
          >
            <h3 slot="header">{{warningtitle}}</h3>
            <el-form ref="form" :model="form" label-width="80px">
              <el-form-item label="标题">
                <el-input v-model="form.title"></el-input>
              </el-form-item>
              <el-form-item label="截止时间">
                <el-date-picker
                  v-model="form.deadtime"
                  type="datetime"
                  placeholder="选择日期时间"
                  align="right"
                  :picker-options="pickerOptions"
                ></el-date-picker>
              </el-form-item>
              <el-form-item label="内容">
                <el-input type="textarea" autosize v-model="form.detail"></el-input>
              </el-form-item>
            </el-form>
            <el-button
              slot="action"
              style="background-color:#ffcdd2;border:0px;"
              @click="expandwarning=false;warningtitle='待补题'"
            >取消</el-button>
            <el-button
              slot="action"
              type="danger"
              @click="addnote(1,3);expandwarning=false"
              v-show="warningtitle=='待补题'"
            >添加</el-button>
            <el-button
              slot="action"
              type="danger"
              @click="editnote(1,3)"
              v-show="warningtitle!='待补题'"
            >修改</el-button>
          </mu-expansion-panel>
        </draggable>
      </el-col>

      <el-col :span="4">
        <draggable
          :list="normallistdone"
          group="people"
          @change="normallistdonechange"
          draggable=".item"
          :sort="false"
          @start="ismoving = true"
          @end="ismoving = false"
        >
          <mu-expansion-panel
            v-for="e in normallistdone"
            :key="e.detail"
            style="margin-top: 5px;"
            class="item"
          >
            <h3 slot="header" style="word-break: break-all;white-space: normal;">{{e.title}}</h3>
            <pre>{{e.detail}}</pre>
            <br />
            <b>
              创建时间：
              <br />
              <el-date-picker type="datetime" :value="e.createtime" readonly />
              <br />
              <br />截止时间：
              <br />
              <el-date-picker type="datetime" :value="e.deadtime" readonly />
            </b>
          </mu-expansion-panel>
          <mu-expansion-panel slot="header" style="background-color:#d7ccc8">
            <h3 slot="header">已补题（提示：可拖动）</h3>
          </mu-expansion-panel>
        </draggable>
      </el-col>
      <el-backtop></el-backtop>
    </el-row>
  </div>
</template>

<script>
import draggable from "vuedraggable";

export default {
  name: "todolist",
  components: {
    draggable
  },
  data() {
    return {
      pickerOptions: {
        shortcuts: [
          {
            text: "今天",
            onClick(picker) {
              picker.$emit("pick", new Date());
            }
          },
          {
            text: "明天",
            onClick(picker) {
              const date = new Date();
              date.setTime(date.getTime() + 3600 * 1000 * 24);
              picker.$emit("pick", date);
            }
          },
          {
            text: "后天",
            onClick(picker) {
              const date = new Date();
              date.setTime(date.getTime() + 3600 * 1000 * 24 * 2);
              picker.$emit("pick", date);
            }
          },
          {
            text: "三天后",
            onClick(picker) {
              const date = new Date();
              date.setTime(date.getTime() + 3600 * 1000 * 24 * 3);
              picker.$emit("pick", date);
            }
          },
          {
            text: "一周后",
            onClick(picker) {
              const date = new Date();
              date.setTime(date.getTime() + 3600 * 1000 * 24 * 7);
              picker.$emit("pick", date);
            }
          },
          {
            text: "两周后",
            onClick(picker) {
              const date = new Date();
              date.setTime(date.getTime() + 3600 * 1000 * 24 * 14);
              picker.$emit("pick", date);
            }
          },
          {
            text: "四周后",
            onClick(picker) {
              const date = new Date();
              date.setTime(date.getTime() + 3600 * 1000 * 24 * 28);
              picker.$emit("pick", date);
            }
          }
        ]
      },
      curid: 0,
      notetitle: "便签",
      warningtitle: "待补题",
      normaltitle: "日常事项",
      activeNames: [],
      activeIndex: "1",
      loginshow: 0,
      name: sessionStorage.username,
      notelist: [],
      normallisttodo: [],
      normallistdone: [],
      warninglisttodo: [],
      dellist: [1],
      ismoving: false,
      form: {
        user: sessionStorage.username,
        title: "",
        detail: "",
        status: 1,
        createtime: new Date(),
        deadtime: new Date(new Date().getTime() + 24 * 60 * 60 * 1000),
        tag: 1
      },
      expandnote: true,
      expandwarning: false,
      expandnormal: false,
      scrolldelay: null
    };
  },
  mounted() {
    if (
      sessionStorage.getItem("username") != "" &&
      sessionStorage.getItem("username") != undefined
    ) {
      this.loginshow = 1;
      this.name = sessionStorage.getItem("username");
    }

    this.refresh();
  },
  methods: {
    //往上滚
    pageScroll() {
      window.scrollBy(0, -70);
      this.scrolldelay = setTimeout(this.pageScroll, 10);
      var sTop = document.documentElement.scrollTop + document.body.scrollTop;
      if (sTop == 0) clearTimeout(this.scrolldelay);
    },
    clearform() {
      this.form = {
        user: sessionStorage.username,
        title: "",
        detail: "",
        createtime: new Date(),
        deadtime: new Date(new Date().getTime() + 24 * 60 * 60 * 1000),
        status: 1,
        tag: 1
      };
    },
    refresh() {
      var notelist = [];
      var normallisttodo = [];
      var normallistdone = [];
      var warninglisttodo = [];
      var warninglistdone = [];
      this.$axios
        .get("/item/")
        .then(response => {
          for (let i = 0; i < response.data.length; i++) {
            if (response.data[i].status == 0) {
              normallistdone.push(response.data[i]);
              continue;
            }
            if (response.data[i].tag == 1) notelist.push(response.data[i]);
            if (response.data[i].tag == 2 && response.data[i].status == 1)
              normallisttodo.push(response.data[i]);
            if (response.data[i].tag == 3 && response.data[i].status == 1)
              warninglisttodo.push(response.data[i]);
          }
          this.notelist = notelist;
          this.normallisttodo = normallisttodo;
          this.normallistdone = normallistdone;
          this.warninglisttodo = warninglisttodo;
          var sortfunc = function(a, b) {
            return a.createtime < b.createtime ? 1 : -1;
          };
          var sortfunc2 = function(a, b) {
            return a.deadtime > b.deadtime ? 1 : -1;
          };

          this.notelist.sort(sortfunc);
          this.normallisttodo.sort(sortfunc);
          this.normallistdone.sort(sortfunc);
          this.warninglisttodo.sort(sortfunc2);
        })
        .catch(error => {
          this.$message.error(
            "服务器错误！" + "(" + JSON.stringify(error.response.data) + ")"
          );
        });
    },

    notechange: function(evt) {
      var msg = evt["added"];
      if (msg != undefined) {
        msg.element.status = 1;
        msg.element.tag = 1;
        console.log(msg.element);
        this.putnode(msg.element);
      }
    },

    normallisttodochange: function(evt) {
      var msg = evt["added"];
      if (msg != undefined) {
        msg.element.status = 1;
        msg.element.tag = 2;
        this.putnode(msg.element);
      }
    },
    normallistdonechange: function(evt) {
      var msg = evt["added"];
      if (msg != undefined) {
        msg.element.status = 0;
        this.putnode(msg.element);
      }
    },
    warninglisttodochange: function(evt) {
      var msg = evt["added"];
      if (msg != undefined) {
        msg.element.status = 1;
        msg.element.tag = 3;
        this.putnode(msg.element);
      }
    },

    delnode(item) {
      this.$axios
        .delete("/putitem/" + item.id + "/")
        .then(response => {
          this.$message({
            message: "删除成功！" + item.id,
            type: "success",
            duration: 2000
          });
          this.refresh();
        })
        .catch(error => {
          this.$message.error(
            "服务器错误！" + "(" + JSON.stringify(error.response.data) + ")"
          );
        });
    },

    addnote(status, tag) {
      this.form.status = status;
      this.form.tag = tag;
      let east8time = new Date().getTime() + 8 * 60 * 60 * 1000;
      if (tag == 1) {
        this.form.deadtime = new Date(east8time);
      } else {
        this.form.deadtime = new Date(
          this.form.deadtime.getTime() + 8 * 60 * 60 * 1000
        );
      }

      this.form.createtime = new Date(east8time);

      this.$axios
        .post("/putitem/", this.form)
        .then(response => {
          this.$message({
            message: "添加成功  " + this.form.title + " ",
            type: "success",
            duration: 500
          });
          this.refresh();
          this.expandnote = false;
          this.expandwarning = false;
          this.expandwarning = false;
        })
        .catch(error => {
          this.$message.error(
            "服务器错误！" + "(" + JSON.stringify(error.response.data) + ")"
          );
        });
    },
    putnode(item) {
      if (item.tag != 1) {
        item.deadtime = new Date(
          new Date(item.deadtime).getTime() + 8 * 60 * 60 * 1000
        );
      }
      this.$axios
        .put("/putitem/" + item.id + "/", item)
        .then(response => {
          this.refresh();
          this.$message({
            message: "切换成功",
            type: "success",
            duration: 500
          });
        })
        .catch(error => {
          this.$message.error(
            "服务器错误！" + "(" + JSON.stringify(error.response.data) + ")"
          );
        });
    },

    editnote(status, tag) {
      this.form.status = status;
      this.form.tag = tag;
      if (tag == 1) {
        let east8time = new Date().getTime() + 8 * 60 * 60 * 1000;
        this.form.deadtime = new Date(east8time);
      }
      if (tag != 1) {
        this.form.deadtime = new Date(
          new Date(this.form.deadtime).getTime() + 8 * 60 * 60 * 1000
        );
      }

      this.$axios
        .put("/putitem/" + this.curid + "/", this.form)
        .then(response => {
          this.$message({
            message: "修改成功  " + this.form.title + " ",
            type: "success",
            duration: 500
          });
          this.refresh();
          this.expandnote = false;
          this.expandwarning = false;
          this.expandnormal = false;
          this.notetitle = "便签";
          this.warningtitle = "待补题";
          this.normaltitle = "日常事项";
        })
        .catch(error => {
          this.$message.error(
            "服务器错误！" + "(" + JSON.stringify(error.response.data) + ")"
          );
        });
    },

    handleChange() {
      console.log("changed");
    },
    getComponentData() {
      return {
        on: {
          change: this.handleChange,
          input: this.handleChange
        },
        attrs: {
          wrap: true
        },
        props: {
          value: this.activeNames
        }
      };
    }
  }
};
</script>

<style scope>
#button {
  float: right;
  margin: 10px;
}
.mu-button {
  display: inline-block;
  overflow: hidden;
  position: relative;
  -webkit-transition-duration: 0.3s;
  -o-transition-duration: 0.3s;
  transition-duration: 0.3s;
  -webkit-transition-timing-function: cubic-bezier(0.23, 1, 0.32, 1);
  -o-transition-timing-function: cubic-bezier(0.23, 1, 0.32, 1);
  transition-timing-function: cubic-bezier(0.23, 1, 0.32, 1);
  text-decoration: none;
  text-align: center;
  border: none;
  -webkit-appearance: none;
  -moz-appearance: none;
  appearance: none;
  outline: none;
  text-transform: uppercase;
  margin: 0;
  padding: 0;
  cursor: pointer;
  -webkit-box-flex: 0;
  -webkit-flex-shrink: 0;
  -ms-flex: 0 0 auto;
  -ms-flex-negative: 0;
  flex-shrink: 0;
}
.mu-button .mu-icon-left {
  margin-right: 8px;
}
.mu-button .mu-icon-right {
  margin-left: 8px;
}
.mu-button.hover:before {
  content: "";
  position: absolute;
  left: 0;
  right: 0;
  top: 0;
  bottom: 0;
  background-color: currentColor;
  opacity: 0.12;
}
.mu-button-wrapper {
  display: -webkit-box;
  display: -webkit-flex;
  display: -ms-flexbox;
  display: flex;
  -webkit-box-pack: center;
  -webkit-justify-content: center;
  -ms-flex-pack: center;
  justify-content: center;
  -webkit-box-align: center;
  -webkit-align-items: center;
  -ms-flex-align: center;
  align-items: center;
  width: 100%;
  height: 100%;
}
.mu-raised-button {
  font-size: 14px;
  min-width: 88px;
  height: 36px;
  line-height: 36px;
  border-radius: 2px;
  background-color: #fff;
  color: rgba(0, 0, 0, 0.87);
  -webkit-box-shadow: 0 3px 1px -2px rgba(0, 0, 0, 0.2),
    0 2px 2px 0 rgba(0, 0, 0, 0.14), 0 1px 5px 0 rgba(0, 0, 0, 0.12);
  box-shadow: 0 3px 1px -2px rgba(0, 0, 0, 0.2), 0 2px 2px 0 rgba(0, 0, 0, 0.14),
    0 1px 5px 0 rgba(0, 0, 0, 0.12);
}
.mu-raised-button.mu-inverse .mu-circle-ripple {
  opacity: 0.3;
}
.mu-raised-button.disabled {
  color: rgba(0, 0, 0, 0.3);
  cursor: not-allowed;
  background-color: #e6e6e6;
}
.mu-raised-button.disabled,
.mu-raised-button.disabled.hover,
.mu-raised-button.disabled:active,
.mu-raised-button.disabled:hover {
  -webkit-box-shadow: none;
  box-shadow: none;
}
.mu-raised-button.focus {
  -webkit-box-shadow: 0 3px 5px -1px rgba(0, 0, 0, 0.2),
    0 6px 10px 0 rgba(0, 0, 0, 0.14), 0 1px 18px 0 rgba(0, 0, 0, 0.12);
  box-shadow: 0 3px 5px -1px rgba(0, 0, 0, 0.2),
    0 6px 10px 0 rgba(0, 0, 0, 0.14), 0 1px 18px 0 rgba(0, 0, 0, 0.12);
}
.mu-raised-button:active {
  -webkit-box-shadow: 0 5px 5px -3px rgba(0, 0, 0, 0.2),
    0 8px 10px 1px rgba(0, 0, 0, 0.14), 0 3px 14px 2px rgba(0, 0, 0, 0.12);
  box-shadow: 0 5px 5px -3px rgba(0, 0, 0, 0.2),
    0 8px 10px 1px rgba(0, 0, 0, 0.14), 0 3px 14px 2px rgba(0, 0, 0, 0.12);
}
.mu-raised-button .mu-button-wrapper {
  padding: 0 16px;
}
.mu-raised-button.mu-button-round {
  border-radius: 36px;
}
.mu-raised-button.mu-button-full-width {
  width: 100%;
}
.mu-raised-button.mu-button-small {
  font-size: 13px;
  height: 28px;
}
.mu-raised-button.mu-button-small.mu-button-round {
  border-radius: 28px;
}
.mu-raised-button.mu-button-small .mu-button-wrapper {
  padding: 0 8px;
}
.mu-raised-button.mu-button-small .mu-icon {
  font-size: 20px;
}
.mu-raised-button.mu-button-large {
  font-size: 15px;
  height: 44px;
}
.mu-raised-button.mu-button-large.mu-button-round {
  border-radius: 44px;
}
.mu-raised-button.mu-button-large .mu-button-wrapper {
  padding: 0 32px;
}
.mu-raised-button.mu-button-large .mu-icon {
  font-size: 28px;
}
.mu-flat-button {
  border-radius: 2px;
  height: 36px;
  line-height: 36px;
  min-width: 88px;
  font-size: 14px;
  color: rgba(0, 0, 0, 0.87);
  background: transparent;
}
.mu-flat-button.disabled {
  color: rgba(0, 0, 0, 0.38);
  cursor: not-allowed;
  background: none;
}
.mu-flat-button .mu-button-wrapper {
  padding: 0 16px;
}
.mu-flat-button.mu-button-small {
  font-size: 13px;
  height: 28px;
}
.mu-flat-button.mu-button-small .mu-button-wrapper {
  padding: 0 8px;
}
.mu-flat-button.mu-button-small .mu-icon {
  font-size: 20px;
}
.mu-flat-button.mu-button-large {
  font-size: 15px;
  height: 44px;
}
.mu-flat-button.mu-button-large .mu-button-wrapper {
  padding: 0 32px;
}
.mu-flat-button.mu-button-large .mu-icon {
  font-size: 28px;
}
.mu-icon-button {
  line-height: 1;
  width: 48px;
  height: 48px;
  border-radius: 50%;
  font-size: 24px;
  padding: 12px;
  border: none;
  -webkit-appearance: none;
  -moz-appearance: none;
  appearance: none;
  background: none;
  color: inherit;
  background-color: transparent;
}
.mu-icon-button.disabled {
  color: rgba(0, 0, 0, 0.38);
  cursor: not-allowed;
}
.mu-icon-button.mu-button-small {
  width: 32px;
  height: 32px;
}
.mu-icon-button.mu-button-small .mu-icon {
  font-size: 20px;
}
.mu-icon-button.mu-button-large {
  width: 56px;
  height: 56px;
}
.mu-icon-button.mu-button-large .mu-icon {
  font-size: 28px;
}
.mu-fab-button {
  line-height: 1;
  width: 56px;
  height: 56px;
  border-radius: 50%;
  border: none;
  -webkit-appearance: none;
  -moz-appearance: none;
  appearance: none;
  background-color: #2196f3;
  color: #fff;
  -webkit-box-shadow: 0 3px 5px -1px rgba(0, 0, 0, 0.2),
    0 6px 10px 0 rgba(0, 0, 0, 0.14), 0 1px 18px 0 rgba(0, 0, 0, 0.12);
  box-shadow: 0 3px 5px -1px rgba(0, 0, 0, 0.2),
    0 6px 10px 0 rgba(0, 0, 0, 0.14), 0 1px 18px 0 rgba(0, 0, 0, 0.12);
}
.mu-fab-button.hover,
.mu-fab-button:active {
  -webkit-box-shadow: 0 7px 8px -4px rgba(0, 0, 0, 0.2),
    0 12px 17px 2px rgba(0, 0, 0, 0.14), 0 5px 22px 4px rgba(0, 0, 0, 0.12);
  box-shadow: 0 7px 8px -4px rgba(0, 0, 0, 0.2),
    0 12px 17px 2px rgba(0, 0, 0, 0.14), 0 5px 22px 4px rgba(0, 0, 0, 0.12);
}
.mu-fab-button.disabled {
  color: rgba(0, 0, 0, 0.3);
  cursor: not-allowed;
  background-color: #e6e6e6;
}
.mu-fab-button.disabled,
.mu-fab-button.disabled.hover,
.mu-fab-button.disabled:active,
.mu-fab-button.disabled:hover {
  -webkit-box-shadow: none;
  box-shadow: none;
}
.mu-fab-button .mu-circle-ripple {
  opacity: 0.3;
}
.mu-fab-button.mu-button-small {
  width: 40px;
  height: 40px;
}
.mu-fab-button.mu-button-small .mu-icon {
  font-size: 18px;
}
.mu-fab-button.mu-button-large {
  width: 72px;
  height: 72px;
}
.mu-fab-button.mu-button-large .mu-icon {
  font-size: 30px;
}
.mu-ripple-wrapper {
  height: 100%;
  width: 100%;
  position: absolute;
  top: 0;
  left: 0;
  overflow: hidden;
}
.mu-circle-ripple {
  position: absolute;
  width: 100%;
  height: 100%;
  left: 0;
  top: 0;
  pointer-events: none;
  -webkit-user-select: none;
  -moz-user-select: none;
  -ms-user-select: none;
  user-select: none;
  border-radius: 50%;
  background-color: currentColor;
  background-clip: padding-box;
  opacity: 0.1;
}
.mu-ripple-enter-active,
.mu-ripple-leave-active {
  -webkit-transition: opacity 2s cubic-bezier(0.23, 1, 0.32, 1),
    -webkit-transform 0.45s cubic-bezier(0.23, 1, 0.32, 1);
  transition: opacity 2s cubic-bezier(0.23, 1, 0.32, 1),
    -webkit-transform 0.45s cubic-bezier(0.23, 1, 0.32, 1);
  -o-transition: opacity 2s cubic-bezier(0.23, 1, 0.32, 1),
    transform 0.45s cubic-bezier(0.23, 1, 0.32, 1);
  transition: opacity 2s cubic-bezier(0.23, 1, 0.32, 1),
    transform 0.45s cubic-bezier(0.23, 1, 0.32, 1);
  transition: opacity 2s cubic-bezier(0.23, 1, 0.32, 1),
    transform 0.45s cubic-bezier(0.23, 1, 0.32, 1),
    -webkit-transform 0.45s cubic-bezier(0.23, 1, 0.32, 1);
}
.mu-ripple-enter {
  -webkit-transform: scale(0);
  transform: scale(0);
}
.mu-ripple-leave-active {
  opacity: 0 !important;
}
.mu-focus-ripple-wrapper {
  height: 100%;
  width: 100%;
  position: absolute;
  top: 0;
  left: 0;
  overflow: hidden;
}
.mu-focus-ripple {
  position: absolute;
  height: 100%;
  width: 100%;
  border-radius: 50%;
  opacity: 0.16;
  background-color: currentColor;
  -webkit-animation: mu-pulsate 0.75s cubic-bezier(0.445, 0.05, 0.55, 0.95);
  animation: mu-pulsate 0.75s cubic-bezier(0.445, 0.05, 0.55, 0.95);
  -webkit-animation-iteration-count: infinite;
  animation-iteration-count: infinite;
  -webkit-animation-direction: alternate;
  animation-direction: alternate;
}
@-webkit-keyframes mu-pulsate {
  0% {
    -webkit-transform: scale(0.72);
    transform: scale(0.72);
  }
  to {
    -webkit-transform: scale(0.85);
    transform: scale(0.85);
  }
}
@keyframes mu-pulsate {
  0% {
    -webkit-transform: scale(0.72);
    transform: scale(0.72);
  }
  to {
    -webkit-transform: scale(0.85);
    transform: scale(0.85);
  }
}
.mu-elevation-0 {
  -webkit-box-shadow: none;
  box-shadow: none;
}
.mu-elevation-1 {
  -webkit-box-shadow: 0 2px 1px -1px rgba(0, 0, 0, 0.2),
    0 1px 1px 0 rgba(0, 0, 0, 0.14), 0 1px 3px 0 rgba(0, 0, 0, 0.12);
  box-shadow: 0 2px 1px -1px rgba(0, 0, 0, 0.2), 0 1px 1px 0 rgba(0, 0, 0, 0.14),
    0 1px 3px 0 rgba(0, 0, 0, 0.12);
}
.mu-elevation-2 {
  -webkit-box-shadow: 0 3px 1px -2px rgba(0, 0, 0, 0.2),
    0 2px 2px 0 rgba(0, 0, 0, 0.14), 0 1px 5px 0 rgba(0, 0, 0, 0.12);
  box-shadow: 0 3px 1px -2px rgba(0, 0, 0, 0.2), 0 2px 2px 0 rgba(0, 0, 0, 0.14),
    0 1px 5px 0 rgba(0, 0, 0, 0.12);
}
.mu-elevation-3 {
  -webkit-box-shadow: 0 3px 3px -2px rgba(0, 0, 0, 0.2),
    0 3px 4px 0 rgba(0, 0, 0, 0.14), 0 1px 8px 0 rgba(0, 0, 0, 0.12);
  box-shadow: 0 3px 3px -2px rgba(0, 0, 0, 0.2), 0 3px 4px 0 rgba(0, 0, 0, 0.14),
    0 1px 8px 0 rgba(0, 0, 0, 0.12);
}
.mu-elevation-4 {
  -webkit-box-shadow: 0 2px 4px -1px rgba(0, 0, 0, 0.2),
    0 4px 5px 0 rgba(0, 0, 0, 0.14), 0 1px 10px 0 rgba(0, 0, 0, 0.12);
  box-shadow: 0 2px 4px -1px rgba(0, 0, 0, 0.2), 0 4px 5px 0 rgba(0, 0, 0, 0.14),
    0 1px 10px 0 rgba(0, 0, 0, 0.12);
}
.mu-elevation-5 {
  -webkit-box-shadow: 0 3px 5px -1px rgba(0, 0, 0, 0.2),
    0 5px 8px 0 rgba(0, 0, 0, 0.14), 0 1px 14px 0 rgba(0, 0, 0, 0.12);
  box-shadow: 0 3px 5px -1px rgba(0, 0, 0, 0.2), 0 5px 8px 0 rgba(0, 0, 0, 0.14),
    0 1px 14px 0 rgba(0, 0, 0, 0.12);
}
.mu-elevation-6 {
  -webkit-box-shadow: 0 3px 5px -1px rgba(0, 0, 0, 0.2),
    0 6px 10px 0 rgba(0, 0, 0, 0.14), 0 1px 18px 0 rgba(0, 0, 0, 0.12);
  box-shadow: 0 3px 5px -1px rgba(0, 0, 0, 0.2),
    0 6px 10px 0 rgba(0, 0, 0, 0.14), 0 1px 18px 0 rgba(0, 0, 0, 0.12);
}
.mu-elevation-7 {
  -webkit-box-shadow: 0 4px 5px -2px rgba(0, 0, 0, 0.2),
    0 7px 10px 1px rgba(0, 0, 0, 0.14), 0 2px 16px 1px rgba(0, 0, 0, 0.12);
  box-shadow: 0 4px 5px -2px rgba(0, 0, 0, 0.2),
    0 7px 10px 1px rgba(0, 0, 0, 0.14), 0 2px 16px 1px rgba(0, 0, 0, 0.12);
}
.mu-elevation-8 {
  -webkit-box-shadow: 0 5px 5px -3px rgba(0, 0, 0, 0.2),
    0 8px 10px 1px rgba(0, 0, 0, 0.14), 0 3px 14px 2px rgba(0, 0, 0, 0.12);
  box-shadow: 0 5px 5px -3px rgba(0, 0, 0, 0.2),
    0 8px 10px 1px rgba(0, 0, 0, 0.14), 0 3px 14px 2px rgba(0, 0, 0, 0.12);
}
.mu-elevation-9 {
  -webkit-box-shadow: 0 5px 6px -3px rgba(0, 0, 0, 0.2),
    0 9px 12px 1px rgba(0, 0, 0, 0.14), 0 3px 16px 2px rgba(0, 0, 0, 0.12);
  box-shadow: 0 5px 6px -3px rgba(0, 0, 0, 0.2),
    0 9px 12px 1px rgba(0, 0, 0, 0.14), 0 3px 16px 2px rgba(0, 0, 0, 0.12);
}
.mu-elevation-10 {
  -webkit-box-shadow: 0 6px 6px -3px rgba(0, 0, 0, 0.2),
    0 10px 14px 1px rgba(0, 0, 0, 0.14), 0 4px 18px 3px rgba(0, 0, 0, 0.12);
  box-shadow: 0 6px 6px -3px rgba(0, 0, 0, 0.2),
    0 10px 14px 1px rgba(0, 0, 0, 0.14), 0 4px 18px 3px rgba(0, 0, 0, 0.12);
}
.mu-elevation-11 {
  -webkit-box-shadow: 0 6px 7px -4px rgba(0, 0, 0, 0.2),
    0 11px 15px 1px rgba(0, 0, 0, 0.14), 0 4px 20px 3px rgba(0, 0, 0, 0.12);
  box-shadow: 0 6px 7px -4px rgba(0, 0, 0, 0.2),
    0 11px 15px 1px rgba(0, 0, 0, 0.14), 0 4px 20px 3px rgba(0, 0, 0, 0.12);
}
.mu-elevation-12 {
  -webkit-box-shadow: 0 7px 8px -4px rgba(0, 0, 0, 0.2),
    0 12px 17px 2px rgba(0, 0, 0, 0.14), 0 5px 22px 4px rgba(0, 0, 0, 0.12);
  box-shadow: 0 7px 8px -4px rgba(0, 0, 0, 0.2),
    0 12px 17px 2px rgba(0, 0, 0, 0.14), 0 5px 22px 4px rgba(0, 0, 0, 0.12);
}
.mu-elevation-13 {
  -webkit-box-shadow: 0 7px 8px -4px rgba(0, 0, 0, 0.2),
    0 13px 19px 2px rgba(0, 0, 0, 0.14), 0 5px 24px 4px rgba(0, 0, 0, 0.12);
  box-shadow: 0 7px 8px -4px rgba(0, 0, 0, 0.2),
    0 13px 19px 2px rgba(0, 0, 0, 0.14), 0 5px 24px 4px rgba(0, 0, 0, 0.12);
}
.mu-elevation-14 {
  -webkit-box-shadow: 0 7px 9px -4px rgba(0, 0, 0, 0.2),
    0 14px 21px 2px rgba(0, 0, 0, 0.14), 0 5px 26px 4px rgba(0, 0, 0, 0.12);
  box-shadow: 0 7px 9px -4px rgba(0, 0, 0, 0.2),
    0 14px 21px 2px rgba(0, 0, 0, 0.14), 0 5px 26px 4px rgba(0, 0, 0, 0.12);
}
.mu-elevation-15 {
  -webkit-box-shadow: 0 8px 9px -5px rgba(0, 0, 0, 0.2),
    0 15px 22px 2px rgba(0, 0, 0, 0.14), 0 6px 28px 5px rgba(0, 0, 0, 0.12);
  box-shadow: 0 8px 9px -5px rgba(0, 0, 0, 0.2),
    0 15px 22px 2px rgba(0, 0, 0, 0.14), 0 6px 28px 5px rgba(0, 0, 0, 0.12);
}
.mu-elevation-16 {
  -webkit-box-shadow: 0 8px 10px -5px rgba(0, 0, 0, 0.2),
    0 16px 24px 2px rgba(0, 0, 0, 0.14), 0 6px 30px 5px rgba(0, 0, 0, 0.12);
  box-shadow: 0 8px 10px -5px rgba(0, 0, 0, 0.2),
    0 16px 24px 2px rgba(0, 0, 0, 0.14), 0 6px 30px 5px rgba(0, 0, 0, 0.12);
}
.mu-elevation-17 {
  -webkit-box-shadow: 0 8px 11px -5px rgba(0, 0, 0, 0.2),
    0 17px 26px 2px rgba(0, 0, 0, 0.14), 0 6px 32px 5px rgba(0, 0, 0, 0.12);
  box-shadow: 0 8px 11px -5px rgba(0, 0, 0, 0.2),
    0 17px 26px 2px rgba(0, 0, 0, 0.14), 0 6px 32px 5px rgba(0, 0, 0, 0.12);
}
.mu-elevation-18 {
  -webkit-box-shadow: 0 9px 11px -5px rgba(0, 0, 0, 0.2),
    0 18px 28px 2px rgba(0, 0, 0, 0.14), 0 7px 34px 6px rgba(0, 0, 0, 0.12);
  box-shadow: 0 9px 11px -5px rgba(0, 0, 0, 0.2),
    0 18px 28px 2px rgba(0, 0, 0, 0.14), 0 7px 34px 6px rgba(0, 0, 0, 0.12);
}
.mu-elevation-19 {
  -webkit-box-shadow: 0 9px 12px -6px rgba(0, 0, 0, 0.2),
    0 19px 29px 2px rgba(0, 0, 0, 0.14), 0 7px 36px 6px rgba(0, 0, 0, 0.12);
  box-shadow: 0 9px 12px -6px rgba(0, 0, 0, 0.2),
    0 19px 29px 2px rgba(0, 0, 0, 0.14), 0 7px 36px 6px rgba(0, 0, 0, 0.12);
}
.mu-elevation-20 {
  -webkit-box-shadow: 0 10px 13px -6px rgba(0, 0, 0, 0.2),
    0 20px 31px 3px rgba(0, 0, 0, 0.14), 0 8px 38px 7px rgba(0, 0, 0, 0.12);
  box-shadow: 0 10px 13px -6px rgba(0, 0, 0, 0.2),
    0 20px 31px 3px rgba(0, 0, 0, 0.14), 0 8px 38px 7px rgba(0, 0, 0, 0.12);
}
.mu-elevation-21 {
  -webkit-box-shadow: 0 10px 13px -6px rgba(0, 0, 0, 0.2),
    0 21px 33px 3px rgba(0, 0, 0, 0.14), 0 8px 40px 7px rgba(0, 0, 0, 0.12);
  box-shadow: 0 10px 13px -6px rgba(0, 0, 0, 0.2),
    0 21px 33px 3px rgba(0, 0, 0, 0.14), 0 8px 40px 7px rgba(0, 0, 0, 0.12);
}
.mu-elevation-22 {
  -webkit-box-shadow: 0 10px 14px -6px rgba(0, 0, 0, 0.2),
    0 22px 35px 3px rgba(0, 0, 0, 0.14), 0 8px 42px 7px rgba(0, 0, 0, 0.12);
  box-shadow: 0 10px 14px -6px rgba(0, 0, 0, 0.2),
    0 22px 35px 3px rgba(0, 0, 0, 0.14), 0 8px 42px 7px rgba(0, 0, 0, 0.12);
}
.mu-elevation-23 {
  -webkit-box-shadow: 0 11px 14px -7px rgba(0, 0, 0, 0.2),
    0 23px 36px 3px rgba(0, 0, 0, 0.14), 0 9px 44px 8px rgba(0, 0, 0, 0.12);
  box-shadow: 0 11px 14px -7px rgba(0, 0, 0, 0.2),
    0 23px 36px 3px rgba(0, 0, 0, 0.14), 0 9px 44px 8px rgba(0, 0, 0, 0.12);
}
.mu-elevation-24 {
  -webkit-box-shadow: 0 11px 15px -7px rgba(0, 0, 0, 0.2),
    0 24px 38px 3px rgba(0, 0, 0, 0.14), 0 9px 46px 8px rgba(0, 0, 0, 0.12);
  box-shadow: 0 11px 15px -7px rgba(0, 0, 0, 0.2),
    0 24px 38px 3px rgba(0, 0, 0, 0.14), 0 9px 46px 8px rgba(0, 0, 0, 0.12);
}
.mu-fade-transition-enter-active,
.mu-fade-transition-leave-active {
  -webkit-transition: opacity 0.45s cubic-bezier(0.23, 1, 0.32, 1);
  -o-transition: opacity 0.45s cubic-bezier(0.23, 1, 0.32, 1);
  transition: opacity 0.45s cubic-bezier(0.23, 1, 0.32, 1);
}
.mu-fade-transition-enter,
.mu-fade-transition-leave-active {
  opacity: 0 !important;
}
.mu-popover-transition-enter-active,
.mu-popover-transition-leave-active {
  -webkit-transition-duration: 0.3s;
  -o-transition-duration: 0.3s;
  transition-duration: 0.3s;
  -webkit-transition-property: opacity, -webkit-transform;
  transition-property: opacity, -webkit-transform;
  -o-transition-property: opacity, transform;
  transition-property: opacity, transform;
  transition-property: opacity, transform, -webkit-transform;
  -webkit-backface-visibility: hidden;
  backface-visibility: hidden;
}
.mu-popover-transition-enter,
.mu-popover-transition-leave-active {
  -webkit-transform: scale(0.6);
  transform: scale(0.6);
  opacity: 0;
}
.mu-bottom-sheet-transition-enter-active,
.mu-bottom-sheet-transition-leave-active {
  -webkit-transition: -webkit-transform 0.45s cubic-bezier(0.23, 1, 0.32, 1);
  transition: -webkit-transform 0.45s cubic-bezier(0.23, 1, 0.32, 1);
  -o-transition: transform 0.45s cubic-bezier(0.23, 1, 0.32, 1);
  transition: transform 0.45s cubic-bezier(0.23, 1, 0.32, 1);
  transition: transform 0.45s cubic-bezier(0.23, 1, 0.32, 1),
    -webkit-transform 0.45s cubic-bezier(0.23, 1, 0.32, 1);
  -webkit-backface-visibility: hidden;
  backface-visibility: hidden;
}
.mu-bottom-sheet-transition-enter,
.mu-bottom-sheet-transition-leave-active {
  -webkit-transform: translate3d(0, 100%, 0);
  transform: translate3d(0, 100%, 0);
}
.mu-slide-top-transition-enter-active,
.mu-slide-top-transition-leave-active {
  -webkit-transition: opacity 0.45s cubic-bezier(0.23, 1, 0.32, 1),
    -webkit-transform 0.45s cubic-bezier(0.23, 1, 0.32, 1);
  transition: opacity 0.45s cubic-bezier(0.23, 1, 0.32, 1),
    -webkit-transform 0.45s cubic-bezier(0.23, 1, 0.32, 1);
  -o-transition: transform 0.45s cubic-bezier(0.23, 1, 0.32, 1),
    opacity 0.45s cubic-bezier(0.23, 1, 0.32, 1);
  transition: transform 0.45s cubic-bezier(0.23, 1, 0.32, 1),
    opacity 0.45s cubic-bezier(0.23, 1, 0.32, 1);
  transition: transform 0.45s cubic-bezier(0.23, 1, 0.32, 1),
    opacity 0.45s cubic-bezier(0.23, 1, 0.32, 1),
    -webkit-transform 0.45s cubic-bezier(0.23, 1, 0.32, 1);
  -webkit-backface-visibility: hidden;
  backface-visibility: hidden;
}
.mu-slide-top-transition-enter,
.mu-slide-top-transition-leave-active {
  -webkit-transform: translate3d(0, -100%, 0);
  transform: translate3d(0, -100%, 0);
  opacity: 0;
}
.mu-slide-bottom-transition-enter-active,
.mu-slide-bottom-transition-leave-active {
  -webkit-transition: opacity 0.45s cubic-bezier(0.23, 1, 0.32, 1),
    -webkit-transform 0.45s cubic-bezier(0.23, 1, 0.32, 1);
  transition: opacity 0.45s cubic-bezier(0.23, 1, 0.32, 1),
    -webkit-transform 0.45s cubic-bezier(0.23, 1, 0.32, 1);
  -o-transition: transform 0.45s cubic-bezier(0.23, 1, 0.32, 1),
    opacity 0.45s cubic-bezier(0.23, 1, 0.32, 1);
  transition: transform 0.45s cubic-bezier(0.23, 1, 0.32, 1),
    opacity 0.45s cubic-bezier(0.23, 1, 0.32, 1);
  transition: transform 0.45s cubic-bezier(0.23, 1, 0.32, 1),
    opacity 0.45s cubic-bezier(0.23, 1, 0.32, 1),
    -webkit-transform 0.45s cubic-bezier(0.23, 1, 0.32, 1);
  -webkit-backface-visibility: hidden;
  backface-visibility: hidden;
}
.mu-slide-bottom-transition-enter,
.mu-slide-bottom-transition-leave-active {
  -webkit-transform: translate3d(0, 100%, 0);
  transform: translate3d(0, 100%, 0);
  opacity: 0;
}
.mu-slide-left-transition-enter-active,
.mu-slide-left-transition-leave-active {
  -webkit-transition: opacity 0.45s cubic-bezier(0.23, 1, 0.32, 1),
    -webkit-transform 0.45s cubic-bezier(0.23, 1, 0.32, 1);
  transition: opacity 0.45s cubic-bezier(0.23, 1, 0.32, 1),
    -webkit-transform 0.45s cubic-bezier(0.23, 1, 0.32, 1);
  -o-transition: transform 0.45s cubic-bezier(0.23, 1, 0.32, 1),
    opacity 0.45s cubic-bezier(0.23, 1, 0.32, 1);
  transition: transform 0.45s cubic-bezier(0.23, 1, 0.32, 1),
    opacity 0.45s cubic-bezier(0.23, 1, 0.32, 1);
  transition: transform 0.45s cubic-bezier(0.23, 1, 0.32, 1),
    opacity 0.45s cubic-bezier(0.23, 1, 0.32, 1),
    -webkit-transform 0.45s cubic-bezier(0.23, 1, 0.32, 1);
  -webkit-backface-visibility: hidden;
  backface-visibility: hidden;
}
.mu-slide-left-transition-enter,
.mu-slide-left-transition-leave-active {
  -webkit-transform: translate3d(-100%, 0, 0);
  transform: translate3d(-100%, 0, 0);
  opacity: 0;
}
.mu-slide-right-transition-enter-active,
.mu-slide-right-transition-leave-active {
  -webkit-transition: opacity 0.45s cubic-bezier(0.23, 1, 0.32, 1),
    -webkit-transform 0.45s cubic-bezier(0.23, 1, 0.32, 1);
  transition: opacity 0.45s cubic-bezier(0.23, 1, 0.32, 1),
    -webkit-transform 0.45s cubic-bezier(0.23, 1, 0.32, 1);
  -o-transition: transform 0.45s cubic-bezier(0.23, 1, 0.32, 1),
    opacity 0.45s cubic-bezier(0.23, 1, 0.32, 1);
  transition: transform 0.45s cubic-bezier(0.23, 1, 0.32, 1),
    opacity 0.45s cubic-bezier(0.23, 1, 0.32, 1);
  transition: transform 0.45s cubic-bezier(0.23, 1, 0.32, 1),
    opacity 0.45s cubic-bezier(0.23, 1, 0.32, 1),
    -webkit-transform 0.45s cubic-bezier(0.23, 1, 0.32, 1);
  -webkit-backface-visibility: hidden;
  backface-visibility: hidden;
}
.mu-slide-right-transition-enter,
.mu-slide-right-transition-leave-active {
  -webkit-transform: translate3d(100%, 0, 0);
  transform: translate3d(100%, 0, 0);
  opacity: 0;
}
.mu-scale-transition-enter-active,
.mu-scale-transition-leave-active {
  -webkit-transition: all 0.45s cubic-bezier(0.23, 1, 0.32, 1);
  -o-transition: all 0.45s cubic-bezier(0.23, 1, 0.32, 1);
  transition: all 0.45s cubic-bezier(0.23, 1, 0.32, 1);
  -webkit-backface-visibility: hidden;
  backface-visibility: hidden;
}
.mu-scale-transition-enter,
.mu-scale-transition-leave-active {
  -webkit-transform: scale(0);
  transform: scale(0);
  opacity: 0;
}
.mu-expand-enter-active,
.mu-expand-leave-active {
  -webkit-transition: all 0.45s cubic-bezier(0.23, 1, 0.32, 1);
  -o-transition: all 0.45s cubic-bezier(0.23, 1, 0.32, 1);
  transition: all 0.45s cubic-bezier(0.23, 1, 0.32, 1);
  -webkit-backface-visibility: hidden;
  backface-visibility: hidden;
  -webkit-transform: translateZ(0);
  transform: translateZ(0);
}
.mu-paper {
  -webkit-transition: all 0.45s cubic-bezier(0.23, 1, 0.32, 1);
  -o-transition: all 0.45s cubic-bezier(0.23, 1, 0.32, 1);
  transition: all 0.45s cubic-bezier(0.23, 1, 0.32, 1);
  color: rgba(0, 0, 0, 0.87);
  background-color: #fff;
}
.mu-paper-round {
  border-radius: 2px;
}
.mu-paper-circle {
  border-radius: 50%;
}
.mu-expansion-panel {
  color: rgba(0, 0, 0, 0.87);
  border-top: 1px solid rgba(0, 0, 0, 0.12);
}
.mu-expansion-panel:first-child {
  border-top-left-radius: 2px;
  border-top-right-radius: 2px;
}
.mu-expansion-panel:last-child {
  border-bottom-left-radius: 2px;
  border-bottom-right-radius: 2px;
}
.mu-expansion-panel:first-child {
  border-top: none;
}
.mu-expansion-panel__expand {
  margin: 16px 0;
  border-top: none;
}
.mu-expansion-panel__expand + .mu-expansion-panel {
  border-top: none;
}
.mu-expansion-panel__expand:first-child {
  margin-top: 0;
}
.mu-expansion-panel__expand:last-child {
  margin-bottom: 0;
}
.mu-expansion-panel-header {
  display: -webkit-box;
  display: -webkit-flex;
  display: -ms-flexbox;
  display: flex;
  -webkit-box-align: center;
  -webkit-align-items: center;
  -ms-flex-align: center;
  align-items: center;
  min-height: 48px;
  padding: 0 24px;
  font-size: 15px;
  cursor: pointer;
  -webkit-transition: min-height 0.15s cubic-bezier(0.4, 0, 0.2, 1) 0ms,
    background-color 0.15s cubic-bezier(0.4, 0, 0.2, 1) 0ms;
  -o-transition: min-height 0.15s cubic-bezier(0.4, 0, 0.2, 1) 0ms,
    background-color 0.15s cubic-bezier(0.4, 0, 0.2, 1) 0ms;
  transition: min-height 0.15s cubic-bezier(0.4, 0, 0.2, 1) 0ms,
    background-color 0.15s cubic-bezier(0.4, 0, 0.2, 1) 0ms;
}
.mu-expansion-panel__expand .mu-expansion-panel-header {
  min-height: 64px;
}
.mu-expansion-toggle-btn.mu-button {
  margin-left: auto;
  margin-right: -12px;
  color: rgba(0, 0, 0, 0.54);
  -webkit-transform: transform 0.15s cubic-bezier(0.4, 0, 0.2, 1);
  transform: transform 0.15s cubic-bezier(0.4, 0, 0.2, 1);
}
.mu-expansion-toggle-btn.mu-button svg {
  width: 24px;
  height: 24px;
  fill: currentColor;
  -webkit-flex-shrink: 0;
  -ms-flex-negative: 0;
  flex-shrink: 0;
}
.mu-expansion-panel__expand .mu-expansion-toggle-btn.mu-button {
  -webkit-transform: rotate(180deg);
  transform: rotate(180deg);
}
.mu-expansion-panel-content {
  padding: 8px 24px 24px;
}
.mu-expansion-panel-actions {
  display: -webkit-box;
  display: -webkit-flex;
  display: -ms-flexbox;
  display: flex;
  -webkit-box-pack: end;
  -webkit-justify-content: flex-end;
  -ms-flex-pack: end;
  justify-content: flex-end;
  padding: 16px 8px;
  border-top: 1px solid rgba(0, 0, 0, 0.12);
}
.mu-expansion-panel-actions .mu-button + .mu-button {
  margin-left: 8px;
}
.mu-inverse {
  color: #fff;
}

</style>
