<script>
export default {
    props: ['module'],

    data() {
        return {
            courseID: sessionStorage.getItem('course-id'),
            lessons: [],
            error: null,
        }
    },

    async mounted() {
        const lessonsResponse = await fetch(`http://127.0.0.1:5000/api/v1/courses/${this.courseID}/modules/${this.module.module_id}/lessons`, {
            method: 'GET',
            headers: {
                'Authentication-Token': sessionStorage.getItem('auth-token')
            } 
        });

        const lessonsData = await lessonsResponse.json();
        if (lessonsResponse.ok) {
            this.lessons = lessonsData['lessons'];
        } else {
            this.error = lessonsData.message;
        }
    }
};
</script>

<template>
    <div class="accordion-item">
        <h2 class="accordion-header">
            <button class="accordion-button collapsed fw-semibold" type="button" data-bs-toggle="collapse" :data-bs-target="`#module${module.module_id}`" aria-expanded="false" :aria-controls="`module${module.module_id}`">
                {{module.module_name}}
            </button>
        </h2>
        <div :id="`module${module.module_id}`" class="accordion-collapse collapse" data-bs-parent="#modules">
            <div class="accordion-body p-2">
                <div v-if="error">
                    {{error}}
                </div>
                <div v-else>
                    <div :class="{'border-bottom': index < lessons.length - 1}" v-for="(lesson, index) in lessons" :key="lesson.lesson_id">
                        <router-link class="text-decoration-none text-dark nav-link" :to="`/course/${courseID}/module/${module.module_id}/lesson/${lesson.lesson_id}/content`">
                            <div>{{lesson.lesson_name}}: Content</div>
                        </router-link>
                        <router-link class="text-decoration-none text-dark nav-link" :to="`/course/${courseID}/module/${module.module_id}/lesson/${lesson.lesson_id}/video`">
                            <div>{{lesson.lesson_name}}: Video</div>
                        </router-link>
                        <router-link class="text-decoration-none text-dark nav-link" :to="`/course/${courseID}/module/${module.module_id}/lesson/${lesson.lesson_id}/slide`">
                            <div>{{lesson.lesson_name}}: Slide</div>
                        </router-link>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<style scoped>
a.nav-link:hover > div {
    font-weight: 600;
    color: #007dff;
}

a.router-link-exact-active > div {
    font-weight: 600;
    color: black;
}

.accordion-button {
    color: white;
    background-color: #007dff;
}

.accordion-button:after {
  background-image: url("data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 16 16' fill='%23ffffff'><path fill-rule='evenodd' d='M1.646 4.646a.5.5 0 0 1 .708 0L8 10.293l5.646-5.647a.5.5 0 0 1 .708.708l-6 6a.5.5 0 0 1-.708 0l-6-6a.5.5 0 0 1 0-.708z'/></svg>") !important;
}
</style>