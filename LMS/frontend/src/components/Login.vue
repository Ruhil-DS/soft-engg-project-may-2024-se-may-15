<script>
export default {
    data() {
        return {
            credential: {
                email: null,
                password: null
            },
            error: null
        }
    },
    methods: {
        async login() {
            const response = await fetch('/user-login', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(this.credential)
            });
            const data = await response.json();
            if (response.ok) {
                sessionStorage.setItem('auth-token', data.token);
                sessionStorage.setItem('user-id', data.id)
                sessionStorage.setItem('email', data.email);
                sessionStorage.setItem('username', data.username);
                sessionStorage.setItem('role', data.role);
                this.$router.push({ path: '/' });
            } else {
                this.error = data.message;
            }
        }
    }
}
</script>

<template>
    <div class='d-flex justify-content-center'>
        <div class="m-3 p-5 bg-body-secondary rounded-3">
            <p class="h3">Log In</p>
            <br>
            <label for="user-email" class="form-label">Email</label>
            <input type="email" class="form-control" id="user-email" placeholder="Enter email" v-model='credential.email' autocomplete="on" required>
            <br>
            <label for="user-password" class="form-label">Password</label>
            <input type="password" class="form-control" id="user-password" placeholder="Enter password" v-model='credential.password'  autocomplete="off" required>
            <div class='text-danger mt-3' v-if="error !== null">*{{error}}</div>
            <button class='btn btn-primary mt-3' type="submit" @click='login()'>Login</button>
            <div class="pt-3">
                <router-link to='/signup' class='text-secondary'>New to SEEK++? Sign Up</router-link>
            </div>
        </div>
    </div>
</template>

<style scoped>

</style>