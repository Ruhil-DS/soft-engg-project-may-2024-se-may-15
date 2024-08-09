<script>
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
            fileID: null,
            error: null,
        }
    },

    async mounted() {
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
        } else {
            this.error = lessonData.message;
        }
    }
};
</script>

<template>
    <div class="mb-4">
        <h4>{{lessonName}}</h4>
        <h5 class="text-muted mb-3">Lesson Content</h5>
        <p>{{lessonContent}}</p>
    </div>
</template>