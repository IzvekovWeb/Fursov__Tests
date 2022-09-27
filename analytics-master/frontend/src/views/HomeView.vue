<template>
  <main id="main" class="main">
    <section class="section dashboard" v-if="!loading">
      <div class="row">
        <!-- Левая колонка -->
        <div class="col-lg-8">
          <div class="row">

            <!-- Заказы (шт) -->
            <div class="col-xxl-4 col-md-6">
              <div class="card info-card sales-card">
                <div class="card-body">
                  <h5 class="card-title">Заказы <span>| Неделя </span></h5>
                  <div class="d-flex align-items-center">
                    <div class="card-icon rounded-circle d-flex align-items-center justify-content-center">
                      <i class="bi bi-cart"></i>
                    </div> <!-- Картинка -->
                    <div class="ps-3">
                      <h6>{{ getNumWithSpaces(DASHBOARD_STATISTICS.orders_amount) }}</h6>
                      <span class="text-muted small pt-1">{{ DASHBOARD_STATISTICS.increase_amount }}%</span>
                      <span class="text-success small pt-2 ps-1" v-if="DASHBOARD_STATISTICS.increase_amount > 0">прирост</span>
                      <span class="text-danger small pt-2 ps-1" v-else>спад</span>
                    </div> <!-- Значение и прирост -->
                  </div>
                </div>
              </div>
            </div>
            <!-- Заказы (руб) -->
            <div class="col-xxl-4 col-md-6">
              <div class="card info-card revenue-card">
                <div class="card-body">
                  <h5 class="card-title">Заказы &#8381; <span>| Неделя</span></h5>
                  <div class="d-flex align-items-center">
                    <div class="card-icon rounded-circle d-flex align-items-center justify-content-center">
                      <i class="bi bi-cash"></i>
                    </div>
                    <div class="ps-3">
                      <h6>{{ getNumWithSpaces(DASHBOARD_STATISTICS.orders_rub) }}</h6>
                      <span class="text-muted small pt-1">{{ DASHBOARD_STATISTICS.increase_rub }}%</span>
                      <span class="text-success small pt-2 ps-1"
                            v-if="DASHBOARD_STATISTICS.increase_rub> 0">прирост</span>
                      <span class="text-danger small pt-2 ps-1" v-else>спад</span>
                    </div>
                  </div>
                </div>
              </div>
            </div>
            <!-- Покупки -->
            <div class="col-xxl-4 col-xl-12">
              <div class="card info-card customers-card">
                <div class="card-body">
                  <h5 class="card-title">Продажи &#8381; <span>| Неделя</span></h5>
                  <div class="d-flex align-items-center">
                    <div class="card-icon rounded-circle d-flex align-items-center justify-content-center">
                      <i class="bi bi-people"></i>
                    </div>
                    <div class="ps-3">
                      <h6>{{ getNumWithSpaces(DASHBOARD_STATISTICS.orders_sells) }}</h6>
                      <span class="text-muted small pt-1">{{ DASHBOARD_STATISTICS.increase_sells }}%</span>
                      <span class="text-success small pt-2 ps-1" v-if="DASHBOARD_STATISTICS.increase_sells > 0">прирост</span>
                      <span class="text-danger small pt-2 ps-1" v-else>спад</span>
                    </div>
                  </div>

                </div>
              </div>

            </div>

            <!-- Динамика -->
            <div class="col-12">
              <div class="card">
                <!-- График -->
                <div class="card-body">
                  <h5 class="card-title">Динамика <span>| Неделя</span></h5>
                  <DashboardChart :series="DASHBOARD_ORDERS_DYNAMIC" :labels="getDates()"/>
                </div>
              </div>
            </div>

            <!-- Топ заказов -->
            <div class="col-12">
              <div class="card top-selling overflow-auto">
                <div class="card-body pb-0">
                  <h5 class="card-title">Топ заказов <span>| Неделя</span></h5>
                  <TopOrdersTable :articles="DASHBOARD_TOP_ORDERS"/>
                </div>
              </div>
            </div>
          </div>
        </div>
        <!-- Правая колонка -->
        <div class="col-lg-4">

          <!-- Топ категорий -->
          <div class="card" style="margin-bottom: 25px">
            <div class="card-body pb-0" style="margin-bottom: 25px">
              <h5 class="card-title">Топ категорий <span>| Неделя</span></h5>
              <DashboardTopCategories :series="DASHBOARD_TOP_CATEGORIES.orders_rub"
                                      :labels="DASHBOARD_TOP_CATEGORIES.category"/>
            </div>
          </div>
          <div class="card">
            <div class="card-body pb-0">
              <h5 class="card-title">Топ бренды <span>| Неделя</span></h5>
              <TopBrandsTable :brands="DASHBOARD_TOP_BRANDS"/>
            </div>
          </div>
        </div>
      </div>

    </section>
    <div class="spinner-border text-primary circle" role="status" v-else>
      <span class="visually-hidden">Loading...</span>
    </div>
  </main>
</template>

<script>
import TopOrdersTable from "@/components/tables/TopOrdersTable";
import DashboardChart from "@/components/charts/DynamicChart";
import DashboardTopCategories from "@/components/charts/TopDonutChart";
import TopBrandsTable from "@/components/tables/TopBrandsTable";
import {mapGetters} from 'vuex';
import baseMixin from "@/mixins/baseMixin";
import NumberModal from "@/components/UI/NumberModal";

export default {
  name: 'HomeView',
  data: () => ({
    dialogVisibility: true
  }),
  components: {
    NumberModal,
    DashboardChart,
    TopOrdersTable,
    DashboardTopCategories,
    TopBrandsTable
  },
  computed: mapGetters(['DASHBOARD_STATISTICS', "DASHBOARD_TOP_CATEGORIES", "DASHBOARD_ORDERS_DYNAMIC", "DASHBOARD_TOP_BRANDS", "DASHBOARD_TOP_ORDERS"]),
  mixins: [baseMixin],
  async mounted() {
      await this.$store.dispatch('GET_DASHBOARD_STATISTICS')
      await this.$store.dispatch('GET_DASHBOARD_TOP_ORDERS')
      await this.$store.dispatch('GET_DASHBOARD_TOP_CATEGORIES')
      await this.$store.dispatch('GET_DASHBOARD_TOP_BRANDS')
      await this.$store.dispatch('GET_DASHBOARD_ORDERS_DYNAMIC')
      this.loading = false
  }
}
</script>

<style>

.card {
  border: none;
}
</style>