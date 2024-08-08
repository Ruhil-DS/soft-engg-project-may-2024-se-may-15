<script>
import Scratchpad from './Scratchpad.vue';
import VideoSummarizer from './VideoSummarizer.vue';

export default {
    data() {
        return {
            courseID: sessionStorage.getItem('course-id'),
            lessonID: this.$route.params.lesson_id,
            lessonName: null,
            lessonContent: null,
            lessonVideoUrl: null,
            lessonSlideUrl: null,
            error: null,
        }
    },

    components: {
        Scratchpad,
        VideoSummarizer,
    },

    async mounted() {
        const heightResizeInterval = setInterval(() => {
            const iframe = document.querySelector('iframe');
            const iframeHeight = iframe.offsetWidth * 9 / 16;
            iframe.style.height = iframeHeight + 'px';
        }, 500);

        const lessonResponse = await fetch(`http://127.0.0.1:5000/api/v1/lessons/${this.$route.params.lesson_id}`, {
            method: 'GET',
            headers: {
                'Authentication-Token': sessionStorage.getItem('auth-token')
            }
        });

        const lessonData = await lessonResponse.json();
        
        if (lessonResponse.ok) {
            this.lessonID = lessonData['lesson_id'];
            this.lessonName = lessonData['lesson_name'];
            this.lessonContent = lessonData['content']['content'];
            this.lessonVideoUrl = lessonData['content']['video_url'];
            this.lessonSlideUrl = lessonData['content']['slide_url'];
        } else {
            this.error = lessonData.message;
        }
    }
};
</script>

<template>
    <div class="mb-4">
        <h4>{{lessonName}}</h4>
        <h5 class="text-muted mb-3">Lesson Video</h5>
    </div>
    <div class="row">
        <div class="col-8 p-0 ps-3 pe-3">
            <iframe class="rounded-3" :src="lessonVideoUrl" width="100%" :height="iframeHeight"></iframe>
        </div>
        <div class="col p-0">
            <Scratchpad :lessonID="lessonID"/>
        </div>
    </div>
    <div class="row">
        <div class="p-0">
            <VideoSummarizer :lessonID="lessonID"/>
        </div>
    </div>
</template>