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
        async generateQuestions() {
            const response = await fetch(`http://127.0.0.1:5000/api/v1/assignment/practice/programming/${this.moduleID}/generate`, {
                method: 'POST',
                headers: {
                    'Authentication-Token': sessionStorage.getItem('auth-token')
                }
            });

            if (response.ok) {
                await this.getQuestions();
            } else {
                this.error = responseData.message;
            }
        },

        async getQuestions() {
            const prpaResponse = await fetch(`http://127.0.0.1:5000/api/v1/assignment/practice/programming/${this.moduleID}`, {
                method: 'GET',
                headers: {
                    'Authentication-Token': sessionStorage.getItem('auth-token')
                }
            });
    
            const prpaData = await prpaResponse.json();
    
            if (prpaResponse.ok) {
                this.questions = prpaData['questions'];
                this.due_date = prpaData['due_date'].split(" ")[0];
            } else {
                this.error = prpaData.message;
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
                <span class="fs-5 ps-4 pt-4 fw-medium">No Questions Yet...Generate Some</span>
            </div>
        </div>
        <div v-else>
            <div class="row m-4">
                <span class="fs-4 ps-4 pt-4 fw-medium">Practice Programming Assignment (PrPA) {{moduleID}}</span>
                <span class="fs-6 ps-4 text-danger">Due Date: {{due_date}}</span>
            </div>
            <div class="row bg-white rounded-3 ms-4 mt-2 me-4">
                <ProgrammingQuestion v-for="(question, index) in questions" :question="question" :index="index" :is_graded="false"/>
            </div>
        </div>
        <div class="m-4">
            <button class="btn btn-warning m-4" type="submit" @click="generateQuestions()">Generate Questions</button>
        </div>
    </div>
</template>