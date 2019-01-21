import Vue from 'vue'
import Router from 'vue-router'
import main from '@/components/main'
import problem from '@/components/problem'
import statue from '@/components/statue'

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
      component: problem
    },
    {
      path: '/main',
      name: 'main',
      component: main
    },
    {
      path: '/statue',
      name: 'statue',
      component: statue
    }
  ]
})
