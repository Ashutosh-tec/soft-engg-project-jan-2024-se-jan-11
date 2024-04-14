<template>
    <div class="container">
        <h1 class="text-center">Edit Ticket</h1>
        <form @submit.prevent="editCard">
            <div class="form-group">
                <label>Title</label>
                <input type="text" v-model="ct" class="form-control" autocomplete="off"
                    required />
            </div>
            <div class="form-group">
                <label>Description</label>
                <textarea v-model="cc" class="form-control" autocomplete="off"
                    required rows="10"> </textarea>
            </div>
            <button type="submit" class="btn btn-primary">Submit</button>
        </form>
    </div>

</template>
  
<script>
import axios from "axios";
export default {
    name: "EditTicketComponent",
    data() {
        return {
            ct: "",
            cc: "",
            t:this.$route.params.ticketId,
        }
    },
    async created() {
        console.log(this.t);
        await axios.get("/api/ticket").then((res) => {
            // console.log(res.data.data);
            for (var i = 0; i < res.data.data.length; i++) {
                if (res.data.data[i].ticket_id == this.t) {
                    this.ct = res.data.data[i].title;
                    this.cc = res.data.data[i].description;
                }
            }
        });
    },
    methods: {
        async editCard(e) {
            e.preventDefault();   
            var data = {
                ticket_id: this.t,
                title: this.ct,
                description: this.cc,
            };
            data = JSON.stringify(data);
            await axios.patch("/api/ticket",data).then((res) => {
                console.log(res);
                if (res.status == 200) {
                    alert("Ticket Edited Successfully");
                    this.$router.push("/dashboard");
                } else {
                    alert(res.data.message);
                }
            }).catch((err) => {
                console.log(err);
            });         
        }
    }
}
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
</style>
  