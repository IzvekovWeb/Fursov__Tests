<template>
  <main id="main" class="main">
    <section class="section dashboard">
      <div class="pagetitle">
        <div class="col-lg-12 report-head">
          <h1><b>Фирменный отчет MarketData</b></h1>
          <div class="head-buttons" v-if="!toolLoading">
            <a :href="createSheetLink(reportInfo.spreadsheet_id, reportInfo.sheet_id)"
               target="_blank" class="btn btn-primary">Таблица</a>
            <i class="bi bi-x-circle reload-btn" style="color: red; cursor: pointer; font-size: 1.5rem" v-if="refreshError" :title="refreshErrorText"></i>
            <i class="bi bi-check-circle reload-btn" v-else-if="refreshSuccess"></i>
            <div class="spinner-border text-primary reload-btn-circle" role="status" v-else-if="refresh"></div>
            <a href="javascript://" class="reload-btn" v-else @click="refreshReport(reportInfo.id)"><i
                class="bi bi-arrow-clockwise reload-icon"></i></a> </div>
        </div>
      </div>
      <div  v-if="!loading" class="col-lg-8">
        <div class="row">

          <div class="col-lg-6">
            <!-- Топ категорий -->
            <div class="card">
              <div class="card-body pb-0">
                <h5 class="card-title">Категорийная оборачиваемость</h5>
                <BarChart :labels="PROFIT_TURNOVER.data" :data="PROFIT_TURNOVER.values"/>
              </div>
            </div>
          </div>
          <div class="col-lg-6">
            <!-- Топ категорий -->
            <div class="card">
              <div class="card-body pb-0">
                <h5 class="card-title">Структура остатков категорий рентабельности</h5>
                <BarChart :labels="PROFIT_STOCKS.data" :data="PROFIT_STOCKS.values"/>
              </div>
            </div>
          </div>


        </div>
        <div class="row">

          <div class="col-lg-6">
            <!-- Топ категорий -->
            <div class="card">
              <div class="card-body pb-0">
                <h5 class="card-title">Структура остатков категорий ликвидности</h5>
                <BarChart :labels="LIQ_PROFIT.data" :data="LIQ_PROFIT.values"/>
              </div>
            </div>
          </div>

          <div class="col-lg-6">
            <!-- Топ категорий -->
            <div class="card">
              <div class="card-body pb-0">
                <h5 class="card-title">Рентабельность категорий ликвидности</h5>
                <BarChart :labels="LIQ_STOCKS.data" :data="LIQ_STOCKS.values"/>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  </main>
</template>

<script>
import BarChart from "@/components/charts/BarChart";
import {mapGetters} from "vuex";
import baseMixin from "@/mixins/baseMixin";
import reportMixin from "@/mixins/reportMixin";
export default {
  name: "Liquidity",
  components: {
    BarChart
  },
  data: () => ({
    slug: 'liquidity'
  }),
  mixins: [baseMixin, reportMixin],
  computed: mapGetters(['LIQ_STOCKS', 'LIQ_PROFIT', 'PROFIT_STOCKS', 'PROFIT_TURNOVER']),
  async mounted() {
    this.reportInfo = await this.getReportInfo(this.slug)
    this.toolLoading = false
    await this.$store.dispatch('GET_LIQUIDITY_PROFIT_TURNOVER')
    await this.$store.dispatch('GET_LIQUIDITY_LIQ_PROFIT')
    await this.$store.dispatch('GET_LIQUIDITY_LIQ_STOCKS')
    await this.$store.dispatch('GET_LIQUIDITY_PROFIT_STOCKS')
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
</style>