<script>
export default {
    data() {
        return {
            credential: {
                username: null,
                email: null,
                password: null,
                role: 'user'
            },
            error: null
        }
    },

    methods: {
        async signup() {
            const response = await fetch('/user-signup', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(this.credential)
            });
            const data = await response.json();
            if (response.ok) {
                alert(data.message);
                this.$router.push({ path: '/login' });
            } else {
                this.error = data.message;
            }
        }
    }
}
</script>

<template>
    <div class='d-flex justify-content-center'>
        <div class="mb-3 p-5 bg-body-secondary rounded-3">
            <p class="h3">Sign Up</p>
            <br>
            <label for="username" class="form-label">Username</label>
            <input type="text" class="form-control" id="username" placeholder="Enter username" v-model='credential.username' autocomplete="on" required>
            <br>
            <label for="user-email" class="form-label">Email</label>
            <input type="email" class="form-control" id="user-email" placeholder="Enter email" v-model='credential.email' autocomplete="on" required>
            <br>
            <label for="user-password" class="form-label">Password</label>
            <input type="password" class="form-control" id="user-password" placeholder="Enter password" v-model='credential.password' autocomplete="off" required>
            <br>
            <p class="form-label">Role</p>
            <div id="role">
                <div class="form-check form-check-inline">
                    <input class="form-check-input" type="radio" name="role" id="student-role" v-model="credential.role" value="student" required>
                    <label class="form-check-label" for="student-role">Student</label>
                </div>
                <div class="form-check form-check-inline">
                    <input class="form-check-input" type="radio" name="role" id="instructor-role" v-model="credential.role" value="instructor" required>
                    <label class="form-check-label" for="instructor-role">Instructor</label>
                </div>
            </div>
            <div class='text-danger mt-3' v-if="error !== null">*{{error}}</div>
            <button class='btn btn-primary mt-3' type="submit" @click='signup()'>Sign Up</button>
            <div class="pt-3">
                <router-link to='/login' class='text-secondary'>Already have an account? Log In</router-link>
            </div>
        </div>
    </div>
</template>