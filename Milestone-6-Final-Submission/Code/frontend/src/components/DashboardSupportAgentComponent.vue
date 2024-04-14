<template>
    <div class="container">
        <div class="topic-container">
            <div class="row">
                <div class="col-md-10">
                    <h3>Hi Agent</h3>
                </div>
                <div class="col-md-2">
                    <div class="btn-group">
                        <button type="button" class="btn dropdown-toggle sortB" data-bs-toggle="dropdown">
                            Sort
                        </button>
                        <ul class="dropdown-menu">
                            <li class="dropdown-item text-center" @click="sort_upvotes">Number of upvotes</li>
                            <li class="dropdown-item text-center" @click="sort_time">Time of creation</li>
                        </ul>
                    </div>
                </div>
            </div>
            <br />
            <div v-for="t in tickets" :key="t.ticket_id">
                <div class="row">
                    <div class="col-md-10">
                        <RouterLink :to="{ name: 'response', params: { ticketId: t.ticket_id } }">
                            <p class="ticket-title">
                                {{ t.title }}
                            </p>
                        </RouterLink>
                        <!-- <div class="btn-grp">
                            <div v-if="t.is_open == 0">
                                <button class="btn btn-sm open">closed</button>
                            </div>
                            <div v-else>
                                <button class="btn btn-sm closed">open</button>
                            </div>
                            <div v-if="t.is_read == 1">
                                <button class="btn btn-sm closed">read</button>
                            </div>
                            <div v-else>
                                <button class="btn btn-sm open">unread</button>
                            </div>
                        </div> -->
                        <p>{{ t.description }}</p>
                    </div>
                    <div class="col-md-2">
                        <div class="row">
                            <button class="btn upvote">^<br>{{
                                t.number_of_upvotes }}</button>
                        </div>
                        <div class="row">
                            <div class="btn-group">
                                <button type="button" class="btn dropdown-toggle" data-bs-toggle="dropdown">
                                    Options
                                </button>
                                <ul class="dropdown-menu">
                                    <li class="dropdown-item text-center" data-bs-toggle="modal" data-bs-target="#confirmModal" @click="this.selected_ticket=t.ticket_id; this.selected_creator=t.creator_id">Flag</li>
                                    <li class="dropdown-item text-center" @click="suggestFAQ(t.ticket_id)">
                                        Suggest as FAQ
                                    </li>
                                    <li class="dropdown-item text-center" @click="mark_as_closed(t.ticket_id)">
                                        Mark as closed
                                    </li>
                                </ul>
                            </div>
                        </div>
                    </div>
                </div>
                <hr />
            </div>
        </div>
         <!-- Modal -->
         <div class="modal fade" id="confirmModal" tabindex="-1" aria-labelledby="confirmModal" aria-hidden="true">
            <div class="modal-dialog">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title" id="confirmModal">Are you sure you want to flag this post as offensive ?</h5>
                        <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                    </div>
                    <!-- <div class="modal-body">

                    </div> -->
                    <div class="modal-footer">
                        <button type="button" class="btn btn-primary btn-block" data-bs-dismiss="modal"
                            @click="flagTicket(this.selected_ticket, this.selected_creator)">Yes</button>
                    <button type="button" class="btn btn-secondary btn-block btn-outline-secondary" data-bs-dismiss="modal"> No </button>

                    </div>
                </div>
            </div>
        </div>

    </div>
</template>
<script>
import axios from "axios";
export default {
    name: "DashboardSupportAgentComponent",
    data() {
        return {
            tickets: [],
            selected_ticket: null,
            selected_creator: null
        };
    },
    async created() {
        await axios.get("/api/ticketAll").then((res) => {
            // console.log(res.data.data);
            for (var i = 0; i < res.data.data.length; i++) {
                if(res.data.data[i].is_open == 1)
                    this.tickets.push(res.data.data[i]);
            }
        });
    },
    methods: {
        async flagTicket(ticket_id, creator_id) {
            var data = {
                ticket_id: ticket_id,
                is_offensive: 1
            }
            data = JSON.stringify(data);
            await axios.patch("/api/ticketAll", data).then((res) => {
                console.log(res);
            }).catch((err) => {
                console.log(err);
            });
            let flagger_id = localStorage.getItem("user_id")
            await axios.post("/api/flaggedPosts", {ticket_id: ticket_id, creator_id: creator_id, flagger_id: flagger_id});
            this.$router.go();
        },
        sort_upvotes() {
            this.tickets.sort((a, b) => {
                return b.number_of_upvotes - a.number_of_upvotes;
            });
        },
        sort_time() {
            this.tickets.sort((a, b) => {
                // console.log(new Date(b.creation_date) - new Date(a.creation_date));
                return new Date(b.creation_date) - new Date(a.creation_date);
            });
        },
        async suggestFAQ(ticket_id) {
            var data = {
                ticket_id: ticket_id,
                is_FAQ: true
            }
            // data = JSON.stringify(data);
            await axios.patch("/api/ticketAll", data).then((res) => {
                console.log(res);
            }).catch((err) => {
                console.log(err);
            });
            this.$router.go();
        },
        async mark_as_closed(ticket_id) {
            var data = {
                ticket_id: ticket_id,
                is_open: 0
            }
            data = JSON.stringify(data);
            await axios.patch("/api/ticketAll", data).then((res) => {
                console.log(res);
            }).catch((err) => {
                console.log(err);
            });
            this.$router.go();
        }
    }
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

.sortB {
    background-color: #000000;
    color: #ffffff;
    font-weight: bold;
    font-size: 10px;
    border-radius: 10%;
}

.closed {
    border: none;
    background: #2fe72f;
    border-radius: 10%;
    color: white;
    margin-bottom: 5px;
    margin-right: 10px;
}

.open {
    border: none;
    background: #e7572f;
    border-radius: 10%;
    color: white;
    margin-bottom: 5px;
    margin-right: 10px;
}

.btn-grp {
    display: flex;
    flex-direction: row;
    /* margin-right: 2px; */
}
</style>