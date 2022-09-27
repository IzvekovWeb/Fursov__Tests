import {createApp} from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import 'bootstrap/dist/css/bootstrap.min.css'
import 'bootstrap/dist/js/bootstrap.min.js'
import VueApexCharts from "vue3-apexcharts";
import VueCookies from 'vue-cookies'
import VueYandexMetrika from 'vue3-yandex-metrika'

const app = createApp(App);


app.use(VueYandexMetrika, {
    id: 90232871,
    router: router,
    env: process.env.NODE_ENV,
})

app.use(store).use(router).use(VueApexCharts).use(VueCookies).mount('#app');
