<template>
  <main id="main" class="main">
    <section class="section dashboard">
      <div class="pagetitle">
        <div class="col-lg-8 report-head">
          <h1><b>Динамика поартикульно</b></h1>
          <div class="head-buttons" v-if="!toolLoading">
            <a :href="createSheetLink(reportInfo.spreadsheet_id, reportInfo.sheet_id)"
               target="_blank" class="btn btn-primary">Таблица</a>
            <i class="bi bi-x-circle reload-btn" style="color: red; cursor: pointer; font-size: 1.5rem" v-if="refreshError" :title="refreshErrorText"></i>
            <i class="bi bi-check-circle reload-btn" v-else-if="refreshSuccess"></i>
            <div class="spinner-border text-primary reload-btn-circle" role="status" v-else-if="refresh"></div>
            <a href="javascript://" class="reload-btn" v-else @click="refreshReport(reportInfo.id)"><i class="bi bi-arrow-clockwise reload-icon"></i></a>
          </div>
        </div>
      </div>
      <div class="row"  v-if="!loading">

        <!-- Левая колонка -->
        <div class="col-lg-8">
          <div class="row">

            <!-- ЧП -->
            <div class="col-xxl-4 col-md-6">
              <div class="card info-card sales-card">
                <!--                <DropdownFilter/>-->
                <div class="card-body">
                  <h5 class="card-title">Заказано шт <span>| Неделя</span></h5>

                  <div class="d-flex align-items-center">
                    <div class="card-icon rounded-circle d-flex align-items-center justify-content-center">
                      <i class="bi bi-cart"></i>
                    </div> <!-- Картинка -->
                    <div class="ps-3">
                      <h6>{{ getNumWithSpaces(DYNAMIC_STATISTICS.orders_count) }}</h6>
                    </div> <!-- Значение и прирост -->
                  </div>
                </div>
              </div>
            </div>
            <!-- Доля неликвида -->
            <div class="col-xxl-4 col-md-6">
              <div class="card info-card revenue-card">
                <!--                <DropdownFilter/>-->
                <div class="card-body">
                  <h5 class="card-title">Заказано руб <span>| Неделя</span></h5>
                  <div class="d-flex align-items-center">
                    <div class="card-icon rounded-circle d-flex align-items-center justify-content-center">
                      <i class="bi bi-bandaid"></i>
                    </div>
                    <div class="ps-3">
                      <h6>{{ getNumWithSpaces(DYNAMIC_STATISTICS.orders_rub) }}</h6>
                    </div>
                  </div>
                </div>
              </div>
            </div>
            <!-- Оборачиваемость -->
            <div class="col-xxl-4 col-xl-12">
              <div class="card info-card customers-card">

                <div class="card-body">
                  <h5 class="card-title">Товаров</h5>

                  <div class="d-flex align-items-center">
                    <div class="card-icon rounded-circle d-flex align-items-center justify-content-center">
                      <i class="bi bi-people"></i>
                    </div>
                    <div class="ps-3">
                      <h6>{{ getNumWithSpaces(DYNAMIC_STATISTICS.orders_rows) }} шт.</h6>
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
                  <h5 class="card-title">Динамика заказов</h5>
                  <DynamicChart :series="DASHBOARD_ORDERS_DYNAMIC" :labels="getDates()"/>
                </div>
              </div>
            </div>

          </div>
        </div>
        <!-- Правая колонка -->
        <div class="col-lg-4">
          <div class="card info-card revenue-card-art">
            <!--                <DropdownFilter/>-->
            <div class="card-body">
              <h5 class="card-title">Товаров <span>| Без заказов</span></h5>
              <div class="d-flex align-items-center">
                <div class="card-icon rounded-circle d-flex align-items-center justify-content-center">
                  <i class="bi bi-x-circle"></i>
                </div>
                <div class="ps-3">
                  <h6>{{ getNumWithSpaces(DYNAMIC_STATISTICS.orders_zero) }} шт.</h6>
                </div>
              </div>
            </div>
          </div>
          <div class="card">
            <div class="card-body pb-0">
              <h5 class="card-title">Заказы<span> | Неделя</span></h5>
              <OrdersByDays :days="DYNAMIC_WEEK_DYNAMIC"/>
            </div>
          </div>
        </div>
      </div>
      <div>Loading...</div>
    </section>
  </main>
</template>

<script>
import DynamicChart from "@/components/charts/DynamicChart";
import OrdersByDays from "@/components/tables/OrdersByDays";

import {mapGetters} from "vuex";
import baseMixin from "@/mixins/baseMixin";
import reportMixin from "@/mixins/reportMixin";

export default {
  name: "DynamicReport",
  components: {
    OrdersByDays,
    DynamicChart
  },
  data: () => ({
    slug: 'dynamic-art-count'
  }),
  computed: mapGetters(['DYNAMIC_WEEK_DYNAMIC', 'DYNAMIC_STATISTICS', 'DASHBOARD_ORDERS_DYNAMIC']),
  mixins: [baseMixin, reportMixin],
  async mounted() {
    this.reportInfo = await this.getReportInfo(this.slug)
    this.toolLoading = false
    await this.$store.dispatch('GET_DASHBOARD_ORDERS_DYNAMIC')
    await this.$store.dispatch('GET_DYNAMIC_WEEK_DYNAMIC')
    await this.$store.dispatch('GET_DYNAMIC_STATISTIC')
    this.loading = false
  },
}
</script>

<style scoped>
.bi-check-circle {
  color: #56b458;
  font-size: 1.5rem;
}


.pagetitle {
  margin-bottom: 25px;
}

.report-head {
  display: flex;
  width: 100%;
  align-items: center;
  justify-content: space-between;
}

.head-buttons {
  display: flex;
  align-items: center;
  align-self: flex-end;
}

.reload-icon {
  margin-left: 25px;
  margin-right: 5px;
  font-size: 2rem;
}

.spinner-border {
  margin-left: 25px;
  margin-right: 5px;
}
</style>