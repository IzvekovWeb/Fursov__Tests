<template>
  <component :is="layout">
    <router-view/>
  </component>
</template>

<script>
import MainLayout from "@/components/layouts/MainLayout";
import LoginLayout from "@/components/layouts/LoginLayout";

export default {
  components: {
    MainLayout, LoginLayout
  },
  computed: {
    layout() {
      return (this.$route.meta.layout || 'empty') + '-layout'
    }
  }
}
</script>

<style lang="scss">
@import "../public/assets/css/style.css";
@import "../public/assets/vendor/bootstrap-icons/bootstrap-icons.css";

.card {
  border: none !important;
}

body {
  background-color: #f6f9ff !important;
}
</style>
