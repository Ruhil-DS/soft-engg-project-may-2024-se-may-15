<script>
import { RouterLink, RouterView } from 'vue-router'
import router from './router/index.js'
import Navbar from './components/Navbar.vue'

router.beforeEach((to, from, next) => {
  if (!(to.name === 'Login' || to.name === 'Signup') && !sessionStorage.getItem('auth-token')) {
    next({ name: 'Login' })
  } else {
    next()
  }
});

export default {
  name: 'App',

  data() {
    return {
      rerender: true
    }
  },

  components: {
    Navbar
  },

  watch: {
        $route(to, from) {
            this.rerender = !this.rerender;
        }
  },

  router
}
</script>

<template>
  <Navbar :key="rerender" />

  <RouterView />

  <footer class="bg-body-secondary align-items-center text-center" id="footer-row">
    <div class="col p-3 mt-5">
      <p class="fs-5 m-2">
        &copy; SEEK++ LMS, 2024 &ensp; <span style="font-size: 1.2rem;">|</span> &ensp; BSCS3001 SE Project &ensp; <span
          style="font-size: 1.2rem;">|</span> &ensp; Website Designed by <a
          href="https://github.com/Ruhil-DS/soft-engg-project-may-2024-se-may-15" id="credits-link"
          class="text-dark">Team 15</a>
      </p>
      <p class="fs-6 text-muted m-2">
        Niharika Girdhar,
        Zahabiyah Ghadiali,
        Anirudha Anekal,
        Ganesh P,
        Laxman Bafna,
        Pushpak Ruhil,
        Lalit Kumar,
        Archit Handa
      </p>
    </div>
  </footer>
</template>

<style scoped>
#credits-link:hover {
  color: #007dff !important;
}
</style>
