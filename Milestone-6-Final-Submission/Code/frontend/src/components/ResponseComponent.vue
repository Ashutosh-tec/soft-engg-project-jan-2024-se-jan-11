<template>
    <div class="container">
        <div class="topic-container">
            <div class="row">
                <p class="ticket-title">{{ title }}</p>
                <p>{{ description }}</p>
            </div>
            <br />
            <hr />
            <h3>Responses :</h3>
            <hr />
            <br />
            <div v-for="r in responses" :key="r.response_id">
                <p class="response">{{ r.response }}</p>
                <br />
                <hr />
            </div>
            <form v-on:submit.prevent="addResponse">
                <div class="row">
                    <div class="col-md-10">
                        <textarea class="form-control" v-model="response" placeholder="Enter Response" rows="10" required> </textarea>
                    </div>
                    <div class="col-md-2">
                        <button class="btn btn-primary" type="submit">Submit</button>
                    </div>
                </div>
            </form>
        </div>
    </div>
</template>
<script>
import axios from 'axios';
import { mapGetters } from "vuex";

export default {
    name: "ResponseComponent",
    computed: {
        ...mapGetters(["role", "user_id"]),
    },
    data() {
        return {
            title: "",
            description: "",
            is_read: 0,
            is_open: null,
            ticket_id: this.$route.params.ticketId,
            cid : null,
            response: "",
            responses: []
        };
    },
    methods: {
        async editOpen() {
            // If ticket is marked as close and student replies then ticket gets reopened
            if (this.$store.state.role==1 && !this.is_open && this.$store.state.user_id==this.cid) {
                let response = await axios.patch('/api/ticket', {
                    ticket_id: this.ticket_id,
                    is_open: true
                });
                console.log(response);
            } else if (this.$store.state.role==2 && this.is_open) {
                let response = await axios.patch('/api/ticketAll', {
                    ticket_id: this.ticket_id,
                    is_open: false
                });
                console.log(response);
            }
        },
        async addResponse() {
            // console.log(this.response)
            await axios.post("/api/respTicket", {
                ticket_id: this.ticket_id,
                response: this.response
            }).then((res) => {
                this.editOpen();
                this.response = "";
                this.$router.go();
                console.log(res);
            }).catch((err) => {
                console.log(err);
            });
        }
    },
    async created() {
        await axios.get("/api/ticketAll").then((res) => {
            // console.log(res.data.data);
            for (var i = 0; i < res.data.data.length; i++) {
                if (this.ticket_id == res.data.data[i].ticket_id) {
                    this.title = res.data.data[i].title;
                    this.description = res.data.data[i].description;
                    this.is_read = res.data.data[i].is_read;
                    this.is_open = res.data.data[i].is_open;
                    this.cid = res.data.data[i].creator_id;
                }
            }
        });
        const role = localStorage.getItem("role");
        if (role == 2 && this.is_read == 0) {
            await axios.patch("/api/ticketAll", {
                ticket_id: this.ticket_id,
                is_read: 1
            }).then((res) => {
                console.log(res);
            }).catch((err) => {
                console.log(err);
            });
        }
        var data = {
            ticket_id: this.ticket_id
        }
        data = JSON.stringify(data);
        await axios.post("/api/getResponseAPI_by_ticket", data).then((res) => {
            // console.log(res.data.data);
            for (var i = 0; i < res.data.data.length; i++) {
                this.responses.push(res.data.data[i]);
            }
        }).catch((err) => {
            console.log(err);
        });

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

.response {
    font-size: 20px;

}

a {
    color: rgb(255, 255, 255);
    text-decoration: none;
}

.dropdown-menu a {
    color: rgb(0, 0, 0);
    text-decoration: none;
}
</style>