<script>
export default {
    props: ['lessonID'],

    data() {
        return {
            summary: null,
            translatedSummary: null,
            keyPoints: [],
            translatedKeyPoints: [],
            targetLanguage: 'english',
            error: null,
        }
    },

    watchers: {
        async targetLanguage() {
            // Fetch translation
        }    
    },

    async mounted() {
        // Fetch Video Summary
        const summaryResponse = await fetch(`http://127.0.0.1:5000/api/v1/courses/${this.$route.params.course_id}/modules/${this.$route.params.module_id}/lessons/${this.$route.params.lesson_id}/generate-summary/video`, {
            "method": "GET",
            "headers": {
                'Authentication-Token': sessionStorage.getItem('auth-token')
            }
        });

        const summaryData = await summaryResponse.json();

        if (summaryResponse.ok) {
            this.summary = summaryData['summary'];
            this.translatedSummary = summaryData['summary'];
            this.keyPoints = summaryData['key_points'];
            this.translatedKeyPoints = summaryData['key_points'];
        } else {
            this.error = summaryData.message;
        }
    }
};
</script>

<template>
    <div id="video-summarizer" class="rounded-3 ms-3 mt-2 p-3 bg-body-secondary">
        <h5 class="mb-3">Video Summary (AI Generated)</h5>
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
        <p class="fw-bold mb-1">Summary</p>
        {{translatedSummary}}
        <br>
        <p class="fw-bold mt-4 mb-1">Quick Key Points</p>
        <ol>
            <li v-for="(keyPoint, index) in translatedKeyPoints" :key="index">{{keyPoint}}</li>
        </ol>
    </div>
</template>