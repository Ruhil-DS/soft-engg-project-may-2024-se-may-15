<script>
export default {
    props: ['courseID'],

    data() {
        return {
            message: '',
            messages: [],
            error: null,
        }
    },

    methods: {
        sendMessage() {
            if (this.message === '') {
                return
            }

            this.messages.push({
                message: this.message,
                sender: 'user'
            });
            this.message = '';
            
            // Fetch Query Backend
            const responseMessage = {
                message: 'This is a default Chatbot message',
                sender: 'chatbot'
            };
            this.messages.push(responseMessage);
        },
    },

    mounted() {
        this.messages.push({
            message: 'Hi! I am pushPAK. How can I help you?',
            sender: 'chatbot'
        });
    }
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
                <div class="modal-body">
                    <div class="p-2" v-for="message in messages">
                        <!-- Chatbot Message -->
                        <div class="row d-flex align-items-end" v-if="message.sender === 'chatbot'">
                            <div class="col-1">
                                <h5 class="bg-primary p-2 m-0 rounded-circle text-center text-light"><i class="bi bi-robot"></i></h5>
                            </div>
                            <div class="col d-flex justify-content-start">
                                <span class="row text-dark bg-body-secondary p-3 rounded-end-5 rounded-top-5 w-50 justify-content-start" >
                                    {{message.message}}
                                </span>
                            </div>
                        </div>

                        <!-- User Message -->
                        <div class="row d-flex align-items-end" v-if="message.sender === 'user'">
                            <div class="col d-flex justify-content-end">
                                <span class="row text-light bg-primary p-3 rounded-start-5 rounded-top-5 w-50 justify-content-end">
                                    {{message.message}}
                                </span>
                            </div>
                            <div class="col-1">
                                <h5 class="bg-primary p-2 m-0 rounded-circle text-center text-light"><i class="bi bi-person"></i></h5>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="modal-footer bg-body-secondary text-center fst-italic text-muted">
                    <div class="input-group mb-3">
                        <input type="text" class="form-control rounded-3 me-2" v-model="message" placeholder="Ask pushPAK or just say Hi..." aria-describedby="sendButton">
                        <button class="btn btn-primary rounded-circle" type="button" id="sendButton"><i class="bi bi-send-fill" @click="sendMessage()"></i></button>
                    </div>
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