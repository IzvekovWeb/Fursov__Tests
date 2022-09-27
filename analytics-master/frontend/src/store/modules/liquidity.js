import API_URL from "@/consts";
import api from "@/api";

export default {
    state: {
        profitTurnover: null,
        profitStocks: null,
        liqStocks: null,
        liqProfit: null,

    },
    getters: {
        PROFIT_TURNOVER(state) {
            return state.profitTurnover
        },
        PROFIT_STOCKS(state) {
            return state.profitStocks
        },
        LIQ_STOCKS(state) {
            return state.liqStocks
        },
        LIQ_PROFIT(state) {
            return state.liqProfit
        },
    },
    mutations: {
        SET_LIQUIDITY_PROFIT_TURNOVER(state, payload) {
            state.profitTurnover = payload
        },
        SET_LIQUIDITY_PROFIT_STOCKS(state, payload) {
            state.profitStocks = payload
        },
        SET_LIQUIDITY_LIQ_STOCKS(state, payload) {
            state.liqStocks = payload
        },
        SET_LIQUIDITY_LIQ_PROFIT(state, payload) {
            state.liqProfit = payload
        }
    },
    actions: {
        GET_LIQUIDITY_PROFIT_TURNOVER(context) {

            return api.get(API_URL + 'analytic/wildberries/liquidity/rent-days')
                .then((response) => {
                    context.commit('SET_LIQUIDITY_PROFIT_TURNOVER', response.data)
                    return response.data
                })
                .catch(
                    error => {
                        console.log(error)
                        return error
                    }
                )
        },
        GET_LIQUIDITY_PROFIT_STOCKS(context) {
            return api.get(API_URL + 'analytic/wildberries/liquidity/rent-remains')
                .then(response => {
                    context.commit('SET_LIQUIDITY_PROFIT_STOCKS', response.data)
                    return response.data
                })
                .catch(
                    error => {
                        console.log(error)
                        return error
                    }
                )
        },
        GET_LIQUIDITY_LIQ_PROFIT(context) {
            return api.get(API_URL + 'analytic/wildberries/liquidity/liquid-remains')
                .then(response => {
                    context.commit('SET_LIQUIDITY_LIQ_STOCKS', response.data)
                    return response.data
                })
                .catch(
                    error => {
                        console.log(error)
                        return error
                    }
                )
        },
        GET_LIQUIDITY_LIQ_STOCKS(context) {
            return api.get(API_URL + 'analytic/wildberries/liquidity/liquid-rent')
                .then(response => {
                    context.commit('SET_LIQUIDITY_LIQ_PROFIT', response.data)
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