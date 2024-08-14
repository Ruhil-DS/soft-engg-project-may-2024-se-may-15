<script>
import { VAceEditor } from 'vue3-ace-editor';
import '../ace-config';

export default {
    props: ['question'],

    data() {
        return {
            code: '# Write your code here\n',
        };
    },

    components: {
        VAceEditor,
    }
};
</script>

<template>
    <div class="p-4 border-bottom border-2">
        <p class="fw-semibold pb-2 m-0">Q{{question.question_num}}.&nbsp;{{question.question}}</p>
        <v-ace-editor v-model:value="code" @init="editorInit" lang="python" theme="monokai" class="editor" style="height: 300px"/>
    </div>
</template>

<style scoped>
    .editor {
        width: 100%;
        font-size: 16px;
        border-radius: 10px;
    }
</style>