import axios_custom from "@/api";
import API_URL from "@/consts";

export default {
    methods: {
        async getReportInfo(slug){
            let data = await axios_custom.get(API_URL + 'analytic/wildberries/' + slug)
            return data.data
        },
        async refreshReport(report_id){
            this.refresh = true
            return await axios_custom
                .put(API_URL + 'analytic/wildberries/refresh/' + report_id, {})
                .then(response => {
                    this.refresh = false
                    this.refreshSuccess = true
                })
                .catch(error => {
                    this.refresh = false
                    this.refreshError = true
                    this.refreshErrorText = error
                });
        }
    },
    data: () => ({
        refresh: false,
        refreshError: false,
        refreshSuccess: false,
        refreshErrorText: '',
        reportInfo: {},
        toolLoading: true
    })
}


