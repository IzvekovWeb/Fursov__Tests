import API_URL from "@/consts";
import api from "@/api";

export default {
    state: {
        topCategories: null,
        statistics: null,
        ordersDynamic: null,
        topOrders: null,
        topBrands: null
    },
    getters: {
        DASHBOARD_STATISTICS (state) {
            return state.statistics
        },
        DASHBOARD_TOP_CATEGORIES(state){
            return state.topCategories
        },
        DASHBOARD_ORDERS_DYNAMIC(state){
            return state.ordersDynamic
        },
        DASHBOARD_TOP_ORDERS(state){
            return state.topOrders
        },
        DASHBOARD_TOP_BRANDS(state){
            return state.topBrands
        }

    },
    mutations: {
        SET_DASHBOARD_STATISTICS (state, payload) {
            state.statistics = payload
        },
        SET_DASHBOARD_TOP_CATEGORIES(state, payload){
            state.topCategories = payload
        },
        SET_DASHBOARD_ORDERS_DYNAMIC(state, payload){
            state.ordersDynamic = payload
        },
        SET_DASHBOARD_TOP_ORDERS(state, payload){
            state.topOrders = payload
        },
        SET_DASHBOARD_TOP_BRANDS(state, payload){
            state.topBrands = payload
        }
    },
    actions: {
        GET_DASHBOARD_STATISTICS(context) {
            return api.get(API_URL + 'analytic/dashboard/base-statistic')
                .then((response) => {
                    context.commit('SET_DASHBOARD_STATISTICS', response.data)
                    return response.data
                })
                .catch(
                    error => {
                        console.log(error)
                        return error
                    }
                )
        },
        GET_DASHBOARD_TOP_CATEGORIES(context) {
            return api.get(API_URL + 'analytic/dashboard/top-categories-donut')
                .then(response => {
                    context.commit('SET_DASHBOARD_TOP_CATEGORIES', response.data)
                    return response.data
                })
                // .catch(
                //     error => {
                //         console.log(error)
                //         return error
                //     }
                // )
        },
        GET_DASHBOARD_TOP_ORDERS(context) {
            return api.get(API_URL + 'analytic/dashboard/top-orders-table')
                .then(response => {
                    context.commit('SET_DASHBOARD_TOP_ORDERS', response.data)
                    return response
                })
                .catch(
                    error => {
                        console.log(error)
                        return error
                    }
                )
        },
        GET_DASHBOARD_TOP_BRANDS(context) {
            return api.get(API_URL + 'analytic/dashboard/top-brands-table')
                .then(response => {
                    context.commit('SET_DASHBOARD_TOP_BRANDS', response.data)
                    return response
                })
                .catch(
                    error => {
                        console.log(error)
                        return error
                    }
                )
        },
        GET_DASHBOARD_ORDERS_DYNAMIC(context) {
            return api.get(API_URL + 'analytic/dashboard/top-orders-graph')
                .then(response => {
                    context.commit('SET_DASHBOARD_ORDERS_DYNAMIC', response.data)
                    return response
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