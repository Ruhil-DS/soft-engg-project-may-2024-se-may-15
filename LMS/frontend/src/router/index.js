import { createRouter, createWebHistory } from 'vue-router'
import Landing from '../views/Landing.vue'
import Login from '../components/Login.vue'
import Signup from '../components/Signup.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    { path: '/', name: 'Home', component: Landing },
    { path:'/login', name: 'Login', component: Login },
    { path: '/signup', name: 'Signup', component: Signup },
  ]
});

export default router;
