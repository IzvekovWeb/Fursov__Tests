<template>
  <main id="main" class="main">
    <section class="section dashboard" v-if="!loading">
      <div class="pagetitle">
        <div class="col-lg-12 selfsell-head">
          <h1><b>Учет выкупов</b></h1>
          <div class="head-buttons">
            <selfsell-modal v-model:show="dialogVisibility"/>
            <button class="btn btn-primary" @click="showDialog" style="margin-right: 15px">Добавить выкуп</button>
          </div>
        </div>
      </div>
      <div class="row">
        <!-- Левая колонка -->
        <div class="col-lg-8">
          <div class="row">

            <!-- Заказы (шт) -->
            <div class="col-xxl-4 col-md-6">
              <div class="card info-card sales-card">
                <div class="card-body">
                  <h5 class="card-title">Выкупы (шт) <span>| 3 месяца</span></h5>
                  <div class="d-flex align-items-center">
                    <div class="card-icon rounded-circle d-flex align-items-center justify-content-center">
                      <i class="bi bi-cart"></i>
                    </div> <!-- Картинка -->
                    <div class="ps-3">
                      <h6>{{ SELFSELL_STATISTICS.total_amount }}</h6>
                      <!--                      <span class="text-muted small pt-1">{{}}</span>-->
                      <!--                      <span class="text-success small pt-2 ps-1">прирост</span>-->
                      <!--                      <span class="text-danger small pt-2 ps-1" v-else>спад</span>-->
                    </div> <!-- Значение и прирост -->
                  </div>
                </div>
              </div>
            </div>
            <!-- Заказы (руб) -->
            <div class="col-xxl-4 col-md-6">
              <div class="card info-card revenue-card">
                <div class="card-body">
                  <h5 class="card-title">Наибольшее кол-во выкупов</h5>
                  <div class="d-flex align-items-center">
                    <div class="card-icon rounded-circle d-flex align-items-center justify-content-center">
                      <i class="bi bi-cash"></i>
                    </div>
                    <div class="ps-3">
                      <h6>{{ SELFSELL_STATISTICS.article_total }}</h6>
                      <span class="text-muted small pt-1">{{ SELFSELL_STATISTICS.article }}</span>
                      <!--                      <span class="text-success small pt-2 ps-1"-->
                      <!--                            v-if="true">прирост</span>-->
                      <!--                      <span class="text-danger small pt-2 ps-1" v-else>спад</span>-->
                    </div>
                  </div>
                </div>
              </div>
            </div>
            <!-- Покупки -->
            <div class="col-xxl-4 col-xl-12">
              <div class="card info-card customers-card">
                <div class="card-body">
                  <h5 class="card-title">Выкупы &#8381; <span>| 3 месяца</span></h5>
                  <div class="d-flex align-items-center">
                    <div class="card-icon rounded-circle d-flex align-items-center justify-content-center">
                      <i class="bi bi-people"></i>
                    </div>
                    <div class="ps-3">
                      <h6>{{ SELFSELL_STATISTICS.total_sum }}</h6>
                      <!--                      <span class="text-muted small pt-1">22%</span>-->
                      <!--                      <span class="text-success small pt-2 ps-1"-->
                      <!--                            v-if="true">прирост</span>-->
                      <!--                      <span class="text-danger small pt-2 ps-1" v-else>спад</span>-->
                    </div>
                  </div>

                </div>
              </div>

            </div>
          </div>
          <div class="row">
            <div class="card">
              <div class="card-body">
                <selfsell-table :selfsells="SELFSELLS"/>
              </div>
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
import baseMixin from "@/mixins/baseMixin";
import {mapGetters} from "vuex";
import selfsellTable from "@/components/tables/SelfsellTable";
import SelfsellModal from "@/components/UI/SelfsellModal";

export default {
  name: "SelfSellView",
  components: {SelfsellModal, selfsellTable},
  mixins: [baseMixin],
  methods: {
    showDialog() {
      this.dialogVisibility = true
    },
  },
  data: () => ({
    dialogVisibility: false
  }),
  computed: mapGetters(['SELFSELLS', 'SELFSELL_STATISTICS']),
  async mounted() {
    await this.$store.dispatch('GET_SELFSELLS')
    await this.$store.dispatch('GET_SELFSELL_STATISTICS')
    this.loading = false
  }
}
</script>

<style scoped>
.selfsell-head {
  display: flex;
  flex-direction: row;
  justify-content: space-between;
}
</style>