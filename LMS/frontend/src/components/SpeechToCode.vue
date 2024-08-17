<script setup>
import { ref, onMounted } from 'vue';

const props = defineProps(['index', 'test']);

const transcript = ref('');
const isRecording = ref(false);

const Recognition = window.SpeechRecognition || window.webkitSpeechRecognition;
const recognition = new Recognition();

onMounted(() => {
    recognition.continuous = true;
    recognition.interimResults = true;

    recognition.onstart = () => {
        isRecording.value = true;
    };

    recognition.onend = () => {
        isRecording.value = false;
    };

    recognition.onresult = (event) => {
        const t = Array.from(event.results)
            .map(result => result[0])
            .map(result => result.transcript)
            .join('');

        transcript.value = t;
    }
});

const toggleMic = () => {
    if (isRecording.value) {
        recognition.stop();
    } else {
        transcript.value = '';
        recognition.start();
    }
};

const hideModal = () => {
    document.getElementById(`closeButton-q${props.index}`).click();
}
</script>

<template>
    <button :id="`speechToCodeButton-q${index}`" type="button" class="btn btn-primary rounded-3 w-25 ms-4 me-4" data-bs-toggle="modal" :data-bs-target="`#speechToCode-q${index}`">
        <span class="fw-medium">Speech to Code <i class="bi bi-mic"></i></span>
    </button>
    <div class="modal fade" :id="`speechToCode-q${index}`" tabindex="-1" :aria-labelledby="`speechToCodeLabel-q${index}`" aria-hidden="true">
        <div class="modal-dialog">
            <div class="modal-content">
                <div class="modal-header">
                    <h1 class="modal-title fs-5" :id="`speechToCodeLabel-q${index}`"><i class="bi bi-mic"></i> Speech to Code</h1>
                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close" :id="`closeButton-q${index}`"></button>
                </div>
                <div class="modal-body">
                    <button class="btn" @click="toggleMic()" :class="{'btn-danger': isRecording, 'btn-secondary': !isRecording}">
                        {{isRecording ? 'Stop Recording': 'Record'}}
                    </button>
                    <hr>
                    <p class="mt-2 mb-2"><span class="fw-medium">Question: </span>{{test}}</p>
                    <br>
                    <p class="fw-medium m-0 p-0">Transcript:</p>
                    <div class="transcript" v-text="transcript"></div>
                </div>
                <div class="modal-body">
                    <button class="btn btn-primary" @click="$emit('convert-to-code', transcript); hideModal()" :disabled="!transcript || isRecording">
                        Convert to Code
                    </button>
                </div>
            </div>
        </div>
    </div>
</template>

<style scoped>

</style>