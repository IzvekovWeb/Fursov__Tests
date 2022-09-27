import API_URL from "@/consts";
import api from "@/api";

export default {
    state: {
        reports: []
    },
    getters: {
        MAIN_REPORTS(state) {
          return state.reports.filter(item => item.secondary === "False")
        },
        REPORTS (state) {
            return state.reports
        }
    },
    mutations: {
        SET_REPORTS_TO_STATE: (state, reports) =>{
            state.reports = reports
        }
    },
    actions: {
        GET_USER_REPORTS_FROM_API(context) {
            return api.get(API_URL + 'analytic/wildberries')
                .then(reports => {
                    context.commit('SET_REPORTS_TO_STATE', reports.data)
                    return reports.data
                })
        },
    },
}