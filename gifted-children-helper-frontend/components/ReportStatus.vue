<template>
  <v-alert v-if="status" type="info">
    {{ status }}
  </v-alert>
</template>

<script>
export default {
  name: 'ReportStatus',
  props: {
    status: {
      type: String,
      required: true
    }
  }
}
</script>

<style scoped>
</style>
