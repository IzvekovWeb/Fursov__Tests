<template>
  <main id="main" class="main">
    <section class="section dashboard">
      <div class="pagetitle">
        <div class="col-lg-8 report-head">
          <h1><b>ABC анализ</b></h1>
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
      <div  v-if="!loading">
        <div class="row">
          <!-- Левая колонка -->
          <div class="col-lg-4">
            <div class="card" style="margin-bottom: 25px">
              <div class="card-body pb-0" style="margin-bottom: 25px">
                <h5 class="card-title">Рентабельность</h5>
                <PieChart :data="ABC_PROFIT.values" :labels="ABC_PROFIT.data"/>
              </div>
            </div>
          </div>
          <div class="col-lg-4">
            <div class="card" style="margin-bottom: 25px">
              <div class="card-body pb-0" style="margin-bottom: 25px">
                <h5 class="card-title">Оборачиваемость</h5>
                <PieChart :data="ABC_TURNOVER.values" :labels="ABC_TURNOVER.data"/>
              </div>
            </div>
          </div>
          <div class="col-lg-4">
            <div class="card" style="margin-bottom: 25px">
              <div class="card-body pb-0" style="margin-bottom: 25px">
                <h5 class="card-title">Итоговый анализ</h5>
                <PieChart :data="ABC_RESULT.values" :labels="ABC_RESULT.data"/>
              </div>
            </div>
          </div>
        </div>
        <div class="row">
          <!-- Левая колонка -->
          <div class="col-lg-4">
            <div class="card" style="margin-bottom: 25px">
              <div class="card-body pb-0">
                <h5 class="card-title">Рентабельность</h5>
                <ABCTable :marks="profit"/>
              </div>
            </div>
          </div>
          <div class="col-lg-4">
            <div class="card" style="margin-bottom: 25px">
              <div class="card-body pb-0">
                <h5 class="card-title">Оборачиваемость</h5>
                <ABCTable :marks="turnover"/>
              </div>
            </div>
          </div>
          <div class="col-lg-4">
            <div class="card" style="margin-bottom: 25px">
              <div class="card-body pb-0">
                <h5 class="card-title">Итоговый анализ</h5>
                <ABCTable :marks="result"/>
              </div>
            </div>
          </div>
        </div>
      </div>
      <div v-else class="spinner-border text-primary circle" role="status">
        <span class="visually-hidden">Loading...</span>
      </div>
    </section>

  </main>
</template>

<script>
import PieChart from "@/components/charts/PieChart";
import ABCTable from "@/components/tables/ABCTable";
import {mapGetters} from "vuex";
import baseMixin from "@/mixins/baseMixin";
import reportMixin from "@/mixins/reportMixin";

export default {
  name: "ABCReport",
  components: {
    PieChart, ABCTable
  },
  computed: mapGetters(['ABC_TURNOVER', 'ABC_RESULT', 'ABC_PROFIT']),
  data: () => ({
    slug: 'abc',
    profit: [
      {name: 'A', range: '40+'},
      {name: 'B', range: '20-40'},
      {name: 'C', range: 'до 20'},
    ],
    turnover: [
      {name: 'A', range: 'до 30'},
      {name: 'B', range: '30-60'},
      {name: 'C', range: '60+'},
    ],
    result: [
      {name: 'A', range: 'A & A'},
      {name: 'B', range: 'A & B, B & B, A & C'},
      {name: 'C', range: 'B & C, C & C'},
    ],
  }),
  mixins: [baseMixin, reportMixin],
  async mounted() {
    this.reportInfo = await this.getReportInfo(this.slug)
    this.toolLoading = false
    await this.$store.dispatch('GET_ABC_TURNOVER')
    await this.$store.dispatch('GET_ABC_PROFIT')
    await this.$store.dispatch('GET_ABC_RESULT')
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