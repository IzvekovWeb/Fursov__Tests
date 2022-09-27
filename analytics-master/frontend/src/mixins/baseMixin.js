import moment from "moment/moment";

export default {
    methods: {
        getNumWithSpaces(x) {
            if (x === null || x === undefined) return '-'
            if (x > 1000000) {
                let s = x / 1000000
                return s.toFixed(1).toString() + 'млн'
            }
            let parts = x.toString().split(".");
            parts[0] = parts[0].replace(/\B(?=(\d{3})+(?!\d))/g, " ");
            return parts.join(".");
        },
        getDates() {
            var dates = []
            for (let i = 7; i > 0; i--) {
                dates.push(moment().subtract(i, 'days').format('YYYY-MM-DD'))
            }
            return dates
        },
        createSheetLink(table, sheet) {
            return 'https://docs.google.com/spreadsheets/d/' + table + '/edit#gid=' + sheet
        },
    },
    data: () => ({
        loading: true,
        errored: false
    })
}

