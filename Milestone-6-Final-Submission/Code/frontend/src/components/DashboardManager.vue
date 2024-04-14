<template>
    <div class = "container">
        <div class= "topic-container">
            <h3><RouterLink :to="{name: 'AddAdmins'}">Add Admins</RouterLink></h3>
        </div>
        <br/>
        <hr/>
    </div>
</template>
<script>
//import router from '@/router';

export default {
    name: "DashboardManagerComponent",
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