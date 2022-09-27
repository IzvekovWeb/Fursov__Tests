<template>
  <main id="main" class="main">
    <section class="section dashboard">
      <div class="pagetitle">
        <div class="col-lg-12 report-head">
          <h1><b>Отчет "Рентабельность"</b></h1>
          <div class="head-buttons" v-if="!toolLoading">
            <a :href="createSheetLink(reportInfo.spreadsheet_id, reportInfo.sheet_id)"
               target="_blank" class="btn btn-primary" style="margin: 0 20px">Таблица</a>
            <a :href="createSheetLink(pricesReportInfo.spreadsheet_id, pricesReportInfo.sheet_id)"
               target="_blank" class="btn btn-primary">Себестоимость</a>
            <i class="bi bi-x-circle reload-btn" style="color: red; cursor: pointer; font-size: 1.5rem"
               v-if="refreshError" :title="refreshErrorText"></i>
            <i class="bi bi-check-circle reload-btn" v-else-if="refreshSuccess"></i>
            <div class="spinner-border text-primary reload-btn-circle" role="status" v-else-if="refresh"></div>
            <a href="javascript://" class="reload-btn" v-else @click="refreshReport(reportInfo.id)"><i
                class="bi bi-arrow-clockwise reload-icon"></i></a>
          </div>
        </div>
      </div>
      <div class="row" v-if="!loading">

        <!-- Левая колонка -->
        <div class="col-lg-8">
          <div class="row">

            <!-- ЧП -->
            <div class="col-xxl-4 col-md-6">
              <div class="card info-card sales-card">
                <!--                <DropdownFilter/>-->
                <div class="card-body">
                  <h5 class="card-title">Операционная прибыль</h5>

                  <div class="d-flex align-items-center">
                    <div class="card-icon rounded-circle d-flex align-items-center justify-content-center">
                      <i class="bi bi-cart"></i>
                    </div> <!-- Картинка -->
                    <div class="ps-3">
                      <h6>{{ getNumWithSpaces(PROFITABILITY_STATISTICS.op) }}</h6>
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
                  <h5 class="card-title">Прибыль на шт <span>| Среднее</span></h5>
                  <div class="d-flex align-items-center">
                    <div class="card-icon rounded-circle d-flex align-items-center justify-content-center">
                      <i class="bi bi-bandaid"></i>
                    </div>
                    <div class="ps-3">
                      <h6>{{ getNumWithSpaces(PROFITABILITY_STATISTICS.average_profit) }}</h6>
                    </div>
                  </div>
                </div>
              </div>
            </div>
            <!-- Доля неликвида -->
            <div class="col-xxl-4 col-xl-12">
              <div class="card info-card customers-card">
                <div class="card-body">
                  <h5 class="card-title">Себестоимость &#8381;</h5>
                  <div class="d-flex align-items-center">
                    <div class="card-icon rounded-circle d-flex align-items-center justify-content-center">
                      <i class="bi bi-people"></i>
                    </div>
                    <div class="ps-3">
                      <h6>{{ getNumWithSpaces(PROFITABILITY_STATISTICS.prime_cost) }}</h6>
                    </div>
                  </div>

                </div>
              </div>

            </div>

          </div>

          <div class="col-12">
            <div class="card">
              <!-- График -->
              <div class="card-body">
                <h5 class="card-title">Лучшие товары по рентабельности</h5>
                <ProfitabilityDynamicChart class="dynamic" :series="PROFITABILITY_TOP.data"
                                           :labels="PROFITABILITY_TOP.name"/>
              </div>
            </div>
          </div>
          <!-- Динамика -->
          <div class="col-12">
            <div class="card">
              <!-- График -->
              <div class="card-body">
                <h5 class="card-title">Худшие товары по рентабельности</h5>
                <ProfitabilityDynamicChart class="dynamic" :series="PROFITABILITY_WORST.data"
                                           :labels="PROFITABILITY_WORST.name"/>
              </div>
            </div>
          </div>
        </div>

        <!-- Правая колонка -->
        <div class="col-lg-4">

          <div class="card">
            <div class="card-body pb-0" style="margin-bottom: 22px;">
              <h5 class="card-title">Затраты &#8381;</h5>
              <div class="d-flex align-items-center goto">
                <div class="ps-3" style="margin-right: 25px">
                  <h6 class="super">{{ getNumWithSpaces(PROFITABILITY_STATISTICS.storage) }}</h6>
                  <span class="text-muted small pt-1">Хранение (склад ВБ)</span>
                </div>
                <div class="ps-3">
                  <h6 class="super">{{ getNumWithSpaces(PROFITABILITY_STATISTICS.logistics) }}</h6>
                  <span class="text-muted small pt-1">Логистика</span>
                </div>
              </div>
            </div>
          </div>

        </div>

      </div>
    </section>
  </main>
</template>

<script>
import ProfitabilityDynamicChart from "@/components/charts/ProfitabilityDynamicChart";
import BarChart from "@/components/charts/BarChart";
import {mapGetters} from "vuex";
import baseMixin from "@/mixins/baseMixin";
import reportMixin from "@/mixins/reportMixin";

export default {

  name: "ProfitabilityReport",
  components: {ProfitabilityDynamicChart, BarChart},
  mixins: [baseMixin, reportMixin],
  computed: mapGetters(['PROFITABILITY_WORST', 'PROFITABILITY_TOP', 'PROFITABILITY_STATISTICS']),
  data: () => ({
    pricesReportInfo: null,
    slug: 'profitability'
  }),
  async mounted() {
    this.reportInfo = await this.getReportInfo(this.slug)
    this.pricesReportInfo = await this.getReportInfo('prime-cost')
    this.toolLoading = false
    await this.$store.dispatch('GET_PROFITABILITY_WORST')
    await this.$store.dispatch('GET_PROFITABILITY_TOP')
    await this.$store.dispatch('GET_PROFITABILITY_STATISTICS')
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

.goto {
  justify-content: flex-start;
}

.ps-3 .super {
  font-size: 32px;
  font-weight: bold;
  margin-bottom: 0;
  color: #012970;
}

</style>