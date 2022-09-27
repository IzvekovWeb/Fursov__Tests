<template>
  <Header :USER="USER" v-if="!loading"/>
  <sidebar/>
  <number-modal v-model:show="dialogVisibility"/>
  <router-view/>
</template>

<script>
import Sidebar from "@/components/UI/Sidebar";
import Header from "@/components/UI/Header";
import NumberModal from "@/components/UI/NumberModal";
import {mapActions, mapGetters} from "vuex";
import WBTokenService from "@/services/wb_token.service";
import api from "@/api";
import API_URL from "@/consts";

export default {
  name: "MainLayout",
  components: {
    Sidebar, Header, NumberModal
  },
  computed: {
    ...mapGetters(['USER'])
  },
  data: () => ({
    loading: true,
    dialogVisibility: null
  }),
  methods: mapActions(['GET_USER']),
  async mounted() {

    await this.$store.dispatch('GET_USER')
    this.dialogVisibility = !(await api.get(API_URL + 'check-wb-auth-token')).data
    await this.$metrika.userParams({username: this.USER.username})
    this.loading = false
  }
}
</script>

<style scoped>

</style>