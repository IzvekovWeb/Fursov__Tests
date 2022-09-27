<template>
  <div>
    <apexchart :options="options" :series="data_series"></apexchart>
  </div>
</template>

<script>

export default {
  name: 'ProfitlabilityDynamic',
  props: {
    series: {
      type: Array
    },
    labels: {
      type: Array,
    }
  },
  methods: {
    getNumWithSpaces(x) {
      // if (x > 1000000) {
      //   let s = x / 1000000
      //   return s.toFixed(1).toString() + 'млн'
      // }
      let parts = x.toString().split(".");
      parts[0] = parts[0].replace(/\B(?=(\d{3})+(?!\d))/g, " ");
      return parts.join(".");
    },
  },
  computed: {
    data_series() {
      return [{
        name: 'Рентабельность',
        data: this.series
      }]
    },
    options() {
      return {
        chart: {
          type: 'area',
          toolbar: {
            show: false
          },
          height: '100px',
        },
        markers: {
          size: 4
        },
        colors: ['#4154f1', '#ff771d', '#2ECA6AFF', '#282e9a', '#B32428'],
        fill: {
          type: "gradient",
          gradient: {
            shadeIntensity: 1,
            opacityFrom: 0.3,
            opacityTo: 0.4,
            stops: [0, 90, 100]
          }
        },
        dataLabels: {
          enabled: false
        },
        stroke: {
          curve: 'smooth',
          width: 2
        },
        xaxis: {
          categories: this.labels,
          labels: {
            show: true,
            rotate: -30,
            rotateAlways: true,
          },
        },
        yaxis: {
          labels: {
            show: true,
            offsetX: 0,
            offsetY: 0,
            rotate: 0,
            formatter: (value) => {
              let parts = value.toString().split(".");
              parts[0] = parts[0].replace(/\B(?=(\d{3})+(?!\d))/g, " ");
              return parts.join(".");
            },
          },
        },
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
  },
}
</script>


<style scoped>
</style>