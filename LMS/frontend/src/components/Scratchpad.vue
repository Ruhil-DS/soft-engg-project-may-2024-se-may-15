<script>
export default {
    props: ['lessonID'],

    data() {
        return {
            note: '',
        }
    },

    async mounted() {
        const heightResizeInterval = setInterval(() => {
            const textarea = document.querySelector('textarea');
            const scratchpad = document.querySelector('iframe');
            textarea.rows = (scratchpad.clientHeight - 112) / 26;
            console.log(textarea.rows)
        }, 500);
    }
}
</script>

<template>
    <div id="scratchpad" class="rounded-3 p-3 bg-body-secondary">
        <h4 class="mb-3">Scratchpad</h4>
        <textarea class="form-control mb-3" placeholder="Take notes..." v-model='note'></textarea>
        <button class="btn btn-primary me-3" @click="clearNote()">Clear Note</button>
        <button class="btn btn-primary" @click="saveNote()">Save Notes</button>
    </div>
</template>