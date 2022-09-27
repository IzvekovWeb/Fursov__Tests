import API_URL from "@/consts";
import api from "@/api";

export default {
    state: {
        statistics: null,
        selfsells: null
    },
    getters: {
        SELFSELLS(state) {
            return state.selfsells
        },
        SELFSELL_STATISTICS(state) {
            return state.statistics
        }
    },
    mutations: {
        SET_SELFSELLS(state, payload) {
            state.selfsells = payload
        },
        SET_STATISTICS(state, payload) {
            state.statistics = payload
        }
    },
    actions: {
        GET_SELFSELLS(context) {
            return api.get(API_URL + 'selfsell')
                .then(response => {
                    context.commit('SET_SELFSELLS', response.data)
                    return response.data
                })
                .catch(
                    error => {
                        console.log(error)
                        return error
                    }
                )
        },
        GET_SELFSELL_STATISTICS(context) {
            return api.get(API_URL + 'selfsell-stat')
                .then(response => {
                    context.commit('SET_STATISTICS', response.data)
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