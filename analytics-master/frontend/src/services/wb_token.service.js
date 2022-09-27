import API_URL from "@/consts";
import api from "@/api";

class WBTokenService {

    async checkWBAuthToken() {
        return !(await api.get(API_URL + 'check-wb-auth-token')).data
    }
    editToken(payload){
        return api.put(API_URL + 'wb-tokens', {data: payload})
    }
}

export default new WBTokenService();