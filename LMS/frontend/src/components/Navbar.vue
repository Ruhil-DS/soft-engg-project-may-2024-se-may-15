<script>
export default {
    props: ['courseID'],

    data() {
        return {
            role: sessionStorage.getItem('role'),
            isLoggedIn: sessionStorage.getItem('auth-token') ? true : false,
            rerender: false,
        }
    },

    methods: {
        getCourseID() {
            return sessionStorage.getItem('course-id');    
        },

        logout() {
            sessionStorage.removeItem('auth-token');
            sessionStorage.removeItem('role');
            sessionStorage.removeItem('username');
            sessionStorage.removeItem('user-id');
            sessionStorage.removeItem('email');
            this.$store.commit('resetState');
            this.$router.push({ path: '/login' });
        }
    }
}
</script>

<template>
    <nav class="navbar sticky-top navbar-expand-lg bg-body-secondary">
        <div class="container-fluid">
            <a class="navbar-brand" href="#">
                <img :src="'/src/assets/Logo.png'" alt="SEEK++ Logo" style="height: 70px">
            </a>
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNavAltMarkup"
                aria-controls="navbarNavAltMarkup" aria-expanded="false" aria-label="Toggle navigation">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarNavAltMarkup">
                <div class="navbar-nav" :key="rerender">
                    <router-link class="nav-link" to="/">Home</router-link>

                    <router-link class="nav-link" v-if="courseID" :to="`/course/${courseID}`">Course</router-link>

                    <router-link class="nav-link" v-if="courseID" :to="`/assignment/${courseID}`">Assignments</router-link>

                    <router-link class="nav-link" v-if="courseID" :to="`/revise-pain-points/${courseID}`">Pain Points and Revision</router-link>

                    <!-- <router-link class="nav-link" to="/users" v-if="role === 'admin'">All Users</router-link>

                    <router-link class="nav-link" to="/create-category"
                        v-if="role === 'admin' || role === 'store_manager'">Create Category</router-link>

                    <router-link class="nav-link" to="/create-product" v-if="role === 'store_manager'">Create
                        Product</router-link>

                    <router-link class="nav-link" to="/send-request" v-if="role === 'store_manager'">Raise
                        Request</router-link>

                    <router-link class="nav-link" to="/see-request"
                        v-if="role === 'admin' || role === 'store_manager'">See Requests</router-link>

                    <router-link class="nav-link" to="/orders" v-if="role === 'user'">Orders</router-link>

                    <router-link class="nav-link" to="/stats" v-if="role === 'store_manager'">Data and
                        Statistics</router-link> -->

                    <a class="nav-link" href="#" v-if="isLoggedIn" @click="logout()">Log out</a>
                </div>
            </div>
        </div>
    </nav>
</template>

<style scoped>
a.nav-link:hover {
    font-weight: 500;
    color: #007dff;
}

a.router-link-exact-active {
    font-weight: 500;
    color: black;
}
</style>