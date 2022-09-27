
import API_URL from "@/consts";
import api from "@/api";

export default {
    state: {
        worstCategories: {},
        ordersDynamic: [],
        statistics: []
    },
    getters: {
        CATEGORIES_STATISTICS(state) {
            return state.statistics
        },
        WORST_CATEGORIES(state) {
            return state.worstCategories
        },
        CATEGORIES_ORDERS_DYNAMIC(state) {
            return state.ordersDynamic
        }
    },
    mutations: {
        SET_CATEGORIES_STATISTICS(state, payload) {
            state.statistics = payload
        },
        SET_WORST_CATEGORIES(state, payload) {
            state.worstCategories = payload
        },
        SET_CATEGORIES_ORDERS_DYNAMIC(state, payload) {
            state.ordersDynamic = payload
        },
    },
    actions: {
        GET_CATEGORIES_STATISTICS(context) {

            return api.get(API_URL + 'analytic/wildberries/categories-base-stat')
                .then((response) => {
                    context.commit('SET_CATEGORIES_STATISTICS', response.data)
                })
                .catch(
                    error => {
                        console.log(error)
                        return error
                    }
                )
        },
        GET_WORST_CATEGORIES(context) {
            return api.get(API_URL + 'analytic/wildberries/top-worst-categories')
                .then(response => {
                    context.commit('SET_WORST_CATEGORIES', response.data)
                    return response.data
                })
                .catch(
                    error => {
                        console.log(error)
                        return error
                    }
                )
        },
        GET_CATEGORIES_ORDERS_DYNAMIC(context) {
            return api.get(API_URL + 'analytic/wildberries/top-categories-graph')
                .then(response => {
                    context.commit('SET_CATEGORIES_ORDERS_DYNAMIC', response.data)
                    return response.data
                })
                .catch(
                    error => {
                        console.log(error)
                        return error
                    }
                )
        },
    },
}