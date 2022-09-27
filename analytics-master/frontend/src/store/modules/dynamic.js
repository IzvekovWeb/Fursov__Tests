import API_URL from "@/consts";
import api from "@/api";

export default {
    state: {
        weekDynamic: [],
        statistics: []
    },
    getters: {
        DYNAMIC_WEEK_DYNAMIC(state) {
            return state.weekDynamic
        },
        DYNAMIC_STATISTICS(state) {
            return state.statistics
        }
    },
    mutations: {
        SET_DYNAMIC_STATISTICS(state, payload) {
            state.statistics = payload
        },
        SET_DYNAMIC_WEEK_DYNAMIC(state, payload) {
            state.weekDynamic = payload
        },
    },
    actions: {
        GET_DYNAMIC_STATISTIC(context) {
            return api.get(API_URL + 'analytic/wildberries/base-stat-dynamic-orders')
                .then((response) => {
                    context.commit('SET_DYNAMIC_STATISTICS', response.data)
                })
                .catch(
                    error => {
                        console.log(error)
                        return error
                    }
                )
        },
        GET_DYNAMIC_WEEK_DYNAMIC(context) {
            return api.get(API_URL + 'analytic/wildberries/dynamic-orders-week')
                .then(response => {
                    context.commit('SET_DYNAMIC_WEEK_DYNAMIC', response.data)
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