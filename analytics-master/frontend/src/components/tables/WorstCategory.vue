<template>
  <table class="table">
    <thead>
    <tr>
      <th scope="col">№</th>
      <th scope="col">Категория</th>
      <th scope="col">Заказы (руб)</th>
    </tr>
    </thead>
    <tbody>
    <tr v-for="(category, index) in categories" :key="category.id">
      <th scope="row">{{ index + 1}}</th>
      <td>{{ category.name }}</td>
      <td>{{ category.orders_rub }}</td>
    </tr>
    </tbody>
  </table>
</template>

<script>
export default {
  name: "WorstCategory",
  props: {
    categories: Object
  }
}
</script>

<style scoped>

</style>