<script>
import CourseCard from './CourseCard.vue';
export default {
    props: ['courses'],

    components: {
        CourseCard,
    }
}
</script>

<template>
    <div class="row bg-body-secondary p-3 rounded-3">
        <div class="col"> 
            <div class="row align-items-center">
                <CourseCard v-for="course in courses" :key="course.course_id" :course="course" />
            </div>
        </div>
    </div>
</template>