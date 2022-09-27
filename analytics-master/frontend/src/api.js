import axios from "axios";
import authService from "@/services/auth.service";
import API_URL from "@/consts";

const axios_custom = axios.create()

axios_custom.interceptors.request.use(config => {
    config.timeout = 900000
    const token = JSON.parse(localStorage.getItem('access'))
    if (token) {
        config.headers['Authorization'] = 'Bearer ' + token
    } else {
        authService.logout()
    }
    return config
})

axios_custom.interceptors.response.use(
    (res) => {
        return res;
    },
    async (err) => {
        const originalConfig = err.config;
        if (originalConfig.url !== API_URL + "login" && originalConfig.url !== API_URL + "register" && err.response) {
            if (originalConfig.url === API_URL + "token/refresh") return authService.logout()
            if (err.response.status === 401 && !originalConfig._retry) {
                originalConfig._retry = true;
                try {
                    await authService.refreshToken()
                    return axios_custom(originalConfig);
                } catch (_error) {
                    return Promise.reject(_error);
                }
            }
        }
        return Promise.reject(err);
    }
)
export default axios_custom
