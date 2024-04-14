<template>
    <div class = "container">
        <div class= "topic-container">
            <h3><RouterLink :to="{name: 'manageUsers'}">Manage Users</RouterLink></h3>
        </div>
        <br/>
        <hr/>
        <div class= "topic-container">
            <h3><RouterLink :to="{name: 'manageFAQ'}">View New Suggestions for FAQ</RouterLink></h3>
        </div>
        <br/>
        <hr/>
        <div class = "topic-container">
            <h3><RouterLink :to= "{name: 'manageFlaggedPosts'}">View Flagged Posts</RouterLink></h3>
        </div>
    </div>
</template>
<script>
//import router from '@/router';

export default {
    name: "DashboardAdminComponent",
    data() {
        return {
            
        };
    },
    
    
}
</script>
<style scoped>
.topic-container {
    margin: 33px 63px;
}

.upvote {
    font-size: 20px;
}

.ticket-title {
    font-weight: bold;
    font-size: 25px;
}

.btn a {
    color: rgb(255, 255, 255);
    text-decoration: none;
}

a {
    color: rgb(0, 0, 0);
    text-decoration: none;
}
</style>