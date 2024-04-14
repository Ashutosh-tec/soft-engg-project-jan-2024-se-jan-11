<!-- <script >
import { createWebHistory, createRouter } from 'vue-router';
import ChangePasswordComponent from './components/ChangePasswordComponent.vue';
import LoginComponent from './components/LoginComponent.vue';
import DashboardStudentComponent from './components/DashboardStudentComponent.vue';
import DashboardAdminComponent from './components/DashboardAdminComponent.vue';
import DashboardSupportAgentComponent from './components/DashboardSupportAgentComponent.vue';
import AddTicketComponent from './components/AddTicketComponent.vue';
import EditTicketComponent from './components/EditTicketComponent.vue';
import AllTicketComponent from './components/AllTicketComponent.vue';
import FaqComponent from './components/FaqComponent.vue';
import ResponseComponent from './components/ResponseComponent.vue';
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
        component: DashboardStudentComponent,
    },
    {
        path: "/dashboardAdmin",
        component: DashboardAdminComponent,
    },
    {
        path: "/dashboardSupportAgent",
        component: DashboardSupportAgentComponent,
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
];

const router = createRouter({
    history: createWebHistory(),
    routes,
});

export default router;
</script> -->