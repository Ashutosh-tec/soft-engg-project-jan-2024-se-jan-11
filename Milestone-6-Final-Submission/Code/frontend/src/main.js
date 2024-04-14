import { createApp } from 'vue'
import App from './App.vue'
// import 'bootstrap/dist/css/bootstrap.css'
// import 'bootstrap-vue/dist/bootstrap-vue.css'
import router from "./router";
import store from "./store";
import "./axios.js";

createApp(App).use(store).use(router).mount('#app')
