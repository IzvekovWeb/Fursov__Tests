<template>
  <table class="table">
    <thead>
    <tr>
      <th scope="col">№</th>
      <th scope="col">Дата</th>
      <th scope="col">Заказы (руб)</th>
    </tr>
    </thead>
    <tbody>
    <tr v-for="(day, index) in days" :key="day.id">
      <th scope="row">{{ index + 1}}</th>
      <td>{{ day.date }}</td>
      <td>{{ getNumWithSpaces(day.data) }}</td>
    </tr>
    </tbody>
  </table>
</template>

<script>
export default {
  name: "OrdersByDays",
  props: {
    days: Object
  },
  methods: {
    getNumWithSpaces(x) {
      if (x > 1000000) {
        let s = x / 1000000
        return s.toFixed(1).toString() + 'млн'
      }
      let parts = x.toString().split(".");
      parts[0] = parts[0].replace(/\B(?=(\d{3})+(?!\d))/g, " ");
      return parts.join(".");
    },
  }
}
</script>

<style scoped>

</style>