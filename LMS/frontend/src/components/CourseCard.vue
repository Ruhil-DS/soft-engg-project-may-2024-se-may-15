<script>
export default {
    props: ['course'],

    data() {
        return {
            userRole: sessionStorage.getItem('role'),
        }
    },

    methods: {
        goToCourse() {
            sessionStorage.setItem('course-id', this.course.course_id);
            this.$router.push({ path: `/course/${this.course.course_id}` });
        }
    }
};
</script>

<template>
    <div class="card m-3 p-3" style="width: 20rem;">
        <img :src="'src/assets/CourseBackground.png'" class="card-img-top" :alt="course.course_name + ' Image'" style="height: 170px; object-fit: cover;">
        <div class="card-body" style="height: 320px">
            <h5 class="card-title">{{course.course_name}}</h5>
            <p class="card-text">{{course.course_description}}</p>

            <div v-if="userRole === 'student'">
                <button class="btn btn-primary m-3" @click="goToCourse()">Launch Course <i class="bi bi-rocket-takeoff-fill"></i></button>
            </div>
            
            <div v-if="userRole === 'instructor'">
                <button class="btn btn-primary" @click="goToCourse()">Manage Course <i class="bi bi-tools"></i></button>
            </div>
        </div>
    </div>
</template>

<style scoped>
button {
    position: absolute;
    left: 0;
    bottom: 0;
}
</style>