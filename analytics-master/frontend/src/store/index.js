import { createStore } from 'vuex';
import reports from "@/store/modules/reports";
import dashboard from "@/store/modules/dashboard";
import user from '@/store/modules/user';
import weekly from '@/store/modules/weekly';
import monthly from "@/store/modules/monthly";
import categories from "@/store/modules/categories";
import profitability from "@/store/modules/profitability";
import dynamic from "@/store/modules/dynamic";
import liquidity from "@/store/modules/liquidity";
import abc from "@/store/modules/abc";
import selfsell from "@/store/modules/selfsell";

export default createStore({
  modules: {
    reports, dashboard, user, weekly, monthly, categories, profitability, dynamic, liquidity, abc, selfsell
  }
})