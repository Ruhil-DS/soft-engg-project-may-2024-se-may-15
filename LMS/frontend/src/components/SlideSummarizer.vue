<script>
export default {
    props: ['lessonID'],

    data() {
        return {
            summary: null,
            translatedSummary: null,
            targetLanguage: 'english',
        }
    },

    watchers: {
        async targetLanguage() {
            // Fetch translation
        }    
    },

    async mounted() {
        // Fetch Video Summary

        // Remove following after implementing above
        this.summary = 'The slide deck begins with an introduction to the list data structure, how to create it, and its basic functions...';
        this.translatedSummary = 'The slide deck begins with an introduction to the list data structure, how to create it, and its basic functions...';
    }
};
</script>

<template>
    <div id="video-summarizer" class="rounded-3 ms-3 mt-2 p-3 bg-body-secondary">
        <h5 class="mb-3">Slide Summary (AI Generated)</h5>
        <div class="input-group mb-3 w-25">
            <label class="input-group-text" for="target-language">Language</label>
            <select class="form-select" id="target-language" v-model="targetLanguage" required>
                <option value="english" selected>English</option>
                <option value="hindi">Hindi</option>
                <option value="bengali">Bengali</option>
                <option value="marathi">Marathi</option>
                <option value="tamil">Tamil</option>
                <option value="telugu">Telugu</option>
                <option value="malayalam">Malayalam</option>
                <option value="kannada">Kannada</option>
            </select>
        </div>
        {{translatedSummary}}
    </div>
</template>