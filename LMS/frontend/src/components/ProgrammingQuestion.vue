<script>
import { VAceEditor } from 'vue3-ace-editor';
import '../ace-config';
import SpeechToCode from './SpeechToCode.vue';

export default {
    props: ['question', 'index'],

    data() {
        return {
            code: '# Write your code here\n',
            publicGrade: '5/5',
            privateGrade: '5/5'
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
        }
    }
};
</script>

<template>
    <div class="p-4 border-bottom border-2 align-items-center">
        <p class="fw-semibold pb-4 m-0">Q{{index}}.&nbsp;{{question.question}}</p>
        <div class="row mb-4">
                <button type="button" class="btn btn-warning rounded-3 ms-4 me-4 w-25" @click="">
                    <span class="fw-medium">Get Hint</span>
                </button>
                <SpeechToCode @convert-to-code="speechToCode" :index="index" :test="question.question"/>
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
                    <td>"Actual Output"</td>
                </tr>
            </tbody>
        </table>
        <p class="fw-semibold p-0 pb-2 m-0 mt-4" v-if="publicGrade">Public Test Cases Passed: {{publicGrade}}</p>
        <p class="fw-semibold p-0 pb-2 m-0" v-if="privateGrade">Private Test Cases Passed: {{privateGrade}}</p>
    </div>
</template>

<style scoped>
    .editor {
        width: 100%;
        font-size: 16px;
        border-radius: 10px;
    }
</style>