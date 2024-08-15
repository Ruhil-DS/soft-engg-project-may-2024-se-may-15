<script>
export default {
    data() {
        return {
            courseID: sessionStorage.getItem('course-id'),
            modules: [],
            moduleIDChosen: -1,
            assessmentTypeChosen: '',
            assignmentTypeChosen: '',
            error: null
        }
    },

    methods: {
        goToAssignment() {
            if (this.moduleIDChosen == -1 || this.assessmentTypeChosen === '' || this.assignmentTypeChosen === '') {
                alert('Invalid Assignment Choice!');
                return;
            }

            this.$router.push({ path: '/assignment/' + this.courseID + '/module/' + this.moduleIDChosen + '/' + this.assessmentTypeChosen + '/' + this.assignmentTypeChosen });
        }
    },

    async mounted() {
        const courseResponse = await fetch('http://127.0.0.1:5000/api/v1/courses/' + this.courseID, {
            method: 'GET',
            headers: {
                'Authentication-Token': sessionStorage.getItem('auth-token')
            }
        });

        const courseData = await courseResponse.json();
        
        if (courseResponse.ok) {
            this.courseName = courseData['course_name'];
            this.courseDescription = courseData['course_description'];
        } else {
            this.error = courseData.message;
        }

        const modulesResponse = await fetch('http://127.0.0.1:5000/api/v1/courses/' + this.courseID + '/modules', {
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
    <div class="m-4" v-if="error">
        <h5>{{error}}</h5>
    </div>
    <div v-else>
        <div class="row m-4">
            <div class="col">
                <label class="form-label fw-medium" for="module-filter">Module:</label>
                <select class="form-select" id="module-filter" v-model="moduleIDChosen" required>
                    <option value="-1" selected>- Choose Module -</option>
                    <option v-for="(module, index) in modules" :key="index" :value="module.module_id">{{module.module_name}}</option>
                </select>
            </div>
            <div class="col-3">
                <label class="form-label fw-medium" for="assessment-type-filter">Assessment Type:</label>
                <select class="form-select" id="assessment-type-filter" v-model="assessmentTypeChosen" required>
                    <option value="" selected>- Choose Assessment Type -</option>
                    <option value="practice" selected>Practice</option>
                    <option value="graded" selected>Graded</option>
                </select>
            </div>
            <div class="col-3">
                <label class="form-label fw-medium" for="assignment-type-filter">Assignment Type:</label>
                <select class="form-select" id="assignment-type-filter" v-model="assignmentTypeChosen" required>
                    <option value="" selected>- Choose Assignment Type -</option>
                    <option value="theory" selected>Theory {{assessmentTypeChosen !== '' ? `(${assessmentTypeChosen.toUpperCase().charAt(0)}A)` : ''}}</option>
                    <option value="programming" selected>Programming {{assessmentTypeChosen !== '' ? `(${assessmentTypeChosen.toUpperCase().charAt(0)}rPA)` : ''}}</option>
                </select>
            </div>
            <div class="col-2 d-flex align-items-end">
                <button class="btn btn-primary rounded-3 w-100" type="submit" @click="goToAssignment()">Test Yourself</button>
            </div>
        </div>
        <div class="row m-4">
            <div class="col">
                <router-view :key="$route.fullPath"/>
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