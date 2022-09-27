import API_URL from "@/consts";
import api from "@/api";

export default {
    state: {
        profit: null,
        turnover: null,
        result: null,
    },
    getters: {
        ABC_PROFIT(state) {
            return state.profit
        },
        ABC_TURNOVER(state) {
            return state.turnover
        },
        ABC_RESULT(state) {
            return state.result
        }
    },
    mutations: {
        SET_ABC_PROFIT(state, payload) {
            state.profit = payload
        },
        SET_ABC_TURNOVER(state, payload) {
            state.turnover = payload
        },
        SET_ABC_RESULT(state, payload) {
            state.result = payload
        }
    },
    actions: {
        GET_ABC_PROFIT(context) {
            return api.get(API_URL + 'analytic/wildberries/abc/rent')
                .then((response) => {
                    context.commit('SET_ABC_PROFIT', response.data)
                    return response.data
                })
                .catch(
                    error => {
                        console.log(error)
                        return error
                    }
                )
        },
        GET_ABC_TURNOVER(context) {
            return api.get(API_URL + 'analytic/wildberries/abc/days')
                .then(response => {
                    context.commit('SET_ABC_TURNOVER', response.data)
                    return response.data
                })
                .catch(
                    error => {
                        console.log(error)
                        return error
                    }
                )
        },
        GET_ABC_RESULT(context) {
            return api.get(API_URL + 'analytic/wildberries/abc/conclusion')
                .then(response => {
                    context.commit('SET_ABC_RESULT', response.data)
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