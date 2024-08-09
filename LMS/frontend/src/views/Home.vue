<script>
import { computed } from 'vue';
import StudentDashboard from '../components/StudentDashboard.vue';

function getToday() {
  const today = new Date();
  const weekday = today.toLocaleDateString('default', { weekday: 'long'});
  const day = today.toLocaleDateString('default', { day: 'numeric'});
  const month = today.toLocaleDateString('default', { month: 'long'});
  const year = today.toLocaleDateString('default', { year: 'numeric'});

  return `${weekday} - ${day} ${month}, ${year}`
};

function getTerm() {
  const today = new Date();
  if (today.getMonth() <= 4) {
    return 'JAN ' + today.getFullYear() + ' TERM';
  } else if (today.getMonth() <= 8) {
    return 'MAY ' + today.getFullYear() + ' TERM';
  } else {
    return 'SEP ' + today.getFullYear() + ' TERM';
  }
}

export default {
  data() {
    return {
      userRole: sessionStorage.getItem('role'),
      userName: sessionStorage.getItem('username'),
      courses: [],
      error: null,
      today: null,
      term: null,
    }
  },

  components: {
    StudentDashboard,
  },

  async mounted() {
    sessionStorage.removeItem('course-id');

    this.today = getToday();
    this.term = getTerm();

    const response = await fetch('http://127.0.0.1:5000/api/v1/courses', {
      headers: {
        'Authentication-Token': sessionStorage.getItem('auth-token')
      }
    });
    const data = await response.json();
    
    if (response.ok) {
        this.courses = data;
    } else {
        this.error = data.message;
    }
  }
};
</script>

<template>
  <div class="row mt-5">
    <div class="col ms-5">
      <h3>{{userName}}'s Dashboard</h3>
    </div>
    <div class="col me-5 text-end">
      <h4>{{today}}</h4>
      <h5>{{term}}</h5>
    </div>
  </div>
  <div class="m-5 fs-5 fw-medium text-muted" v-if="error">{{error}}</div>
  <div class="m-5" v-else>
    <StudentDashboard v-if="userRole === 'student'" :courses="courses"/>
  </div>
</template>

<style scoped>
</style>