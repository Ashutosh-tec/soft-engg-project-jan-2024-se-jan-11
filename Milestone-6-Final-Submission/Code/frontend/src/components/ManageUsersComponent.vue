<template>
    <div class="container">
        <div class="container" style="margin-top: 20px;">
            <p>
                <button class="btn btn-primary heading" type="button" data-bs-toggle="collapse"
                    data-bs-target="#collapseExample" aria-expanded="false" aria-controls="collapseExample">
                    ADD A USER BY EMAIL ID
                </button>
            </p>
            <div class="collapse" id="collapseExample">
                <div class="card card-body">
                    <form v-on:submit="addUser">
                        <div class="form-group">
                            <label>Enter Email ID</label>
                            <input type="text" class="form-control" v-model="emailID" required />
                        </div>
                        <br />
                        <div class="form-group"><label>Choose Role</label><select v-model="roleID" class="form-select">
                                <option value="student">Student</option>
                                <option value="support agent">Support Agent</option>
                                <option value="admin">Admin</option>
                                <option value="manager">Manager</option>
                            </select>
                        </div>
                        <button class="btn btn-primary" type="submit">Submit</button>
                    </form>
                </div>
            </div>
        </div>
        <hr />
        <div class="container">
            <p>
                <button class="btn btn-primary heading" type="button" data-bs-toggle="collapse"
                    data-bs-target="#collapseExample2" aria-expanded="false" aria-controls="collapseExample">
                    ADD MULTIPLE USERS BY CSV FILE
                </button>
            </p>
            <div class="collapse" id="collapseExample2">
                <div class="card card-body">
                    <label> Please upload a CSV file if you wish to import data</label><br />
                    <div class="form-group"><input class="btn btn-lg" ref="file" id=file type="file" accept=".csv"
                            v-on:change="onUpload($event)" /></div>
                    <div class="col-md-4">
                        <button class="btn btn-primary" @click="fileSubmission">Submit</button>
                    </div>
                </div>
            </div>
        </div>
        <hr />
        <div class="container">
            <p>
                <button class="btn btn-primary heading" type="button" data-bs-toggle="collapse"
                    data-bs-target="#collapseExample3" aria-expanded="false" aria-controls="collapseExample">
                    DELETE USER BY USERNAME
                </button>
            </p>
            <div class="collapse" id="collapseExample3">
                <div class="card card-body">
                    <div class="form-group"><label>Enter the username you wish to delete</label><input type="text"
                            class="form-control" v-model="username" required /></div>
                    <div class="col-md-4">
                        <button class="btn btn-primary" type="submit" @click="onDelete">Delete</button>
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
    name: "ManageUsersComponent",
    data() {
        return {
            emailID: "",
            roleID: "",
            myFile: '',
            username: "",
            usernames: [],
            user_id: null,
        };

    },
    methods: {
        async onDelete(x) {
            x.preventDefault();
            await axios.get("/api/user").then((res) => {
                let data = res.data.data;
                this.usernames = data.map(({ user_name }) => user_name)
                if (!this.usernames.includes(this.username)) {
                    alert("This username doesn't exist or is an admin/manager.");
                    this.$router.go();
                }
                else {
                    data.forEach(x => { if (x.user_name == this.username) { this.user_id = x.user_id; console.log(this.user_id) } });
                }

            }).catch((err) => {
                console.log(err);
            });
            await axios.delete(`/api/user/${this.user_id}`).then(() => { alert("User deleted successfully"); this.$router.go(); }).catch((err) => { console.log(err); })
        },
        async addUser(x) {
            // console.log(this.response)
            x.preventDefault();
            let thing = null;
            if (this.roleID.toLowerCase() == "student") {
                thing = 1;
            }
            else if (this.roleID.toLowerCase() == "admin") {
                thing = 3;
            }
            else if (this.roleID.toLowerCase() == "support agent") {
                thing = 2;
            }
            else if (this.roleID.toLowerCase() == "manager") {
                thing = 4;
            }
            else {
                alert("Please choose role amongst student/admin/manager/support agent!")
                this.roleID = "";
            }
            if (this.roleID == "") {
                location.reload();
            }
            else {
                console.log(this.emailID);
                console.log(thing);
                let c = this.emailID
                var data = { email_id: c, role_id: thing };
                console.log(c);
                data = JSON.stringify(data);
                console.log("Data is :")
                console.log(data);
                await axios.post("/api/user", data).then((res) => {
                    alert("User has been successfully added.")
                    this.$router.go();
                    console.log(res)
                }).catch((err) => {
                    console.log(err);
                });
            }
        },
        onUpload() {
            this.myFile = this.$refs.file.files[0];

        },
        fileSubmission() {
            let formData = new FormData();
            console.log(this.myFile);
            formData.append('file', this.myFile);

            let authtoken = localStorage.getItem("token");
            fetch("http://localhost:5000/api/importUsers", {
                method: 'POST',
                mode: 'cors',
                cache: 'no-cache',
                credentials: 'omit',
                headers: {
                    'secret_authtoken': authtoken,
                    //'Content-Type': "multipart/form-data",
                },
                redirect: 'follow',
                referrerPolicy: 'no-referrer',
                body: formData
            }).then(() => { alert("User addition request has been received. You will get notified via email on the status.");/*location.reload()*/ }).catch(e => console.log(e));
        },
    }
}
</script>
<style scoped>
.topic-container {
    margin: 33px 63px;
}

.form-group {
    margin-bottom: 1.5rem;
}

.heading {
    background-color: white;
    color: black;
    font-size: 25px;
}

.heading:hover {
    background-color: #f1f1f1;
    color: black;
    font-size: 20px;
}
</style>