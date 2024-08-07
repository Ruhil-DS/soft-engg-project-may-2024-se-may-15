<script>
import ModuleListing from '../components/ModuleListing.vue';

export default {
    data() {
        return {
            courseID: sessionStorage.getItem('course-id'),
            courseName: null,
            courseDescription: null,
            modules: [],
            error: null
        }
    },

    components: {
        ModuleListing,
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
    <div class="row m-4" v-else>
        <div class="col-3 p-3 bg-body-secondary">
            <div class="row">
                <h5 class="fw-semibold">{{courseName}}</h5>
                <h6 class="text-muted fw-semibold fst-italic">{{courseID}}</h6>
                <hr>
            </div>
            <div class="row">
                <div class="accordion" id="modules">
                    <div class="accordion-item">
                        <h2 class="accordion-header">
                            <button class="accordion-button fw-semibold" type="button" data-bs-toggle="collapse" data-bs-target="#generalInfo" aria-expanded="true" aria-controls="generalInfo">
                                General Information
                            </button>
                        </h2>
                        <div id="generalInfo" class="accordion-collapse collapse show" data-bs-parent="#modules">
                            <div class="accordion-body">
                                Course Description
                            </div>
                        </div>
                    </div>
                    <ModuleListing v-for="module in modules" :key="module.module_id" :module="module"/>
                </div>
            </div>
        </div>
        <div class="col">
            Module View
        </div>
    </div>
</template>