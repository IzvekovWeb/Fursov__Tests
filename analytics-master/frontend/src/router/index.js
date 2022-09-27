import {createRouter, createWebHistory} from 'vue-router'

const routes = [
    {
        path: '/',
        name: 'home',
        meta: {layout: 'main'},
        component: () => import('@/views/HomeView')
    },
    {
        path: '/login',
        name: 'login',
        meta: {layout: 'login'},
        component: () => import('@/views/LoginView')
    },
    {
        path: '/register',
        name: 'register',
        meta: {layout: 'login'},
        component: () => import('@/views/RegisterView')
    },
    {
        path: '/analytic/selfsell',
        name: 'selfsell',
        meta: {layout: 'main'},
        component: () => import('@/views/SelfsellView')
    },
    {
        path: '/profile',
        name: 'profile',
        meta: {layout: 'main'},
        component: () => import('@/views/ProfileView.vue')
    },
    {
        path: '/analytic/wildberries',
        name: 'wildberries',
        meta: {layout: 'main'},
        component: () => import('@/views/ReportsView.vue')
    },
    {
        path: '/contacts',
        name: 'contacts',
        meta: {layout: 'main'},
        component: () => import('@/views/ContactsView.vue')
    },
    {
        path: '/favorite',
        name: 'favorite',
        meta: {layout: 'main'},
        component: () => import('@/views/FavoriteView.vue')
    },
    {
        path: '/faq',
        name: 'faq',
        meta: {layout: 'main'},
        component: () => import('@/views/FAQView.vue')
    },
    {
        path: '/rules',
        name: 'rules',
        meta: {layout: 'login'},
        component: () => import('@/views/RulesView.vue')
    },
    {
        path: '/tariffs',
        name: 'tariffs',
        meta: {layout: 'main'},
        component: () => import('@/views/TariffsView.vue')
    },
    {
        path: '/analytic/wildberries/orders-categories',
        name: 'wb-dynamic-category',
        meta: {layout: 'main'},
        component: () => import('@/views/reports/DynamicCategory.vue')
    },
    {
        path: '/analytic/wildberries/dynamic-art-count',
        name: 'wb-dynamic',
        meta: {layout: 'main'},
        component: () => import('@/views/reports/DynamicReport.vue')
    },
    {
        path: '/analytic/wildberries/week',
        name: 'wb-weekly',
        meta: {layout: 'main'},
        component: () => import('@/views/reports/WeeklyReport.vue')
    },
    {
        path: '/analytic/wildberries/profitability',
        name: 'wb-profitability',
        meta: {layout: 'main'},
        component: () => import('@/views/reports/ProfitabilityReport.vue')
    },
    {
        path: '/analytic/wildberries/month',
        name: 'month',
        meta: {layout: 'main'},
        component: () => import('@/views/reports/MonthlyReport.vue')
    },
    {
        path: '/analytic/wildberries/abc',
        name: 'abc',
        meta: {layout: 'main'},
        component: () => import('@/views/reports/ABCReport.vue')
    },
    {
        path: '/analytic/wildberries/liquidity',
        name: 'wb-monthly',
        meta: {layout: 'main'},
        component: () => import('@/views/reports/LiquidityReport.vue')
    },
    {
        path: '/logout',
        name: 'logout',
        meta: {layout: 'login'},
        component: () => import('@/views/AuthView.vue')
    },

]

const router = createRouter({
    history: createWebHistory(process.env.BASE_URL),
    routes
})

export default router

router.beforeEach((to, from, next) => {
    const publicPages = ['/register', '/login', '/rules',];
    const authRequired = !publicPages.includes(to.path);
    const loggedIn = localStorage.getItem('access');

    if (loggedIn && (to.path === '/login' || to.path === '/register')) {
        next('/')
    } else if (authRequired && !loggedIn && to.path !== '/register') {
        next('/login');
    } else {
        next();
    }
});