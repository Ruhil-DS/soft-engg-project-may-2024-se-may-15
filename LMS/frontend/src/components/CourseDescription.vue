<script>
export default {
    data() {
        return {
            courseID: sessionStorage.getItem('course-id'),
            courseDescription: null,
            modules: [],
        }
    },

    async mounted() {
        const courseResponse = await fetch(`http://127.0.0.1:5000/api/v1/courses/${this.courseID}`, {
            method: 'GET',
            headers: {
                'Authentication-Token': sessionStorage.getItem('auth-token')
            }
        });

        const courseData = await courseResponse.json();
        
        if (courseResponse.ok) {
            this.courseDescription = courseData['course_description'];
        } else {
            this.error = courseData.message;
        }

        const modulesResponse = await fetch(`http://127.0.0.1:5000/api/v1/courses/${this.courseID}/modules`, {
            method: 'GET',
            headers: {
                'Authentication-Token': sessionStorage.getItem('auth-token')
            }
        });

        const modulesData = await modulesResponse.json();

        if (modulesResponse.ok) {
            this.modules = modulesData['modules'];
        } else {
            this.error = modulesData.message;
        }
    }
};
</script>

<template>
    <div>
        <h3>Course Description</h3>
        <p>
            {{courseDescription}}
        </p>
        <br>
        <h5 class="mb-3">Modules in this Course</h5>
        <dl>
            <div v-for="module in modules" :key="module.module_id">
                <dt>{{module.module_name}}</dt>
                <dd>{{module.module_description}}</dd>
            </div>
        </dl>
    </div>
</template>