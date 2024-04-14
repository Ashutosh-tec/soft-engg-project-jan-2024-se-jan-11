import axios from "axios";
axios.defaults.baseURL = "http://localhost:5000";
axios.defaults.headers.common["secret_authtoken"] = localStorage.getItem("token");
axios.defaults.headers.post['Content-Type'] = 'application/json';
axios.defaults.headers.patch['Content-Type'] = 'application/json';
