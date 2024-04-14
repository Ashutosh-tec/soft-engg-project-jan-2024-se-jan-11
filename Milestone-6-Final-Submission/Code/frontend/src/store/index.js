import { createStore } from "vuex";

export default createStore({ 
    state:{
        user_id: parseInt(localStorage.getItem('user_id')),
        role: parseInt(localStorage.getItem('role')),
    },
    getters:{
        user_id: (state) => {
            return state.user_id;
          },
        role: (state) => {
            return state.role;
          },
    },
    mutations:{
        user_id(state, user_id ) {
            state.user_id = user_id;
          },
        role(state, role ) {
            state.role = role;
          },
    },
    actions: {
        user_id(context, user_id) {
            context.commit("user_id", user_id);
          },
        role(context, role) {
            context.commit("role", role);
          },   
    },
    modules: {},
})