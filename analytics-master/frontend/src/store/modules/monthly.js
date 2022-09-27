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
        MONTHLY_GOTO(state) {
            return state.goto
        },
        MONTHLY_DYNAMIC(state) {
            return state.ordersDynamic
        },
        MONTHLY_ORDERS(state) {
            return state.orders
        },
        MONTHLY_SOLD(state) {
            return state.sold
        },

    },
    mutations: {
        SET_MONTHLY_GOTO(state, payload) {
            state.goto = payload
        },
        SET_MONTHLY_DYNAMIC(state, payload) {
            state.ordersDynamic = payload
        },
        SET_MONTHLY_ORDERS(state, payload) {
            state.orders = payload
        },
        SET_MONTHLY_SOLD(state, payload) {
            state.sold = payload
        }
    },
    actions: {
        GET_MONTHLY_GOTO(context) {
            return api.get(API_URL + 'analytic/wildberries/monthly-report-goto')
                .then(response => {
                    context.commit('SET_MONTHLY_GOTO', response.data)
                    return response.data
                })
                .catch(
                    error => {
                        console.log(error)
                        return error
                    }
                )
        },
        GET_MONTHLY_DYNAMIC(context) {
            return api.get(API_URL + 'analytic/wildberries/monthly-report-dynamic-orders')
                .then(response => {
                    context.commit('SET_MONTHLY_DYNAMIC', response.data)
                    return response.data
                })
                .catch(
                    error => {
                        console.log(error)
                        return error
                    }
                )
        },
        GET_MONTHLY_ORDERS(context) {
            return api.get(API_URL + 'analytic/wildberries/monthly-report-orders')
                .then(response => {
                    context.commit('SET_MONTHLY_ORDERS', response.data)
                    return response.data
                })
                .catch(
                    error => {
                        console.log(error)
                        return error
                    }
                )
        },
        GET_MONTHLY_SOLD(context) {
            return api.get(API_URL + 'analytic/wildberries/monthly-report-sold')
                .then(response => {
                    context.commit('SET_MONTHLY_SOLD', response.data)
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