<script>
import Scratchpad from './Scratchpad.vue';
import VideoSummarizer from './VideoSummarizer.vue';

export default {
    data() {
        return {
            courseID: sessionStorage.getItem('course-id'),
            moduleID: this.$route.params.module_id,
            lessonID: this.$route.params.lesson_id,
            lessonName: null,
            lessonContent: null,
            lessonVideoUrl: null,
            lessonSlideUrl: null,
            videoID: null,
            error: null,
        }
    },

    components: {
        Scratchpad,
        VideoSummarizer,
    },

    methods: {
        computeVideoID(lessonVideoUrl) {
            this.videoID = lessonVideoUrl.split('=')[1];
        }
    },

    async mounted() {
        const iframe = document.querySelector('iframe');
        const iframeHeight = iframe.offsetWidth * 9 / 16;
        iframe.style.height = iframeHeight + 'px';

        const lessonResponse = await fetch(`http://127.0.0.1:5000/api/v1/courses/${this.courseID}/modules/${this.moduleID}/lessons/${this.lessonID}`, {
            method: 'GET',
            headers: {
                'Authentication-Token': sessionStorage.getItem('auth-token')
            }
        });

        const lessonData = await lessonResponse.json();
        
        if (lessonResponse.ok) {
            this.lessonName = lessonData['lesson_name'];
            this.lessonContent = lessonData['content']['content'];
            this.lessonVideoUrl = lessonData['content']['video_url'];
            this.lessonSlideUrl = lessonData['content']['slide_url'];
            this.computeVideoID(this.lessonVideoUrl);
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
            <iframe class="rounded-3" :src="`https://www.youtube.com/embed/${videoID}`" width="100%" :height="iframeHeight"></iframe>
        </div>
        <div class="col p-0">
            <Scratchpad :lessonID="lessonID"/>
        </div>
    </div>
    <div class="row">
        <div class="p-0">
            <VideoSummarizer :moduleID="moduleID" :lessonID="lessonID"/>
        </div>
    </div>
</template>