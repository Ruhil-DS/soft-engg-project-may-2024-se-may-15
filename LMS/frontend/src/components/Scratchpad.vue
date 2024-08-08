<script>
export default {
    props: ['lessonID'],

    data() {
        return {
            note: '',
            message: null,
            error: null,
        }
    },

    methods: {
        async saveNote() {
            const noteResponse = await fetch(`http://127.0.0.1:5000/api/v1/notes/${this.lessonID}`, {
                method: 'POST',
                headers: {
                    'Authentication-Token': sessionStorage.getItem('auth-token'),
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    note: this.note
                })
            });

            if (noteResponse.ok) {
                this.message = 'Note Saved ✓';
            } else {
                this.error = noteResponse.message;
            }
        },

        async clearNote() {
            this.note = '';
            
            const noteResponse = await fetch(`http://127.0.0.1:5000/api/v1/notes/${this.lessonID}`, {
                method: 'POST',
                headers: {
                    'Authentication-Token': sessionStorage.getItem('auth-token'),
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    note: this.note
                })
            });

            if (noteResponse.ok) {
                this.message = 'Note Cleared ✓';
            } else {
                this.error = noteResponse.message;
            }
        }
    },

    async mounted() {
        const heightResizeInterval = setInterval(() => {
            const textarea = document.querySelector('textarea');
            const scratchpad = document.querySelector('iframe');
            textarea.rows = (scratchpad.clientHeight - 112) / 26;
        }, 500);

        const noteResponse = await fetch(`http://127.0.0.1:5000/api/v1/notes/${this.lessonID}`, {
            method: 'GET',
            headers: {
                'Authentication-Token': sessionStorage.getItem('auth-token')
            }
        });

        const noteData = await noteResponse.json();
        if (noteResponse.ok) {
            this.note = noteData['note'];
        } else {
            this.error = noteData.message;
        }
    },
}
</script>

<template>
    <div id="scratchpad" class="rounded-3 p-3 bg-body-secondary">
        <h4 class="mb-3">Scratchpad</h4>
        <textarea class="form-control mb-3" placeholder="Take notes..." v-model='note'></textarea>
        <div>
            <button class="btn btn-primary me-3" @click="clearNote()">Clear Note</button>
            <button class="btn btn-primary me-3" @click="saveNote()">Save Note</button>
            <span class="text-success">{{message}}</span>
        </div>
    </div>
</template>