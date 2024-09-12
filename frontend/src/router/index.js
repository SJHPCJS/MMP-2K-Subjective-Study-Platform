import Vue from 'vue'
import VueRouter from 'vue-router'
import App from '../App.vue'
import IntroPage from '../components/IntroPage.vue'
import LoginPage from '../components/LoginPage.vue'
import BeforeStartPage from '../components/BeforeStartPage.vue'
import TrainPage from '../components/TrainPage.vue'
import MainPage from '@/components/MainPage.vue'
import MenuPage from '@/components/MenuPage.vue'
import ReferenceExample from '@/components/ReferenceExample.vue'
import ReferenceIntro from '@/components/ReferenceIntro.vue'
import ResultPage from '@/components/ResultPage.vue'

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    redirect: 'login'
  },
  {
    path: '/app',
    name: 'App',
    component: App
  },
  {
    path: '/login',
    name: 'LoginPage',
    component: LoginPage
  },
  {
    path: '/intro/:id',
    name: 'IntroPage',
    component: IntroPage
  },
  {
    path: '/beforeStart/:id',
    name: 'BeforeStartPage',
    component: BeforeStartPage
  },
  {
    path:'/train/:id',
    name:'TrainPage',
    component:TrainPage
  },
  {
    path: '/main-page/:id/:customParam/:batch',
    name: 'MainPage',
    component: MainPage,
  },
  {
    path:'/menu/:id',
    name:'MenuPage',
    component:MenuPage
  },
  {
    path:'/referenceExample/:id/:batch',
    name:'ReferenceExample',
    component:ReferenceExample
  },
  {
    path:'/referenceIntro/:id/:batch',
    name:'ReferenceIntro',
    component:ReferenceIntro
  },
  {
    path:'/result/:id',
    name:'ResultPage',
    component:ResultPage
  }
]

const router = new VueRouter({
  routes,
  mode: "history"
})

export default router
