<template>
  <table class="table">
    <thead>
    <tr>
      <th scope="col">№</th>
      <th scope="col">Оценка</th>
      <th scope="col">Критерий</th>
    </tr>
    </thead>
    <tbody>
    <tr v-for="(mark, index) in marks">
      <th scope="row">{{ index + 1}}</th>
      <td>{{ mark.name }}</td>
      <td>{{ mark.range }}</td>
    </tr>
    </tbody>
  </table>
</template>

<script>
export default {
  name: "ABCTable",
  props: {
    marks: {
      type: Array
    }
  }
}
</script>

<style scoped>

</style>