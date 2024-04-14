<template>
    <div class="container">
        <div class="topic-container">
            <div class="container" v-for="(category, index) in categories" :key="index">
                <h3> {{ category  }}</h3>
                <br>
                <div v-for="t in tickets" :key="t.ticket_id">
               <div class="container" v-if="t.is_approved && t.category==category">
                <div class="row">
                    <div class="col-md-10">
                        <p class="ticket-title">
                            <RouterLink :to="{ name: 'response', params: { ticketId: t.ticket_id } }">
                                {{ t.title }}
                            </RouterLink>
                        </p>
                        <p>{{ t.description }}</p>
                    </div>
                    <div class="col-md-2">
                        <div class="row">
                            <button class="btn upvote" @click="increaseVote(t.ticket_id, t.number_of_upvotes)">^<br>{{
                                t.number_of_upvotes }}</button>
                        </div>
                        <div class="row" v-if="this.$store.state.role==3">
                            <div class="btn-group">
                                <button type="button" class="btn dropdown-toggle" data-bs-toggle="dropdown">
                                    Options
                                </button>
                                <ul class="dropdown-menu">
                                    <button class="dropdown-item text-center" @click="removeFromFAQ(t.ticket_id)"> Remove From FAQ </button>
                                    <button class="dropdown-item text-center" data-bs-toggle="modal" data-bs-target="#faqModal" @click="this.selected_ticket = t.ticket_id; this.selected=t.category"> Change Category </button>
                                </ul>
                            </div>
                            <!-- <button class="btn btn-info" data-bs-toggle="modal" data-bs-target="#ratingModal" v-if="t.is_open==0" @click="this.selected_ticket=t.ticket_id">Rate Resolution</button> -->
                        </div>
                    </div>
                </div>
                <hr />
            </div>
        </div>
            </div>
               </div>
        <!-- Modal -->
<div class="modal fade" id="faqModal" tabindex="-1" aria-labelledby="faqModalLabel" aria-hidden="true">
  <div class="modal-dialog">
    <div class="modal-content">
      <div class="modal-header">
        <h5 class="modal-title" id="faqModalLabel">Please choose the appropriate category</h5>
        <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
      </div>
      <div class="modal-body">
        <select v-model="selected">
            <option disabled value="">Please select one</option>
            <option v-for="(c, index) in categories"  :key="index">{{ c }}</option>
        </select>
      </div>
      <div class="modal-footer">
        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
        <button type="button" class="btn btn-success" data-bs-dismiss="modal" @click="changeCategory()">Submit</button>
      </div>
    </div>
  </div>
</div>
<div class="container" v-if="this.$store.state.role==3">
    <div class="text-center">
            <button class="btn btn-primary" data-bs-toggle="modal" data-bs-target="#categoryModal">
               New Category
            </button>
        </div>
        <!-- Modal -->
<div class="modal fade" id="categoryModal" tabindex="-1" aria-labelledby="categoryModalLabel" aria-hidden="true">
  <div class="modal-dialog">
    <div class="modal-content">
      <div class="modal-header">
        <h5 class="modal-title" id="categoryModalLabel">Please add the appropriate category name</h5>
        <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
      </div>
      <div class="modal-body">
        <div class="form-group">
                <label>Category: </label>
                <input type="text" v-model="cat" class="form-control" placeholder="Enter Category" autocomplete="off"
                    required>
            </div>
      </div>
      <div class="modal-footer">
        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
        <button type="button" class="btn btn-success" data-bs-dismiss="modal" @click=" addCategory()">Submit</button>
      </div>
    </div>
  </div>
</div>
</div>
    </div>
</template>
<script>
import axios from 'axios';

export default {
    name: "FaqComponent",
    data() {
        return {
            tickets: [],
            categories: [],
            selected_ticket: null,
            selected: null,
            cat: null
        };
    },
    async created() {
        var res2 = await axios.get('/api/category');
        this.categories = res2.data.data;
        await axios.get("/api/faq").then((res) => {
            // console.log(res.data.data);
            for (var i = 0; i < res.data.data.length; i++) {
                this.tickets.push(res.data.data[i]);
            }
        });
    },
    methods: {
        async addCategory() {
            var res = await axios.post('/api/category', {
                category: this.cat
            });
            console.log(res);
            this.$router.go();
        },
        async changeCategory() {
            var res = await axios.patch('/api/faq', {
                ticket_id: this.selected_ticket,
                is_approved: true,
                category: this.selected
            });
            console.log(res);
            this.$router.go();
        },
        async removeFromFAQ(ticket_id) {
            var res = await axios.patch('/api/faq', {
                ticket_id: ticket_id,
                is_approved: false
            });
            console.log(res);
            this.$router.go();
        },
        increaseVote(ticket_id, upVotes) {
            var data = {
                ticket_id: ticket_id,
                number_of_upvotes: upVotes + 1
            }
            data = JSON.stringify(data);
            axios.patch("/api/ticketAll", data).then((res) => {
                console.log(res);
            }).catch((err) => {
                console.log(err);
            });
            this.$router.go();
        },
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
</style>