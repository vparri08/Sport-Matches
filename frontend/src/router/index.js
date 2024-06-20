import Vue from 'vue'
import Router from 'vue-router'
import TeamSet from '@/components/TeamSet'
import Cart from '@/components/Cart'
import Login from '@/components/Login'
import CreateAccount from '@/components/CreateAccount'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/teams',
      name: 'TeamSet',
      component: TeamSet
    },
    {
      path: '/',
      name: 'Cart',
      component: Cart
    },
    {
      path: '/userlogin',
      name: 'Login',
      component: Login
    },
    {
      path: '/create-account',
      name: 'CreateAccount',
      component: CreateAccount
    }
  ]
})
