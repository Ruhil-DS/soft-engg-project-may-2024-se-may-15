<script>
export default {
    data() {
        return {
            painPoints: [],
            revisionPlan: null,
            detecting: false,
            error: null,
        }
    },

    methods: {
        async detectPainPoints() {
            this.detecting = true;

            const response = await fetch('http://127.0.0.1:5000/api/v1/detect-pain-points', {
                method: 'GET',
                headers: {
                    'Authentication-Token': sessionStorage.getItem('auth-token')
                }
            });

            const responseData = await response.json();

            if (response.ok) {
                this.painPoints = responseData.pain_points;
                this.revisionPlan = responseData.revision_plan;
            } else {
                this.error = responseData.message;
            }

            this.detecting = false;
        }
    },

    async mounted() {
        await this.detectPainPoints();
    }
}
</script>

<template>
    <div class="container bg-body-secondary">
        <div class="row m-4">
            <span class="fs-4 ps-4 pt-4 fw-medium">Pain Points and Revision Plan {{moduleID}}</span>
        </div>
        <div class="row bg-white rounded-3 ms-4 mt-2 me-4 p-4 fs-6 fw-semibold" v-if="error">
            Could Not Detect Pain Points...Make a Submission to Detect
        </div>
        <div class="row bg-white rounded-3 ms-4 mt-2 me-4 p-4" v-if="painPoints.length > 0">
            <div class="fs-5 fw-semibold mb-3">Pain Points</div>
            <ul class="ms-3">
                <li class="fs-6 m-0 mb-2" v-for="(painPoint, index) in painPoints" :key="index">{{painPoint}}</li>
            </ul>
            <hr>
            <div class="fs-5 fw-semibold mt-2 mb-3">Revision Plan</div>
            <div class="fs-6 m-0 mb-2">{{revisionPlan}}</div>
        </div>
        <div class="row ms-2 mb-2 me-4 p-4">
            <button class="btn btn-primary mt-1 fw-medium" style="width:25%;" type="submit" @click="detectPainPoints()" :disabled="detecting">
                <span class="spinner-border spinner-border-sm me-2" role="status" v-if="detecting"></span>
                <span v-if="detecting">Detecting Pain Points...</span>
                <span v-else>Detect Pain Points</span>
            </button>
        </div>
    </div>
</template>