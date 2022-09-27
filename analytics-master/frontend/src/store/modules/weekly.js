import API_URL from "@/consts";
import api from "@/api";

export default {
    state: {
        goto: null,
        ordersDynamic: null,
        orders: null,
        sold: null
    },
    getters: {
        WEEKLY_GOTO (state) {
            return state.goto
        },
        WEEKLY_DYNAMIC(state){
            return state.ordersDynamic
        },
        WEEKLY_ORDERS(state){
            return state.orders
        },
        WEEKLY_SOLD(state){
            return state.sold
        },

    },
    mutations: {
        SET_WEEKLY_GOTO (state, payload) {
            state.goto = payload
        },
        SET_WEEKLY_DYNAMIC(state, payload){
            state.ordersDynamic = payload
        },
        SET_WEEKLY_ORDERS(state, payload){
            state.orders = payload
        },
        SET_WEEKLY_SOLD(state, payload){
            state.sold = payload
        }
    },
    actions: {
        GET_WEEKLY_GOTO(context) {
            return api.get(API_URL + 'analytic/wildberries/weekly-report-goto')
                .then(response => {
                    context.commit('SET_WEEKLY_GOTO', response.data)
                    return response.data
                })
                .catch(
                    error => {
                        console.log(error)
                        return error
                    }
                )
        },
        GET_WEEKLY_DYNAMIC(context) {
            return api.get(API_URL + 'analytic/wildberries/weekly-report-dynamic-orders')
                .then(response => {
                    context.commit('SET_WEEKLY_DYNAMIC', response.data)
                    return response.data
                })
                .catch(
                    error => {
                        console.log(error)
                        return error
                    }
                )
        },
        GET_WEEKLY_ORDERS(context) {
            return api.get(API_URL + 'analytic/wildberries/weekly-report-orders')
                .then(response => {
                    context.commit('SET_WEEKLY_ORDERS', response.data)
                    return response.data
                })
                .catch(
                    error => {
                        console.log(error)
                        return error
                    }
                )
        },
        GET_WEEKLY_SOLD(context) {
            return api.get(API_URL + 'analytic/wildberries/weekly-report-sold')
                .then(response => {
                    context.commit('SET_WEEKLY_SOLD', response.data)
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