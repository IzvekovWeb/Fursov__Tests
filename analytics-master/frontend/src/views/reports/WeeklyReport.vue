<template>
  <main id="main" class="main">
    <section class="section dashboard">
      <div class="pagetitle">
        <div class="col-lg-12 report-head">
          <h1><b>Отчет "Неделя"</b></h1>
          <div class="head-buttons" v-if="!toolLoading">
            <a :href="createSheetLink(reportInfo.spreadsheet_id, reportInfo.sheet_id)"
               target="_blank" class="btn btn-primary">Таблица</a>
            <plan-modal v-model:show="dialogVisibility" url="analytic/wildberries/week-plan-update"/>
            <button class="btn btn-primary" @click="showDialog">Ввести план</button>
            <i class="bi bi-x-circle reload-btn" style="color: red; cursor: pointer; font-size: 1.5rem" v-if="refreshError" :title="refreshErrorText"></i>
            <i class="bi bi-check-circle reload-btn" v-else-if="refreshSuccess"></i>
            <div class="spinner-border text-primary reload-btn-circle" role="status" v-else-if="refresh"></div>
            <a href="javascript://" class="reload-btn" v-else @click="refreshReport(reportInfo.id)"><i class="bi bi-arrow-clockwise reload-icon"></i></a>
            </div>
          </div>
        </div>
      <div v-if="!loading" class="row">

        <!-- Левая колонка -->
        <div class="col-lg-12">
          <div class="row">

            <!-- ЧП -->
            <div class="col-xxl-3 col-md-6">
              <div class="card info-card sales-card">
                <div class="card-body">
                  <h5 class="card-title">Заказы <span>| Факт (% плана) </span></h5>
                  <div class="d-flex align-items-center">
                    <div class="card-icon rounded-circle d-flex align-items-center justify-content-center">
                      <i class="bi bi-cart"></i>
                    </div> <!-- Картинка -->
                    <div class="ps-3">
                      <h6>{{ getNumWithSpaces(WEEKLY_ORDERS.orders_count) }}</h6>
                      <span class="text-muted small pt-1">{{ WEEKLY_ORDERS.percent_fact }}% от плана</span>
                    </div> <!-- Значение и прирост -->
                  </div>
                </div>
              </div>
            </div>
            <!-- Доля неликвида -->
            <div class="col-xxl-6 col-md-6">
              <div class="card info-card revenue-card">
                <!--                <DropdownFilter/>-->
                <div class="card-body">
                  <div class="goto-header">
                    <h5 class="card-title">Идем на <span>| К чему придем к концу недели </span></h5>

                  </div>
                  <div class="d-flex align-items-center goto">
                    <div class="ps-3">
                      <h5 class="super">{{ getNumWithSpaces(WEEKLY_GOTO.orders_rub) }}</h5>
                      <span class="text-muted small pt-1">Заказы руб</span>
                    </div>
                    <div class="ps-3">
                      <h5 class="super">{{ getNumWithSpaces(WEEKLY_GOTO.sold) }}</h5>
                      <span class="text-muted small pt-1">Продажи руб</span>
                    </div>
                    <div class="ps-3">
                      <h5 class="super">{{ getNumWithSpaces(WEEKLY_GOTO.logistic) }}</h5>
                      <span class="text-muted small pt-1">Логистика руб</span>
                    </div>
                    <div class="ps-3">
                      <h5 class="super">{{ getNumWithSpaces(WEEKLY_GOTO.realize) }}</h5>
                      <span class="text-muted small pt-1">К перечислению</span>
                    </div>
                  </div>
                </div>
              </div>
            </div>
            <!-- Оборачиваемость -->
            <div class="col-xxl-3 col-md-6">
              <div class="card info-card sales-card">
                <div class="card-body">
                  <h5 class="card-title">Продажи <span>| Факт (% плана) </span></h5>
                  <div class="d-flex align-items-center">
                    <div class="card-icon rounded-circle d-flex align-items-center justify-content-center">
                      <i class="bi bi-cart"></i>
                    </div> <!-- Картинка -->
                    <div class="ps-3">
                      <h6>{{ getNumWithSpaces(WEEKLY_SOLD.sold_count) }}</h6>
                      <span class="text-muted small pt-1">{{ WEEKLY_SOLD.percent_fact }}% от плана</span>
                    </div> <!-- Значение и прирост -->
                  </div>
                </div>
              </div>
            </div>

          </div>
          <div class="row">

            <!-- Динамика -->
            <div class="col-9 graph">
              <div class="card">
                <!-- График -->
                <div class="card-body">
                  <h5 class="card-title">Заказы/Продажи за неделю</h5>
                  <DynamicChart class="dynamic" :series="dynamicOrders.data" :labels="dynamicOrders.dates"
                                :height="150"/>
                </div>
              </div>
            </div>
          </div>
        </div>


      </div>
      <div v-else>Loading...</div>
    </section>
  </main>
</template>

<script>
import DynamicChart from "@/components/charts/DynamicChart";
import planModal from "@/components/UI/PlanModal";
import {mapActions, mapGetters} from "vuex";
import baseMixin from "@/mixins/baseMixin";
import reportMixin from "@/mixins/reportMixin";

export default {
  name: "WeeklyReport",
  components: {
    DynamicChart, planModal
  },
  computed: {
    dynamicOrders() {
      // if (this.WEEKLY_DYNAMIC().length){
      //   let dates = this.WEEKLY_DYNAMIC()[0].dates
      //   let ordersData = this.WEEKLY_DYNAMIC()[0].orders_dat
      //   let soldData = this.WEEKLY_DYNAMIC()[0].sold_data
      // } else {
      //   let dates = this.WEEKLY_DYNAMIC()[0].dates
      //   let ordersData = this.WEEKLY_DYNAMIC()[0].orders_dat
      //   let soldData = this.WEEKLY_DYNAMIC()[0].sold_data
      // }
      return {
        dates: this.WEEKLY_DYNAMIC().dates,
        data: [{
          name: 'Заказы',
          data: this.WEEKLY_DYNAMIC().orders_data,
        }, {
          name: 'Продажи',
          data: this.WEEKLY_DYNAMIC().sold_data,
        }]
      }
    },
    ...mapGetters(['WEEKLY_GOTO', 'WEEKLY_SOLD', 'WEEKLY_ORDERS'])
  },
  data: () => ({
    dialogVisibility: false,
    slug: 'week'
  }),
  mixins: [baseMixin, reportMixin],
  methods: {
    ...mapActions(['GET_WEEKLY_DYNAMIC', 'GET_WEEKLY_ORDERS', 'GET_WEEKLY_SOLD', 'GET_WEEKLY_GOTO']),
    ...mapGetters(['WEEKLY_DYNAMIC', 'WEEKLY_GOTO', 'WEEKLY_SOLD', 'WEEKLY_ORDERS']),
    showDialog() {
      this.dialogVisibility = true
    },

  },
  async mounted() {
    this.reportInfo = await this.getReportInfo(this.slug)
    this.toolLoading = false
    await this.$store.dispatch('GET_WEEKLY_DYNAMIC')
    await this.$store.dispatch('GET_WEEKLY_ORDERS')
    await this.$store.dispatch('GET_WEEKLY_SOLD')
    await this.$store.dispatch('GET_WEEKLY_GOTO')
    this.loading = false
  }
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

/*.prices {*/
/*  margin-left: auto;*/
/*  margin-right: 20px;*/
/*  bottom: 0;*/
/*}*/

/*.reload-icon {*/
/*  margin-left: 25px;*/
/*  margin-right: 5px;*/
/*  font-size: 2rem;*/
/*}*/

/*.spinner-border {*/
/*  margin-left: 25px;*/
/*  margin-right: 5px;*/
/*}*/

.btn-primary {
  margin-right: 25px;
}

.goto {
  justify-content: space-between;
}

.super {
  font-weight: bold;
}
</style>