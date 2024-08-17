<script>
export default {
    props: ['question', 'index', 'submitted', 'feedback', 'disabled'],

    data() {
        return {
            chosenOption: null,
        };
    }
};
</script>

<template>
    <div class="p-4 border-bottom border-2">
        <p class="fw-semibold pb-2 m-0">Q{{index + 1}}.&nbsp;{{question.question}}</p>
        <div class="form-check ps-5 pb-2" v-for="(option, index) in question.options">
            <input class="form-check-input" type="radio" :name="`answer${question.question_id}`" :id="`${question.question_id}-${option.option_num}`" v-model="chosenOption" :value="option.option_num" @click="chosenOption = option.option_num; $emit('option-selected', {'question_id': question.question_id, 'chosen_option': chosenOption})" :disabled="disabled"/>
            <label class="form-check-label" :for="option.option_num" :class="{'correct-option': submitted && option.is_correct, 'wrong-option': submitted && !option.is_correct && option.option_num == chosenOption}">
                {{option.option}}
            </label>
        </div>
        <div v-if="submitted && feedback" class="text-muted mt-3 mb-3">
            <span class="fw-medium"><i class="bi bi-chat-left-text"></i> Feedback: </span> {{feedback.feedback}}
        </div>
        <div v-if="submitted && feedback" class="text-primary mt-3 mb-3">
            <span class="fw-medium"><i class="bi bi-lightbulb"></i> Tip: </span> {{feedback.tip}}
        </div>
    </div>
</template>

<style scoped>
    .correct-option {
        color: green;
        font-weight: bold;
    }

    .wrong-option {
        color: red;
        font-weight: bold;
    }
</style>