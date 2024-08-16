<script>
export default {
    props: ['question', 'index'],

    data() {
        return {

        };
    }
};
</script>

<template>
    <div class="p-4 border-bottom border-2">
        <p class="fw-semibold pb-2 m-0">Q{{index}}.&nbsp;{{question.question}}</p>
        <div class="form-check ps-5 pb-2" v-for="(option, index) in question.options">
            <input class="form-check-input" type="radio" :name="`answer${index}`" :id="option.option_num">
            <label class="form-check-label" :for="option.option_num">
                <!-- :class="{'correct-option': option.option_num === question.correct_option_num}"> -->
                {{option.option}}
            </label>
        </div>
    </div>
</template>

<style scoped>
    .correct-option {
        color: green;
        font-weight: bold;
    }
</style>