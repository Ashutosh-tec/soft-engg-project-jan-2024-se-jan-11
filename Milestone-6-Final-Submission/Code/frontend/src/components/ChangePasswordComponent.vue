<template>
    <div class="container">
        <h1 class="text-center">Change Password</h1>
        <form @submit.prevent="loginUser">
            <div class="form-group">
                <label>Email</label>
                <input type="text" v-model="email" class="form-control" placeholder="Enter Email" autocomplete="off"
                    required />
            </div>
            <div class="form-group">
                <label>Old Password</label>
                <input type="password" v-model="oldPassword" class="form-control" placeholder="Password" autocomplete="off"
                    required />
            </div>
            <div class="form-group">
                <label>New Password</label>
                <input type="password" v-model="newPassword" class="form-control" placeholder="Password" autocomplete="off"
                    required />
            </div>
            <button type="submit" class="btn btn-primary btn-lg">Submit</button>
        </form>
    </div>
</template>
  
<script>
import axios from "axios";
export default {
    name: "ChangePasswordComponent",
    data() {
        return {
            email: "",
            oldPassword: "",
            newPassword: ""
        };
    },
    methods: {
        async loginUser(e) {
            e.preventDefault();
            console.log(this.email, this.password);
            await axios.post("/login", {
                email: this.email,
                password: this.oldPassword
            }).then(res => {
                console.log(res);
                if (res.status == 200) {
                    this.changePassword(res.data.token,res.data.user_id);
                } else {
                    alert(res.data.message);
                }
            }).catch(err => {
                console.log(err);
            });
        },
        async changePassword(token,user_id) {
            var data = {
                user_id: user_id,
                email: this.email,
                password: this.newPassword
            }
            data=JSON.stringify(data);
            await axios.patch("/api/user", data).then(res => {
                console.log(res);
                if (res.status == 200) {
                    alert("Password changed successfully");
                    this.$router.push("/");
                } else {
                    alert(res.data.message);
                }
            }).catch(err => {
                console.log(err);
            });


        }
    }
}
</script>
  
<style scoped>
.container {
    /* border: #40cbea solid 2px;
    border-radius: 20px; */
    font-family: "Muli", sans-serif;
    margin-top: 50px;
    width: 50%;
    padding: 20px 40px;
    margin-left: auto;
    margin-right: auto;
}

.container h1 {
    text-align: center;
    margin-bottom: 30px;
    font-size: 50px;
}

.form-group {
    margin-bottom: 25px;
}

label {
    font-size: 20px;
    font-weight: 500;
    color: #333;
    margin-bottom: 5px;
}
</style>
  