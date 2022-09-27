import router from "@/router";
import API_URL from "@/consts";
import axios from "axios";
import api from "@/api";

function getCookie(name) {
    let matches = document.cookie.match(new RegExp(
        "(?:^|; )" + name.replace(/([\.$?*|{}\(\)\[\]\\\/\+^])/g, '\\$1') + "=([^;]*)"
    ));
    return matches ? decodeURIComponent(matches[1]) : undefined;
}

function clearCookie(name){
    document.cookie = name +'=; Path=/; Expires=Thu, 01 Jan 1970 00:00:01 GMT;';
}

function setCookie(name, value, options = {}) {

    options = {
        path: '/',
        ...options
    };

    if (options.expires instanceof Date) {
        options.expires = options.expires.toUTCString();
    }

    let updatedCookie = encodeURIComponent(name) + "=" + encodeURIComponent(value);

    for (let optionKey in options) {
        updatedCookie += "; " + optionKey;
        let optionValue = options[optionKey];
        if (optionValue !== true) {
            updatedCookie += "=" + optionValue;
        }
    }

    document.cookie = updatedCookie;
}

class AuthService {

    login(user) {
        return axios
            .post(API_URL + 'login', user)
            .then(response => {
                localStorage.setItem('access', JSON.stringify(response.data.access));
                setCookie('refresh', response.data.refresh)
            });
    }

    logout() {
        localStorage.removeItem('access')
        clearCookie('refresh')
        router.go(0)
    }

    refreshToken() {
        let refreshToken = getCookie('refresh')
        if (!refreshToken) return this.logout()
        return api
            .post(API_URL + 'token/refresh', {refresh: refreshToken}, {headers: {

                }})
            .then(response => {
                localStorage.setItem('access', JSON.stringify(response.data.access));
                setCookie('refresh', response.data.refresh)
            })
    }

    register(user) {
        return axios
            .post(API_URL + 'register', user)
            .then(res => res)
    }
}

export default new AuthService();