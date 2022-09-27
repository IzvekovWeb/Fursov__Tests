<template>
  <table class="table">
    <thead>
    <tr>
      <th scope="col">№</th>
      <th scope="col">Номенклатура</th>
      <th scope="col">Артикул</th>
      <th scope="col">Кол-во товаров</th>
      <th scope="col">Сумма выкупов</th>
      <th scope="col">Дата последнего выкупа</th>
    </tr>
    </thead>
    <tbody>
    <tr v-for="(selfsell, index) in selfsells">
      <th scope="row">{{ index + 1 }}</th>
      <td>{{ selfsell.nm_id }}</td>
      <td>{{ selfsell.article }}</td>
      <td>{{ selfsell.total_amount }}</td>
      <td>{{ selfsell.total_sum }}</td>
      <td>{{ selfsell.last_selfsell }}</td>
    </tr>
    </tbody>
  </table>
</template>

<script>
export default {
  name: "SelfsellTable",
  props: {
    selfsells: Object
  }
}
</script>

<style scoped>

</style>