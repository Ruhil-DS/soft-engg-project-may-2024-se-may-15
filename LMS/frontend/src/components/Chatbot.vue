<script>
export default {
    props: ['courseID'],
};
</script>

<template>
    <button id="chatbotButton" type="button" class="btn btn-primary rounded-3 w-100" data-bs-toggle="modal" data-bs-target="#chatbot">
                    <span class="fw-medium">Ask pushPAK <i class="bi bi-chat-left-text-fill"></i></span>
    </button>
    <div class="modal fade" id="chatbot" tabindex="-1" aria-labelledby="chatbotLabel" aria-hidden="true">
        <div class="modal-dialog modal-lg">
            <div class="modal-content">
                <div class="modal-header">
                    <h1 class="modal-title fs-5" id="chatbotLabel"><i class="bi bi-chat-left-text"></i> Ask <abbr title="Push Pupils to Attain Knowledge">pushPAK</abbr></h1>
                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                </div>
                <div class="modal-body text-center">
                    Chatbot for Course {{courseID}}
                </div>
                <div class="modal-footer text-center fst-italic text-muted">
                    <p>Did you know, pushPAK stands for '<span class="fw-bold">push P</span>upils to <span class="fw-bold">A</span>ttain <span class="fw-bold">K</span>nowledge'?</p>
                </div>
            </div>
        </div>
    </div>
</template>

<style scoped>
#chatbotButton {
    font-size: 1.1rem;
}

.modal-footer {
    font-size: 1rem;
}
</style>