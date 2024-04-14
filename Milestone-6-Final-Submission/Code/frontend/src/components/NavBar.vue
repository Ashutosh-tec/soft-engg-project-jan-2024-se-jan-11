<template>
    <nav class="navbar navbar-expand-lg bg-light" style="width: 100%;">
        <div class="container-fluid">
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarSupportedContent"
                aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarSupportedContent">
                <ul class="navbar-nav me-auto mb-2 mb-lg-0" v-if="user_id">
                    <li class="nav-item">
                    <router-link to="/dashboard" class="navbar-brand"><b>Dashboard</b></router-link>
                    </li>
                    <li class="nav-item">
                        <router-link to="/allTicket" class="nav-link active" aria-current="page">All Tickets</router-link>
                    </li>
                    <li class="nav-item">
                        <router-link to="/faq" class="nav-link active" aria-current="page">FAQ</router-link>
                    </li>
                </ul>
                <form class="d-flex" role="search" v-if="user_id">
                    <button class="btn btn-outline-danger" type="submit" @click="logout">Logout</button>
                </form>
            </div>
        </div>
    </nav>
</template>
<script>
import axios from 'axios';
import { mapGetters } from "vuex";
export default {
    name: 'NavBar',
    methods: {
        logout() {
            localStorage.removeItem('token');
            localStorage.removeItem('user_id');
            localStorage.removeItem('role');
            this.$store.dispatch("user_id", null);
            this.$store.dispatch("role", null);
            delete axios.defaults.headers.common["secret_authtoken"];
            this.$router.push('/');

        }
    },
    computed: {
    ...mapGetters(["user_id"]),
  },
}
</script>
