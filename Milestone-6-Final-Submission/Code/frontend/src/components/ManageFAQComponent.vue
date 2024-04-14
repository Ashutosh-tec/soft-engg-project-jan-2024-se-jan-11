<template>
    <div class="container">
        <div class="topic-container">
            <h3>The following tickets have been suggested for FAQ </h3>
            <br />
            <hr />
            <div class="container" v-for="(t, index) in relevant_tickets" :key="index">
                <div class="row">
                    <div class="col-md-10">
                        <RouterLink :to="{ name: 'response', params: { ticketId: t.ticket_id } }">
                            <p class="ticket-title">
                                {{ t.title }}
                            </p>
                        </RouterLink>
                        <p>{{ t.description }}</p>
                    </div>
                    <div class="col-md-2">
                        <button class="btn upvote disabled">^<br>{{ t.number_of_upvotes }}</button>
                    </div>
                </div>
                <div class="row">
                    <div class="col-md-2">
                        <button class="btn btn-success rounded" data-bs-toggle="modal" data-bs-target="#faqModal"
                            @click="this.selected_ticket = t.ticket_id"> Approve </button>
                    </div>
                    <div class="col-md-8">
                    </div>
                    <div class="col-md-2">
                        <button class="btn btn-danger rounded" @click="rejectFAQ(t.ticket_id)"> Reject </button>
                    </div>
                </div>
            </div>
            <hr />
        </div>
        <br />
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
                            <option v-for="(c, index) in categories" :key="index">{{ c }}</option>
                        </select>
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                        <button type="button" class="btn btn-success" data-bs-dismiss="modal"
                            @click="approveFAQ()">Submit</button>
                    </div>
                </div>
            </div>
        </div>

    </div>
</template>
<script>
//import router from '@/router';

import axios from 'axios';

export default {
    name: "ManageFAQSuggestionsComponent",
    methods: {
        async approveFAQ() {
            var res = await axios.post('/api/faq', {
                ticket_id: this.selected_ticket,
                is_approved: true,
                category: this.selected
            });
            console.log(res);
            this.$router.go();
        },
        async rejectFAQ(ticket_id) {
            var res = await axios.post('/api/faq', {
                ticket_id: ticket_id,
                is_approved: false
            });
            console.log(res);
            this.$router.go();
        },
    },
    data() {
        return {
            selected: null,
            selected_ticket: null,
            faq_ticket_ids: [],
            faqs: [],
            relevant_tickets: [],
            categories: []
        };

    },
    async created() {
        var res3 = await axios.get('/api/category');
        this.categories = res3.data.data;
        var res = await axios.get('/api/faq');
        this.faqs = res.data.data;
        this.faq_ticket_ids = this.faqs.map(({ ticket_id }) => ticket_id)
        var res2 = await axios.get('/api/ticketAll');
        for (var i = 0; i < res2.data.data.length; i++) {
            if (res2.data.data[i].is_FAQ) {
                // eslint-disable-next-line
                if (this.faq_ticket_ids.includes(res2.data.data[i].ticket_id)) { } else {
                    this.relevant_tickets.push(res2.data.data[i]);
                }
            }
        }
    },
    computed: {
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