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
    }
  ]
})
