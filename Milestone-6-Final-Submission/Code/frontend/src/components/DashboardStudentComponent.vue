<template>
    <div class="container">
        <div class="topic-container">
            <div  v-for="(t, index) in tickets"  :key="index">
                <div class="row">
                    <div class="col-md-10">
                        <RouterLink :to="{ name: 'response', params: { ticketId: t.ticket_id } }">
                            <p class="ticket-title">
                                {{ t.title }}
                            </p>
                        </RouterLink>
                        <div class="btn-grp">
                            <div v-if="t.is_open == 0">
                                <span class="d-inline-block" tabindex="0" data-toggle="tooltip" title="Support agent has marked this ticket as closed. To reopen, simply reply with your query">
                                <button class="btn btn-success btn-sm disabled">Ticket Closed <i class="bi bi-patch-question-fill"></i></button>
                                </span>
                            </div>
                            <div v-else-if="t.is_open==1 && t.is_read==0">
                                <span class="d-inline-block" tabindex="0" data-toggle="tooltip" title="This ticket is still hasn't been read by a support agent. Please wait 48 hours before escalating.">
                                <button class="btn btn-sm btn-outline-danger disabled">Unread <i class="bi bi-patch-question-fill"></i></button>
                                </span>
                            </div>
                            <div v-if="t.is_open==1 && t.is_read == 1">
                                <span class="d-inline-block" tabindex="0" data-toggle="tooltip" title="A support agent has read your query. Please wait as they will respond shortly">
                                <button class="btn btn-sm btn-outline-success disabled">Read <i class="bi bi-patch-question-fill"></i></button>
                                </span>
                            </div>
                        </div>
                        <br/>
                        <p>{{ t.description }}</p>
                    </div>
                    <div class="col-md-2">
                        <div class="row">
                            <button class="btn upvote" @click="increaseVote(t.ticket_id, t.number_of_upvotes)">^<br>{{
                                t.number_of_upvotes }}</button>
                        </div>
                        <div class="row">
                            <div class="btn-group">
                                <button type="button" class="btn dropdown-toggle" data-bs-toggle="dropdown">
                                    Options
                                </button>
                                <ul class="dropdown-menu">
                                    <li class="dropdown-item text-center" @click="deleteTicket(t.ticket_id)"> Delete </li>
                                    <li class="dropdown-item text-center">
                                        <RouterLink :to="{ name: 'editTicket', params: { ticketId: t.ticket_id } }">
                                            Edit
                                        </RouterLink>
                                    </li>
                                    <li class="dropdown-item text-center" data-bs-toggle="modal" data-bs-target="#ratingModal" v-if="t.is_open==0" @click="this.selected_ticket=t.ticket_id"> Rate Resolution

                                    </li>
                                </ul>
                            </div>
                            <!-- <button class="btn btn-info" data-bs-toggle="modal" data-bs-target="#ratingModal" v-if="t.is_open==0" @click="this.selected_ticket=t.ticket_id">Rate Resolution</button> -->
                        </div>
                    </div>
                </div>
                <hr />
            </div>
        </div>
        <div class="text-center">
            <button class="btn btn-primary">
                <RouterLink to="/addTicket">New Ticket</RouterLink>
            </button>
        </div>
    </div>
    <!-- Modal -->
<div class="modal fade" id="ratingModal" tabindex="-1" aria-labelledby="ratingModalLabel" aria-hidden="true">
  <div class="modal-dialog">
    <div class="modal-content">
      <div class="modal-header">
        <h5 class="modal-title" id="ratingModalLabel"> Please rate the resolution of this ticket</h5>
        <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
      </div>
      <div class="modal-body">
    <label for="myChoice1">Very Unhappy<br />
        <input type="radio" v-model="rating" value="1" id="myChoice1"> 
    </label>
    <label for="myChoice2">Unhappy<br />
        <input type="radio" v-model="rating" value="2" id="myChoice2"> 
    </label>
    <label for="myChoice3">Neutral<br />
        <input type="radio" v-model="rating" value="3" id="myChoice3"> 
    </label>
    <label for="myChoice4">Happy<br />
        <input type="radio" v-model="rating" value="4" id="myChoice4"> 
    </label>
    <label for="myChoice5">Very Happy<br />
        <input type="radio" v-model="rating" value="5" id="myChoice5">
    </label>
      </div>
      <div class="modal-footer">
        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
        <button type="button" class="btn btn-primary" data-bs-dismiss="modal" @click="submitRating()">Submit</button>
      </div>
    </div>
  </div>
</div>
</template>
<script>
import axios from "axios";
export default {
    name: "DashboardStudentComponent",
    data() {
        return {
            tickets: [],
            rating: null,
            selected_ticket: null,
        };
    },
    async created() {
        await axios.get("/api/ticket").then((res) => {
            // console.log(res.data.data);
            for (var i = 0; i < res.data.data.length; i++) {
                this.tickets.push(res.data.data[i]);
            }
        });
    },
    methods: {
        async submitRating() {
            var data = {
                ticket_id: this.selected_ticket,
                rating: this.rating
            }
            const response = await axios.patch('/api/ticket', data)
            console.log(response)
        },
        async increaseVote(ticket_id, upVotes) {
            var data = {
                ticket_id: ticket_id,
                number_of_upvotes: upVotes + 1
            }
            data = JSON.stringify(data);
            await axios.patch("/api/ticket", data).then((res) => {
                console.log(res);
            }).catch((err) => {
                console.log(err);
            });
            this.$router.go();
        },
        async deleteTicket(ticket_id) {
            await axios.delete("/api/ticket/" + ticket_id).then((res) => {
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
/* .closed {
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
} */
.btn-grp {
    display: flex;
    flex-direction: row;
    /* margin-right: 2px; */
}

label {
  float: left;
  padding: 0 1em;
  text-align: center;
}
</style>