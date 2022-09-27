<template>
  <div class="row mb-3">
    <div class="col-md-8 col-lg-9">
      <label :for="'token' + supplier.id" class="col-md-4 col-lg-3 col-form-label">{{ supplier.name }}</label>
      <input v-model="supplier.token" name="token" type="text" class="form-control" :id="'token' + supplier.id" style="margin-bottom: 5px;"
             placeholder="Токен API">
      <input v-model="supplier.x64key" name="x64" type="text" class="form-control" :id="'x64key' + supplier.id"  placeholder="x64 ключ">
    </div>
  </div>
</template>

<script>
export default {
  name: "TokenFragInput",
  props: {
    supplier: {
      type: Object
    }
  },
}
</script>

<style scoped>

</style>