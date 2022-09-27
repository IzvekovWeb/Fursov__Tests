<template>
  <table class="table">
    <thead>
    <tr>
      <th scope="col">№</th>
      <th scope="col">Бренд</th>
      <th scope="col">Заказы (шт)</th>
    </tr>
    </thead>
    <tbody>
    <tr v-for="(brand, index) in brands" :key="brand.id">
      <th scope="row">{{ index + 1}}</th>
      <td>{{ brand.brand }}</td>
      <td>{{ brand.orders_amount }}</td>
    </tr>
    </tbody>
  </table>
</template>

<script>
export default {
  name: "TopBrandsTable",
  props: {
    brands: Object
  }
}
</script>

<style scoped>

</style>