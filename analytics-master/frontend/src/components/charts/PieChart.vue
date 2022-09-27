<template>
  <apexchart :series="data" :options="options"></apexchart>
</template>

<script>
export default {
  name: "PieChart",
  props: {
    labels: {
      type: Array
    },
    data: {
      type: Array
    }
  },
  computed: {
    options() {
      return {
        chart: {
          type: 'pie'
        },
        dataLabels: {
          enabled: false
        },
        labels: this.labels
      }
    }
  }
}
</script>

<style scoped>

</style>