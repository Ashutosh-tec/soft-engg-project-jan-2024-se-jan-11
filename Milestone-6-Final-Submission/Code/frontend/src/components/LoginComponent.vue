<template>
  <div class="container">
    <h1 class="text-center">Login</h1>
    <form @submit.prevent="loginUser">
      <div class="form-group">
        <label>Email</label>
        <input type="text" v-model="email" class="form-control" placeholder="Enter Email" autocomplete="off" required />
      </div>
      <div class="form-group">
        <label>Password</label>
        <input type="password" v-model="password" class="form-control" placeholder="Password" autocomplete="off" required />
      </div>
      <button type="submit" class="btn btn-primary btn">Submit</button>

      <p class="text" style="margin-top:10px">
        You want to change password?<RouterLink to="/changePassword">Change Password</RouterLink>
      </p>
    </form>
  </div>
</template>

<script>
import axios from "axios";
export default {
  name: "LoginComponent",
  data() {
    return {
      email: "",
      password: ""
    };
  },
  methods: {
    loginUser(e) {
      e.preventDefault();
      axios.post("/login", {
        email: this.email,
        password: this.password
      }).then(res => {
        if (res.status == 200) {
          localStorage.setItem("token", res.data.token);
          localStorage.setItem("user_id", res.data.user_id);
          this.$store.dispatch("user_id", res.data.user_id);
          localStorage.setItem("role", res.data.role);
          this.$store.dispatch("role", res.data.role);
          axios.defaults.headers.common["secret_authtoken"] = res.data.token;
          if(res.data.role == "1"){
            this.$router.push("/dashboard");
          }
          else if(res.data.role == "3"){
            this.$router.push("/dashboard");
          }
          else if(res.data.role == "2"){
            this.$router.push("/dashboard");
          }
          else if(res.data.role == "4"){
            this.$router.push("/dashboard");
          }
        } else {
          alert(res.data.message);
        }
      }).catch(err => {
        console.log(err);
      });
    },
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
