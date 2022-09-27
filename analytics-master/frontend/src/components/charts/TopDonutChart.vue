<template>
  <div class="chart-container">
    <apexchart :options="options" :series="series"></apexchart>
  </div>
</template>

<script>
export default {
  name: "DashboardTopCategories",
  props: {
    series: {
      type: Array
    },
    labels: {
      type: Array
    }
  },
  computed: {
    options() {
      return {
        chart: {
          type: 'donut',
          toolbar: {
            show: false
          },
        },
        dataLabels: {
          enabled: false
        },
        colors: ['#ff771d', '#2ECA6AFF', '#4154f1', '#282e9a',  '#B32428'],
        labels: this.labels,
        tooltip: {
          y: {
            formatter: function (value) {
              let parts = value.toString().split(".");
              parts[0] = parts[0].replace(/\B(?=(\d{3})+(?!\d))/g, " ");
              return parts.join(".");
            },
          },
        },
      }
    }
  }
}
</script>

<style scoped>
.chart-container {
  margin-bottom: 25px;
}
</style>