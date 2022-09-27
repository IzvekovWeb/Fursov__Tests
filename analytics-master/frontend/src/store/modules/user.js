import API_URL from "@/consts";
import api from "@/api";

export default {
    state: {
        user: null,
        suppliers: null
    },
    getters: {
        USER(state) {
            return state.user
        },
        SUPPLIERS_WITHOUT_TOKENS(state){
            return state.suppliers
        }
    },
    mutations: {
        SET_USER(state, payload) {
            localStorage.setItem('user', JSON.stringify(payload))
            state.user = payload
        },
        SET_SUPPLIERS(state, payload){
            state.suppliers = payload
        }
    },
    actions: {
        GET_USER(context) {
            if (context.state.user) return context.state.user
            return api.get(API_URL + 'user')
                .then(response => {
                    context.commit('SET_USER', response.data)
                    return response.data
                })
                .catch(
                    error => {
                        console.log(error)
                        return error
                    }
                )
        },
        GET_SUPPLIERS_WITHOUT_TOKENS(context) {
            return api.get(API_URL + 'wb-tokens')
                .then(response => {
                    context.commit('SET_SUPPLIERS', response.data)
                    return response.data
                })
                .catch(
                    error => {
                        console.log(error)
                        return error
                    }
                )
        }
    },
}