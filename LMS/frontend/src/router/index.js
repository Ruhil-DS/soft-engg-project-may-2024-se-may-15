import { createRouter, createWebHistory } from 'vue-router';
import Home from '../views/Home.vue';
import Login from '../components/Login.vue';
import Signup from '../components/Signup.vue';
import CoursePage from '../views/CoursePage.vue';
import LessonContentPage from '../components/LessonContentPage.vue';
import LessonVideoPage from '../components/LessonVideoPage.vue';
import LessonSlidePage from '../components/LessonSlidePage.vue';
import CourseDescription from '../components/CourseDescription.vue';

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    { path: '/', name: 'Home', component: Home },
    { path: '/login', name: 'Login', component: Login },
    { path: '/signup', name: 'Signup', component: Signup },
    { path: '/course',
      name: 'CoursePage',
      component: CoursePage,
      children: [
        {
          path: ':course_id/module/:module_id/lesson/:lesson_id/content',
          component: LessonContentPage,
          name: 'LessonContentPage'
        },
        {
          path: ':course_id/module/:module_id/lesson/:lesson_id/video',
          component: LessonVideoPage,
          name: 'LessonVideoPage'
        },
        {
          path: ':course_id/module/:module_id/lesson/:lesson_id/slide',
          component: LessonSlidePage,
          name: 'LessonSlidePage'
        },
        {
          path: '',
          component: CourseDescription,
          name: 'CourseDescription'
        }
      ]
    },
  ]
});

export default router;