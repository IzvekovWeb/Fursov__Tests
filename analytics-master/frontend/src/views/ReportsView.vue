<template>
  <main id="main" class="main">
    <section class="section workspace" v-if="!loading">
      <div class="product-list-header">
        <h3 class="workspace-title"><b>Отчеты по Wildberries</b></h3>
      </div>
      <div class="product-wrapper">
        <ReportCard v-for="(report, index) in MAIN_REPORTS" :report="report" :index="index + 1" :key="report.id" class="product"/>
      </div>
    </section>
  </main>
</template>

<script>
import ReportCard from "@/components/cards/ReportCard";
import {mapGetters} from "vuex";

export default {
  name: "ReportsView",
  components: {ReportCard},
  computed: mapGetters(['MAIN_REPORTS']),
  data: () => ({
    loading: false,

  }),
  async mounted() {
    await this.$store.dispatch('GET_USER_REPORTS_FROM_API')
    this.loading = false
  }
}
</script>

<style scoped>
.workspace-title {
  color: #012970;

}

.product-list-header {
  display: flex;
  align-items: center;
  margin-top: 15px;
  margin-bottom: 15px;
}

.workspace {
  margin-left: 40px;
}

.product-wrapper {
  display: grid;
  grid-template-columns: repeat(auto-fill, 266px);
  gap: 15px 70px;
}
</style>