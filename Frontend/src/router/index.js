import Vue from 'vue'
import Router from 'vue-router'
// import main from '@/components/main'
// import problem from '@/components/mainpage/problem'
// import statue from '@/components/mainpage/statue'
// import user from '@/components/mainpage/user'
// import setting from '@/components/mainpage/setting'
// import contest from '@/components/mainpage/contest'
// import contestdetail from '@/components/contest/contestdetail'
// import problemdetail from '@/components/problem/problemdetail'
// import rank from '@/components/mainpage/rank'
// import admin from '@/components/mainpage/admin'
// import billboard from '@/components/mainpage/billboard'
// import blog from '@/components/mainpage/blog'
// import wiki from '@/components/mainpage/wiki'
// import algorithm from '@/components/wiki/algorithm'
// import mbcode from '@/components/wiki/code'
// import trainning from '@/components/wiki/trainning'
// import viewcode from '@/components/wiki/mbcode/viewcode'
// import viewcodedetail from '@/components/wiki/mbcode/viewcodedetail'
// import codeedit from '@/components/wiki/mbcode/codeedit'
// import wikidetail from '@/components/utils/wikidetail'
// import trainningdetail from '@/components/wiki/trainning/trainningdetail'
// import newalgorithm from '@/components/wiki/newalgorithm'
// import todolist from '@/components/utils/todolist'
// import homework from '@/components/mainpage/homework'
// import givechoiceproblemscore from "@/components/admin/givechoiceproblemscore"

const homepage = r => require.ensure([], () => r(require("@/components/main")), 'main"');
const problem = r => require.ensure([], () => r(require("@/components/mainpage/problem")), 'mainpage');
const statue = r => require.ensure([], () => r(require("@/components/mainpage/statue")), 'mainpage'); 
const user = r => require.ensure([], () => r(require("@/components/mainpage/user")), 'mainpage');     
const setting = r => require.ensure([], () => r(require("@/components/mainpage/setting")), 'mainpage');
const contest = r => require.ensure([], () => r(require("@/components/mainpage/contest")), 'mainpage');
const contestdetail = r => require.ensure([], () => r(require("@/components/contest/contestdetail")), 'contest');
const problemdetail = r => require.ensure([], () => r(require("@/components/problem/problemdetail")), 'problem');
const rank = r => require.ensure([], () => r(require("@/components/mainpage/rank")), 'mainpage');     
const admin = r => require.ensure([], () => r(require("@/components/mainpage/admin")), 'mainpage');   
const billboard = r => require.ensure([], () => r(require("@/components/mainpage/billboard")), 'mainpage');
const blog = r => require.ensure([], () => r(require("@/components/mainpage/blog")), 'mainpage');     
const wiki = r => require.ensure([], () => r(require("@/components/mainpage/wiki")), 'mainpage');     
const algorithm = r => require.ensure([], () => r(require("@/components/wiki/algorithm")), 'wiki');   
const mbcode = r => require.ensure([], () => r(require("@/components/wiki/code")), 'wiki');
const trainning = r => require.ensure([], () => r(require("@/components/wiki/trainning")), 'wiki');   
const viewcode = r => require.ensure([], () => r(require("@/components/wiki/mbcode/viewcode")), 'wiki');
const viewcodedetail = r => require.ensure([], () => r(require("@/components/wiki/mbcode/viewcodedetail")), 'wiki');
const codeedit = r => require.ensure([], () => r(require("@/components/wiki/mbcode/codeedit")), 'wiki');
const wikidetail = r => require.ensure([], () => r(require("@/components/utils/wikidetail")), 'utils');
const trainningdetail = r => require.ensure([], () => r(require("@/components/wiki/trainning/trainningdetail")), 'wiki');
const newalgorithm = r => require.ensure([], () => r(require("@/components/wiki/newalgorithm")), 'wiki');
const todolist = r => require.ensure([], () => r(require("@/components/utils/todolist")), 'utils');
const homework = r => require.ensure([], () => r(require("@/components/mainpage/homework")), 'mainpage');
const givechoiceproblemscore = r => require.ensure([], () => r(require("@/components/admin/givechoiceproblemscore")), 'admin');
const classes = r => require.ensure([], () => r(require("@/components/mainpage/classes")), 'mainpage');
const classdetail = r => require.ensure([], () => r(require("@/components/mainpage/classdetail")), 'mainpage');


Vue.use(Router)

export default new Router({
  mode: 'history',
  routes: [
    {
      path: '/',
      name: 'homepage',
      component: homepage
    },
    {
      path: '/problem',
      name: 'problem',
      component: problem,
    },
    {
      path: '/problemdetail',
      name: 'problemdetail',
      component: problemdetail,
    },
    {
      path: '/admin',
      name: 'admin',
      component: admin
    },
    {
      path: '/statue',
      name: 'statue',
      component: statue
    },
    {
      path: '/user',
      name: 'user',
      component: user
    },
    {
      path: '/setting',
      name: 'setting',
      component: setting
    },
    {
      path: '/contest',
      name: 'contest',
      component: contest
    },
    {
      path: '/contest/:contestID',
      name: 'contestdetail',
      component: contestdetail,
    },
    {
      path: '/rank',
      name: 'rank',
      component: rank,
    },
    {
      path: '/billboard',
      name: 'billboard',
      component: billboard,
    },
    {
      path: '/blog',
      name: 'blog',
      component: blog,
    },
    {
      path: '/wiki',
      name: 'wiki',
      component: wiki,
    },
    {
      path: '/classdetail',
      name: 'classdetail',
      component: classdetail,
    },
    {
      path: '/classes',
      name: 'classes',
      component: classes,
    },
    {
      path: '/wiki/algorithm',
      name: 'algorithm',
      component: algorithm,
    },
    {
      path: '/wiki/code',
      name: 'mbcode',
      component: mbcode,
    },
    {
      path: '/wiki/trainning',
      name: 'trainning',
      component: trainning,
    },
    {
      path: '/wiki/mbcode/:username',
      name: 'viewcode',
      component: viewcode,
    },
    {
      path: '/wiki/mbcodedetail/:codeID',
      name: 'viewcodedetail',
      component: viewcodedetail,
    },
    {
      path: '/wiki/mbcodeedit',
      name: 'codeedit',
      component: codeedit,
    },
    {
      path: '/wikidetail/:wikiid',
      name: 'wikidetail',
      component: wikidetail,
    },
    {
      path: '/trainningdetail/:trainningid',
      name: 'trainningdetail',
      component: trainningdetail,
    },
    {
      path: '/wiki/newalgorithm',
      name: 'newalgorithm',
      component: newalgorithm,
    },
    {
      path: '/todolist',
      name: 'todolist',
      component: todolist,
    },
    {
      path: '/homework',
      name: 'homework',
      component: homework,
    },
    {
      path: '/givechoiceproblemscore',
      name: 'givechoiceproblemscore',
      component: givechoiceproblemscore,
    }
  ]
})
