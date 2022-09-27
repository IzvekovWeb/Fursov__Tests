import API_URL from "@/consts";
import api from "@/api";

class SelfsellService {

    selfsell(payload) {
        return api
            .post(API_URL + 'selfsell', payload)
            .then(response => {
                return response.data
            });
    }
}

export default new SelfsellService();