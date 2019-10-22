import Vue from 'vue'
import Router from 'vue-router'
import main from '@/components/main'
import problem from '@/components/mainpage/problem'
import statue from '@/components/mainpage/statue'
import user from '@/components/mainpage/user'
import setting from '@/components/mainpage/setting'
import contest from '@/components/mainpage/contest'
import contestdetail from '@/components/contest/contestdetail'
import problemdetail from '@/components/problem/problemdetail'
import rank from '@/components/mainpage/rank'
import admin from '@/components/mainpage/admin'
import billboard from '@/components/mainpage/billboard'
import blog from '@/components/mainpage/blog'
import wiki from '@/components/mainpage/wiki'
import algorithm from '@/components/wiki/algorithm'
import mbcode from '@/components/wiki/code'
import trainning from '@/components/wiki/trainning'
import viewcode from '@/components/wiki/mbcode/viewcode'
import viewcodedetail from '@/components/wiki/mbcode/viewcodedetail'
import codeedit from '@/components/wiki/mbcode/codeedit'
import wikidetail from '@/components/utils/wikidetail'
import trainningdetail from '@/components/wiki/trainning/trainningdetail'
import newalgorithm from '@/components/wiki/newalgorithm'
import todolist from '@/components/utils/todolist'

Vue.use(Router)

export default new Router({
  mode: 'history',
  routes: [
    {
      path: '/',
      name: 'main',
      component: main
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
      path: '/main',
      name: 'main',
      component: main
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
    }
  ]
})
