<script>
import ProgrammingQuestion from './ProgrammingQuestion.vue';

export default {
    data() {
        return {
            courseID: this.$route.params.course_id,
            moduleID: this.$route.params.module_id,
            questions: [
                {
                    "question_id": 1,
                    "question": "Define a function list_sum() that takes a list of integers as input and returns the sum",
                    "test_cases": {
                        "public": [
                            {
                                "test_input": "[1, 2, 3, 4]",
                                "expected_output": "10"
                            }
                        ],
                        "private": [
                            {
                                "test_input": "[1, -2, 3, -4]",
                                "expected_output": "-2"
                            }
                        ]
                    }
                },
                {
                    "question_id": 2,
                    "question": "Define a function list_tuple() that takes a tuple of integers as input and returns the sum",
                    "test_cases": {
                        "public": [
                            {
                                "test_input": "[2, 2, 3, 4]",
                                "expected_output": "10"
                            }
                        ],
                        "private": [
                            {
                                "test_input": "[2, -2, 3, -4]",
                                "expected_output": "-2"
                            }
                        ]
                    }
                }
            ],
            due_date: '20 August 2024, 11:59 PM',
            grade: null,
            error: null,
        };
    },

    components: {
        ProgrammingQuestion,
    },

    async mounted() {
        // const moduleResponse = await fetch('http://127.0.0.1:5000/api/v1/courses/' + this.courseID + '/modules/' + this.moduleID, {
        //     method: 'GET',
        //     headers: {
        //         'Authentication-Token': sessionStorage.getItem('auth-token')
        //     }
        // });

        // const moduleData = await moduleResponse.json();
        
        // if (moduleResponse.ok) {
        //     this.module = moduleData['module'];
        // } else {
        //     this.error = moduleData.message;
        // }
    }
};
</script>

<template>
    <div class="container bg-body-secondary rounded-3">
        <div class="row m-4">
            <span class="fs-4 ps-4 pt-4 fw-medium">Practice Programming Assignment (PrPA) {{moduleID}}</span>
            <span class="fs-6 ps-4 text-danger">Due Date: {{due_date}}</span>
        </div>
        <div class="row bg-white rounded-3 ms-4 mt-2 me-4">
            <ProgrammingQuestion v-for="(question, index) in questions" :question="question" :index="index"/>
        </div>
        <div class="row ms-4 mb-2 me-4 p-4">
            <button class="btn btn-primary mt-1" style="width:10%;" type="submit">Submit</button>
        </div>
    </div>
</template>