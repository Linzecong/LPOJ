import Vue from 'vue'
import Router from 'vue-router'
import main from '@/components/main'
import problem from '@/components/problem'
import statue from '@/components/statue'
import user from '@/components/user'
import setting from '@/components/setting'
import contest from '@/components/contest'
import contestdetail from '@/components/contestdetail'
import problemdetail from '@/components/problemdetail'
import rank from '@/components/rank'
import admin from '@/components/admin'
import billboard from '@/components/billboard'
import blog from '@/components/blog'

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
    }
  ]
})
