<script>
import { VAceEditor } from 'vue3-ace-editor';
import '../ace-config';
import SpeechToCode from './SpeechToCode.vue';

export default {
    props: ['question', 'index', 'is_graded'],

    data() {
        return {
            code: '# Write your code here\n',
            hint: null,
            assessment_type: this.is_graded ? 'graded' : 'practice',
            publicGrade: null,
            privateGrade: null,
            result: {},
            submitted: false,
            feedback: null,
            tip: null,
            error: null,
        };
    },

    components: {
        VAceEditor,
        SpeechToCode,
    },

    methods: {
        async speechToCode(transcript) {
            const response = await fetch(`http://127.0.0.1:5000/api/v1/transcript-to-code`, {
                method: 'POST',
                headers: {
                    'Authentication-Token': sessionStorage.getItem('auth-token'),
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    audio_transcript: transcript,
                    coding_language: 'python',
                    'question': this.question.question
                })
            });

            const responseData = await response.json();

            if (response.ok) {
                this.code = responseData.formatted_code;
            } else {
                this.error = responseData.message;
            }
        },

        async codeHelp() {
            if (this.is_graded) {
                return;
            }
            
            const response = await fetch(`http://127.0.0.1:5000/api/v1/assignment/practice/programming/${this.$route.params.module_id}/code-help`, {
                method: 'POST',
                headers: {
                    'Authentication-Token': sessionStorage.getItem('auth-token'),
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    'question_id': this.question.question_id,
                    'partial_code': this.code
                })
            });

            const responseData = await response.json();

            if (response.ok) {
                this.hint = responseData.code_help
            } else {
                this.error = responseData.message;
            }
        },

        async runCode() {
            const response = await fetch("http://127.0.0.1:5000/api/v1/run-code", {
                method: 'POST',
                headers: {
                    'Authentication-Token': sessionStorage.getItem('auth-token'),
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    'question_id': this.question.question_id,
                    'code': this.code
                })
            });

            let responseData = await response.json();

            if (response.ok) {
                this.publicGrade = responseData.public_grade;
                responseData = responseData.result
                for (let i = 0; i < responseData.length; i++) {
                    this.result[responseData[i].test_case_id] = responseData[i];
                }
            } else {
                this.error = responseData.message;
            }
        },

        async submitCode() {
            await this.runCode();

            const response = await fetch(`http://127.0.0.1:5000/api/v1/assignment/${this.assessment_type}/programming/${this.$route.params.module_id}/submit`, {
                method: 'POST',
                headers: {
                    'Authentication-Token': sessionStorage.getItem('auth-token'),
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    'question_id': this.question.question_id,
                    'code_submission': this.code
                })
            });

            let responseData = await response.json();

            if (response.ok) {
                this.privateGrade = responseData.private_grade;
                this.publicGrade = responseData.public_grade;
                this.submitted = true;
            } else {
                this.error = responseData.message;
            }
        },

        async generateFeedback() {
            const response = await fetch(`http://127.0.0.1:5000/api/v1/assignment/${this.assessment_type}/programming/${this.$route.params.module_id}/generate-feedback`, {
                method: 'POST',
                headers: {
                    'Authentication-Token': sessionStorage.getItem('auth-token'),
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    'question_id': this.question.question_id,
                    'code_submission': this.code
                })
            });

            const responseData = await response.json();

            if (response.ok) {
                this.feedback = responseData.feedback;
                this.tip = responseData.tip;
            } else {
                this.error = responseData.message;
            }
        }
    }
};
</script>

<template>
    <div class="p-4 border-bottom border-2 align-items-center">
        <p class="fw-semibold pb-4 m-0">Q{{index + 1}}.&nbsp;{{question.question}}</p>
        <div class="row mb-4">
                <button type="button" class="btn btn-warning rounded-3 ms-4 me-4 w-25" @click="codeHelp()" v-if="!is_graded">
                    <span class="fw-medium">Get Hint</span>
                </button>
                <SpeechToCode @convert-to-code="speechToCode" :index="index" :test="question.question"/>
        </div>
        <div class="m-0 mb-4 hint-text" v-if="hint && !is_graded">
            <span class="fw-semibold"><i class="bi bi-search"></i> Hint: </span> {{hint}}
        </div>
        <v-ace-editor v-model:value="code" @init="editorInit" lang="python" theme="monokai" class="editor" style="height: 300px"/>

        <table class="table mt-4 mb-4" :id="`publicTestCase${index}`">
            <thead>
                <tr>
                    <th scope="col">#</th>
                    <th scope="col">Input</th>
                    <th scope="col">Expected Output</th>
                    <th scope="col">Actual Output</th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="(public_test_case, index) in question.test_cases.public">
                    <th scope="row">{{index + 1}}</th>
                    <td>{{public_test_case.test_input}}</td>
                    <td>{{public_test_case.expected_output}}</td>
                    <td>{{result[public_test_case.test_case_id]?.result || '-'}}</td>
                </tr>
            </tbody>
        </table>
        <p class="fw-semibold p-0 pb-2 m-0 mt-4" v-if="publicGrade">Public Test Cases Passed: {{publicGrade}}</p>
        <p class="fw-semibold p-0 pb-2 m-0" v-if="privateGrade">Private Test Cases Passed: {{privateGrade}}</p>
        <div class="row mb-2 p-4">
            <button class="btn btn-primary mt-1 w-25" type="submit" @click="runCode()" :disabled="is_graded && submitted">Run</button>
            <button class="btn btn-primary mt-1 ms-4 w-25" type="submit" @click="submitCode()" :disabled="is_graded && submitted">Submit</button>
            <button class="btn btn-warning mt-1 ms-4 w-25" type="submit" @click="generateFeedback()" v-if="submitted">Get Feedback</button>
            <div class="text-success mt-3 mb-3" v-if="submitted">
                ✓ Submitted Successfully
            </div>
            <div v-if="submitted && feedback" class="text-muted mt-3 mb-3">
                <span class="fw-medium"><i class="bi bi-chat-left-text"></i> Feedback: </span> {{feedback}}
            </div>
            <div v-if="submitted && tip" class="text-primary mt-3 mb-3">
                <span class="fw-medium"><i class="bi bi-lightbulb"></i> Tip: </span> {{tip}}
            </div>
        </div>
    </div>
</template>

<style scoped>
    .editor {
        width: 100%;
        font-size: 16px;
        border-radius: 10px;
    }

    .hint-text {
        color: #ff6c00;
    }
</style>