import { createRouter, createWebHistory } from 'vue-router';
import Home from '../views/Home.vue';
import Login from '../components/Login.vue';
import Signup from '../components/Signup.vue';
import CoursePage from '../views/CoursePage.vue';
import LessonContentPage from '../components/LessonContentPage.vue';
import LessonVideoPage from '../components/LessonVideoPage.vue';
import LessonSlidePage from '../components/LessonSlidePage.vue';
import CourseDescription from '../components/CourseDescription.vue';
import AssignmentPage from '../views/AssignmentPage.vue';
import PracticeTheoryAssignment from '../components/PracticeTheoryAssignment.vue';
import GradedTheoryAssignment from '../components/GradedTheoryAssignment.vue';
import PracticeProgrammingAssignment from '../components/PracticeProgrammingAssignment.vue';
import GradedProgrammingAssignment from '../components/GradedProgrammingAssignment.vue';
import DefaultAssignment from '../components/DefaultAssignment.vue';
import RevisionPage from '../views/RevisionPage.vue';

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
          path: ':course_id',
          component: CourseDescription,
          name: 'CourseDescription'
        }
      ]
    },
    { path: '/assignment/:course_id',
      name: 'AssignmentPage',
      component: AssignmentPage,
      children: [
        {
          path: 'module/:module_id/practice/theory',
          component: PracticeTheoryAssignment,
          name: 'PracticeTheoryAssignment'
        },
        {
          path: 'module/:module_id/graded/theory',
          component: GradedTheoryAssignment,
          name: 'GradedTheoryAssignment'
        },
        {
          path: 'module/:module_id/practice/programming',
          component: PracticeProgrammingAssignment,
          name: 'PracticeProgrammingAssignment'
        },
        {
          path: 'module/:module_id/graded/programming',
          component: GradedProgrammingAssignment,
          name: 'GradedProgrammingAssignment'
        },
        {
          path: '',
          component: DefaultAssignment,
          name: 'DefaultAssignment'
        }
      ]
    },
    { path: '/revise-pain-points/:course_id', component: RevisionPage, name: 'RevisionPage' }
  ]
});

export default router;