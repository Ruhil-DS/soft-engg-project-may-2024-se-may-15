<script>
import TheoryQuestion from './TheoryQuestion.vue';

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
        updateSubmission(selection) {
            const question_id = selection.question_id
            const chosen_option = selection.chosen_option

            for (let i = 0; i < this.submission.length; i++) {
                if (this.submission[i].question_id == question_id) {
                    this.submission[i].chosen_option = chosen_option;
                    return;
                }
            }

            this.submission.push({
                "question_id": selection.question_id,
                "chosen_option": selection.chosen_option
            });
            return;
        },

        async generateQuestions() {
            const response = await fetch(`http://127.0.0.1:5000/api/v1/assignment/practice/theory/${this.moduleID}/generate`, {
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
            const paResponse = await fetch(`http://127.0.0.1:5000/api/v1/assignment/practice/theory/${this.moduleID}`, {
                method: 'GET',
                headers: {
                    'Authentication-Token': sessionStorage.getItem('auth-token')
                }
            });
    
            const paData = await paResponse.json();
    
            if (paResponse.ok) {
                this.questions = paData['questions'];
                this.due_date = paData['due_date'].split(" ")[0];
            } else {
                this.error = paData.message;
            }
        },

        async submit() {
            const submitResponse = await fetch(`http://127.0.0.1:5000/api/v1/assignment/practice/theory/${this.moduleID}/submit`, {
                method: 'POST',
                headers: {
                    'Authentication-Token': sessionStorage.getItem('auth-token'),
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    "submission_date": new Date().toISOString().split("T")[0],
                    "submission": this.submission
                })
            });

            const submitData = await submitResponse.json()

            if (submitResponse.ok) {
                this.grade = submitData['grade'];
            } else {
                this.error = submitResponse.message;
            }

            this.submitted = true;

            const feedbackBody = []
            for (let i = 0; i < this.submission.length; i++) {
                feedbackBody.push({
                    "question_id": this.submission[i].question_id,
                    "submitted_option_num": this.submission[i].chosen_option
                })
            }

            const feedbackResponse = await fetch(`http://127.0.0.1:5000/api/v1/assignment/practice/theory/${this.moduleID}/generate-feedback`, {
                method: 'POST',
                headers: {
                    'Authentication-Token': sessionStorage.getItem('auth-token'),
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    "questions": feedbackBody
                })
            });

            let feedbackData = await feedbackResponse.json();

            if (feedbackResponse.ok) {
                feedbackData = feedbackData.feedback
                for (let i = 0; i < feedbackData.length; i++) {
                    this.feedback[feedbackData[i].question_id] = feedbackData[i];
                }
            } else {
                this.error = feedbackData.message;
            }
        }
    },

    components: {
        TheoryQuestion,
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
                <span class="fs-4 ps-4 pt-4 fw-medium">Practice Assignment (PA) {{moduleID}}</span>
                <span class="fs-6 ps-4 text-danger">Due Date: {{due_date}}</span>
            </div>
            <div class="row bg-white rounded-3 ms-4 mt-2 me-4">
                <TheoryQuestion v-for="(question, index) in questions" :question="question" :index="index" :submitted="submitted" :feedback="feedback[question.question_id]" @option-selected="updateSubmission"/>
            </div>
            <div class="row ms-4 mb-2 me-4 p-4">
                <p class="fw-semibold p-0 pb-2 m-0" v-if="grade">Grade: {{grade}}</p>
                <button class="btn btn-primary mt-1" style="width:10%;" type="submit" @click="submit()">Submit</button>
            </div>
        </div>
        <div class="m-4">
            <button class="btn btn-warning m-4" type="submit" @click="generateQuestions()">Generate Questions</button>
        </div>
    </div>
</template>