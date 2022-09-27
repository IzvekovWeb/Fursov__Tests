import API_URL from "@/consts";
import api from "@/api";

export default {
    state: {
        statistics: null,
        top: null,
        worst: null
    },
    getters: {
        PROFITABILITY_STATISTICS(state) {
            return state.statistics
        },
        PROFITABILITY_TOP(state) {
            return state.top
        },
        PROFITABILITY_WORST(state) {
            return state.worst
        }
    },
    mutations: {
        SET_PROFITABILITY_STATISTICS(state, payload) {
            state.statistics = payload
        },
        SET_PROFITABILITY_TOP(state, payload) {
            state.top = payload
        },
        SET_PROFITABILITY_WORST(state, payload) {
            state.worst = payload
        }
    },
    actions: {
        GET_PROFITABILITY_STATISTICS(context) {
            return api.get(API_URL + 'analytic/wildberries/base-stat-profitability')
                .then((response) => {
                    context.commit('SET_PROFITABILITY_STATISTICS', response.data)
                    return response.data
                })
                .catch(
                    error => {
                        console.log(error)
                        return error
                    }
                )
        },
        GET_PROFITABILITY_TOP(context) {
            return api.get(API_URL + 'analytic/wildberries/top-profit-profitability')
                .then(response => {
                    context.commit('SET_PROFITABILITY_TOP', response.data)
                    return response.data
                })
                .catch(
                    error => {
                        console.log(error)
                        return error
                    }
                )
        },
        GET_PROFITABILITY_WORST(context) {
            return api.get(API_URL + 'analytic/wildberries/worst-profit-profitability')
                .then(response => {
                    context.commit('SET_PROFITABILITY_WORST', response.data)
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