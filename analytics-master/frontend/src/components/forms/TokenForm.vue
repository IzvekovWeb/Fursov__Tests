<template>
  <form>
    <token-frag-input v-for="supplier in suppliers" :supplier="supplier"/>
  </form>
  <div class="text-center">
    <button type="submit" class="btn btn-primary" style="margin-left: 50px;" @click="editTokens">Изменить</button>
  </div>
</template>

<script>
import TokenFragInput from "@/components/forms/TokenFragInput";
import WBTokenService from "@/services/wb_token.service";

export default {
  name: "TokenForm",
  components: {TokenFragInput},
  props: {
    suppliers: {
      type: Array
    }
  },
  methods: {
    async editTokens() {
      await WBTokenService.editToken(this.suppliers).then(
          res =>{
            this.$store.dispatch('GET_SUPPLIERS_WITHOUT_TOKENS')
          }
      )
    }
  }
}
</script>

<style scoped>

</style>