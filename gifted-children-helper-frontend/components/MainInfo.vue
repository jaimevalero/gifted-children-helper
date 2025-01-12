<template>
  <div>
    <v-alert type="info" class="mb-4">
      Esta aplicación de inteligencia artificial simula un gabinete psicológico, especializado en familias con niños de altas capacidades.
      <br><br>
      Por favor, completa el formulario para generar un informe psicológico.
      <v-btn href="https://github.com/jaimevalero/gifted-children-helper/raw/master/src/streamlit/static/example_report.pdf" target="_blank" color="primary" class="mt-2">
        Descargar reporte de ejemplo ficticio
      </v-btn>
    </v-alert>
    <v-alert type="info">
      No olvides logarte con google y aceptar los términos del servicio.
    </v-alert>
  </div>
</template>

<script>
export default {
  name: 'MainInfo'
}
</script>

<style scoped>
</style>
