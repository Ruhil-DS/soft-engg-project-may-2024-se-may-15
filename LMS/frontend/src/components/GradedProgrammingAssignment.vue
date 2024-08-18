<script>
import ProgrammingQuestion from './ProgrammingQuestion.vue';

export default {
    data() {
        return {
            courseID: this.$route.params.course_id,
            moduleID: this.$route.params.module_id,
            questions: [],
            submission: [],
            submitted: false,
            due_date: null,
            grade: null,
            feedback: {},
            error: null,
        };
    },

    methods: {
        async getQuestions() {
            const grpaResponse = await fetch(`http://127.0.0.1:5000/api/v1/assignment/graded/programming/${this.moduleID}`, {
                method: 'GET',
                headers: {
                    'Authentication-Token': sessionStorage.getItem('auth-token')
                }
            });
    
            const grpaData = await grpaResponse.json();
    
            if (grpaResponse.ok) {
                this.questions = grpaData['questions'];
                this.due_date = grpaData['due_date'].split(" ")[0];
            } else {
                this.error = grpaData.message;
            }
        }
    },

    components: {
        ProgrammingQuestion,
    },

    async mounted() {
        await this.getQuestions();
    }
};
</script>

<template>
    <div class="container bg-body-secondary rounded-3">
        <div v-if="questions.length == 0">
            <div class="row m-4">
                <span class="fs-5 ps-4 pt-4 fw-medium">No Questions Yet</span>
            </div>
        </div>
        <div v-else>
            <div class="row m-4">
                <span class="fs-4 ps-4 pt-4 fw-medium">Graded Programming Assignment (GrPA) {{moduleID}}</span>
                <span class="fs-6 ps-4 text-danger">Due Date: {{due_date}}</span>
            </div>
            <div class="row bg-white rounded-3 ms-4 mt-2 me-4">
                <ProgrammingQuestion v-for="(question, index) in questions" :question="question" :index="index" :is_graded="true"/>
            </div>
        </div>
    </div>
</template>