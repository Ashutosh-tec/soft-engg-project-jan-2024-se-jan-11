<template>
    <div class="container">
        <div class="row" style="height: 100%;">
            <div class="col-sm">
                <h1 class="text-center">Add Ticket</h1>
                <form @submit.prevent="addCard">
                    <div class="form-group">
                        <label>Title </label>
                        <i class="bi bi-patch-question-fill" data-toggle="tooltip" data-placement="top" title="As you type the title, similar queries will appear on the right. Please read them before creating a new ticket."></i>
                        <input type="text" v-model="title" class="form-control" placeholder="Enter title" autocomplete="off" required />
                    </div>
                    <div class="form-group">
                        <label>Description:</label>
                        <textarea v-model="description" class="form-control" placeholder="Enter description" autocomplete="off" required rows='5'></textarea>
                    </div>
                    <div class="form-group">
                        <label>Category:</label>
                        <select v-model="category" class="form-control" placeholder="Select category" required>
                            <option value="4">General</option>
                            <option value="3">Staff</option>
                            <option value="2">Site Feedback</option>
                        </select>
                    </div>
                    <div class="form-group">
                        <label>Priority:</label>
                        <select v-model="priority" class="form-control" placeholder="Select Priority level" required>
                        <option value="low">Low</option>
                        <option value="medium">Medium</option>
                        <option value="high">High</option>
                        <option value="urgent">Urgent</option>
                        </select>
                    </div>
                    <button type="submit" class="btn btn-primary">Submit</button>
                </form>
            </div>
            <div class="vr"></div>
            <div class="col-sm">
                <div class="container overflow-auto" style="height: 280px;">
                    <p v-if="ticketResults"> Please look at the following similar tickets before posting a new query. </p>
                    <div class="search-result" v-for="(ticketResult, index) in ticketResults"  :key="index">
                        <h3>
                            <RouterLink :to="{ name: 'response', params: { ticketId: ticketResult.ticket_id } }">
                                <div v-html="ticketResult._highlightResult.title.value"></div>
                            </RouterLink>
                        </h3>
                        <div v-html="ticketResult._highlightResult.description.value"></div>
                    </div>
                </div>
                <div class="container overflow-auto" style="height: 280px;">
                    <p v-if="ticketResults"> Please look at the following similar posts from Discourse before creating a new Ticket. </p>
                    <div class="search-result" v-for="(discourseResult, index) in discourseResults.topics" :key="index">
                        <h4><a :href="'http://localhost:4200/t/'+discourseResult.slug+'/'+discourseResult.id" target="_blank">{{ discourseResult.title }}</a></h4>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import axios from "axios";
import { debounce } from 'lodash';
export default {
    name: "AddTicketComponent",
    data() {
        return {
            title: "",
            description: "",
            category: "4",
            priority: "low",
            ticketResults: null,
            discourseResults: {},
            debouncedSearch: debounce(this.searchDiscourse, 500) // Debounce the searchDiscourse function
        };
    },
    watch: {
        title: async function (val) {
           let url = 'https://C37H2BH94X-dsn.algolia.net/1/indexes/sociogrammers_app/query'
           // eslint-disable-next-line
           let config = {
                headers: {
                    'X-Algolia-Application-Id': 'C37H2BH94X',
                    'X-Algolia-API-Key': '7ba7215d84745d2397e19ebbefb9c49a',
                }
            };
            // eslint-disable-next-line
            let data = {
                'query': val
            };
            var instance = axios.create();
            delete instance.defaults.headers.common['secret_authtoken'];
            const response = await instance.post(url, data, config)
            this.ticketResults = response.data.hits
            
            if(val.length >= 3) {
                this.debouncedSearch(val); // Call the debouncedSearch function
            }
            else {
                this.discourseResults = {};
            }
        }
    },
    methods: {
        async searchDiscourse(val) {
            try {
                const discourseUrl = 'http://127.0.0.1:5000/api/discourse/search?q='+val;
                const discourseResponse = await axios.get(discourseUrl);
                this.discourseResults = discourseResponse.data;
            } catch (error) {
                console.error('Error searching Discourse:', error);
            }
        },
        async addCard() {
            var data = {
                title: this.title,
                description: this.description,
                category: this.category,
                priority: this.priority,
                number_of_upvotes : 0,
                is_read: false,
                is_open: true,
                is_offensive: false,
                is_FAQ: false
            };
            data = JSON.stringify(data);
            await axios.post("/api/ticket",data, {
                headers: {
                    // "secret_authtoken": localStorage.getItem("token"),
                    "Content-Type": "application/json"
                }
            }).then((res) => {
                if (res.status == 200) {
                    alert("Ticket Added Successfully");
                    this.$router.push("/dashboard");
                } else {
                    alert(res.data.message);
                }
            }).catch((err) => {
                console.log(err);
            });

            await axios.post("http://localhost:5000/api/discourse/posts", {
                title: this.title,
                content: this.description,
                category: this.category
            }).then((res) => {
                console.log(res);
            }).catch((err) => {
                console.log(err);
            });

            // Trigger webhook based on priority
            if (this.priority === "high" || this.priority === "urgent") {
                this.triggerWebhook();
            }
        },
        async triggerWebhook() {
            // Implement webhook integration to notify support team
            try {
                const response = await axios.post("http://localhost:5000/webhook", {
                // Include relevant data to notify about high priority or urgent ticket
                title: this.title,
                description: this.description,
                priority: this.priority
                });
                console.log("Webhook response:", response);
            } catch (error) {
                console.error("Error triggering webhook:", error);
            }
        }
    }
};
</script>

<style scoped>
.container {
    font-family: "Muli", sans-serif;
    /* display: flex;
     */
    flex-direction: column;
    align-items: center;
    justify-content: center;
    height: 75vh;
    overflow: hidden;
    margin-top: 75px;
}

label {
    font-size: 1.2rem;
    font-weight: 500;
    margin-bottom: 5px;
}

h1 {
    font-size: 3rem;
    font-weight: 700;
    margin-bottom: 2rem;
}

.form-group {
    margin-bottom: 1.5rem;
}
.topic-container {
    margin: 33px 63px;
}

.ticket-title {
    font-weight: bold;
    font-size: 25px;
}
</style>
