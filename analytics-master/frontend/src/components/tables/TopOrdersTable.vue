<template>
  <table class="table">
    <thead>
    <tr>
      <th scope="col">№</th>
      <th scope="col">Артикул</th>
      <th scope="col">Номенклатура</th>
      <th scope="col">Заказы (шт)</th>
      <th scope="col">Заказы (руб)</th>
    </tr>
    </thead>
    <tbody>
    <tr v-for="(article, index) in articles" :key="article.nomenclature">
      <th scope="row">{{ index + 1}}</th>
      <td>{{ article.article }}</td>
      <td>{{ article.nomenclature }}</td>
      <td>{{ numberWithSpaces(article.orders_amount) }}</td>
      <td>{{ numberWithSpaces(article.orders_rub) }}</td>
    </tr>

    </tbody>
  </table>

</template>

<script>
export default {
  name: "TopOrdersTable",
  props: {
    articles: Object
  },
  methods: {
    numberWithSpaces(x) {
      return x.toString().replace(/\B(?=(\d{3})+(?!\d))/g, " ");
    }
  }
}
</script>

<style scoped>

</style>