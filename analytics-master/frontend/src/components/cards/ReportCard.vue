<template>
  <div class="card-temp">
    <div class="card-header">
      <img src="@/assets/analytics.jpg" alt="rover" />
    </div>
    <div class="card-body-temp">
      <h4 class="card-title-m">
        {{index + '. ' + report.sheet_name}}
      </h4>
      <span class="update-time"><b>{{report.update_at}}</b></span>
      <p class="card-desc">
        {{report.description}}
      </p>
      <div class="card-footer">
        <router-link v-if="report.has_detail !== 'False'" :to="'/analytic/wildberries/' + report.slug" class="btn btn-primary" style="margin-right: 10px">Подробнее</router-link>
        <button class="btn btn-primary" style="margin-right: 10px;" v-else disabled>Подробнее</button>
        <a :href="createSheetLink(report.spreadsheet_id, report.sheet_id)" target="_blank" class="card-link">Таблица</a>
      </div>
    </div>
    <i class="bi bi-x-circle reload-btn" style="color: red; cursor: pointer" v-if="error" :title="errorText"></i>
    <i class="bi bi-check-circle reload-btn" v-else-if="check"></i>
    <div class="spinner-border text-primary reload-btn-circle" role="status" v-else-if="refresh"></div>
    <a href="javascript://" class="reload-btn" v-else @click="refreshReport(report.id)"><i class="bi bi-arrow-clockwise reload-icon"></i></a>
  </div>
</template>

<script>
import axios_custom from "@/api";
import API_URL from "@/consts";

export default {
  name: "ReportCard",
  props: {
    report: Object,
    index: Number
  },
  data: () => ({
    refresh: false,
    check: false,
    error: false,
    errorText: ''
  }),
  methods: {
    createSheetLink(table, sheet) {
      return 'https://docs.google.com/spreadsheets/d/' + table + '/edit#gid=' + sheet
    },
    async refreshReport(report_id){
      this.refresh = true
      await axios_custom
          .put(API_URL + 'analytic/wildberries/refresh/' + report_id, {})
          .then(response => {
            this.report.update_at = response.data.update_at
            this.refresh = false
            this.check = true
          })
          .catch(error => {
            this.refresh = false
            this.error = true
            this.errorText = error
          });
    }
  }
}
</script>

<style scoped>
.bi-check-circle {
  color: #56b458;
}

.reload-btn {
  font-size: 1.5rem;
  position: absolute;
  right: 20px;
  top: 10px;
}
.reload-btn-circle{
  width: 25px;
  height: 25px;
  position: absolute;
  right: 20px;
  top: 10px;
}

.card-link {
  text-decoration: none;
  font-size: 16px;
}

.card-temp {
  position: relative;
  margin: 10px;
  background-color: #fff;
  border-radius: 10px;
  box-shadow: 0 2px 20px rgba(0, 0, 0, 0.1);
  overflow: hidden;
  width: 300px;
}

.card-header img {
  width: 100%;
  height: 200px;
  object-fit: contain;
}
.card-body-temp {
  height: 100%;
  display: flex;
  flex-direction: column;
  padding-left: 20px;
  padding-right: 20px;
  padding-bottom: 20px;
  min-height: 250px;
}

.card-body p {
  font-size: 16px;
  margin: 0 0 40px;
}

.user img {
  border-radius: 50%;
  width: 40px;
  height: 40px;
  margin-right: 10px;
}
.user-info h5 {
  margin: 0;
}
.user-info small {
  color: #545d7a;
}

.card-title-m {
  align-self: flex-start;
  font-size: 22px;
  margin-top: 5px;
  margin-bottom: 2px;
}
.card-desc {
  line-height: 20px;
}

.card-footer {
  align-items: center;
  position: absolute;
  bottom: 15px;
  left: 15px;
}

.update-time {
  font-size: 14px;
  margin-bottom: 10px;
  color: #18249ADB;
}

</style>