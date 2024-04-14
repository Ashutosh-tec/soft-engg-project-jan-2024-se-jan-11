import { createWebHistory, createRouter } from 'vue-router';
import ChangePasswordComponent from '../components/ChangePasswordComponent.vue';
import LoginComponent from '../components/LoginComponent.vue';
import dash_board from '../components/Dashboard.vue';
// import DashboardStudentComponent from '../components/DashboardStudentComponent.vue';
// import DashboardAdminComponent from '../components/DashboardAdminComponent.vue';
// import DashboardSupportAgentComponent from '../components/DashboardSupportAgentComponent.vue';
import AddTicketComponent from '../components/AddTicketComponent.vue';
import EditTicketComponent from '../components/EditTicketComponent.vue';
import AllTicketComponent from '../components/AllTicketComponent.vue';
import FaqComponent from '../components/FaqComponent.vue';
import ResponseComponent from '../components/ResponseComponent.vue';
import ManageUsersComponent from '../components/ManageUsersComponent.vue';
import ManageFAQSuggestionsComponent from '../components/ManageFAQComponent.vue';
import ManageFlaggedPosts from '../components/ManageFlaggedPosts.vue';
import AddAdminsComponent from '../components/AddAdmins.vue';
// import store from "../store";
const routes = [
    {
        path: "/",
        component: LoginComponent,
    },
    {
        path: "/changePassword",
        component: ChangePasswordComponent,
    },
    {
        path: "/dashboard",
        component: dash_board,
    },
    {
        path: "/addTicket",
        component: AddTicketComponent,
    },
    {
        name: "editTicket",
        path: "/editTicket/:ticketId",
        component: EditTicketComponent,
        props: true
    },
    {
        path: "/allTicket",
        component: AllTicketComponent,
    },
    {
        path: "/faq",
        component: FaqComponent,
    },
    {
        path: "/response/:ticketId",
        component: ResponseComponent,
        name: "response",
        props: true
    },
    {
        path: "/manageUsers",
        component: ManageUsersComponent,
        name: "manageUsers"
        
    },
    {
        path: "/manageFAQ",
        component: ManageFAQSuggestionsComponent,
        name: "manageFAQ"
    },
    {
        path: "/manageFlaggedPosts",
        component: ManageFlaggedPosts,
        name: "manageFlaggedPosts"
    },
    {
        path: "/addAdmins",
        component: AddAdminsComponent,
        name: "AddAdmins"
    }
];
const router = createRouter({
    history: createWebHistory(),
    routes: routes,
});

export default router;