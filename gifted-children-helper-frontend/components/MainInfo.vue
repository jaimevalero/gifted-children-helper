<template>
  <div class="main-info">
    <v-alert type="info" class="mb-2 mt-0">
      Esta aplicación de inteligencia artificial simula un gabinete psicológico, especializado en familias con niños de altas capacidades.
      <br><br>
      Por favor, completa el formulario de entrada para generar un informe psicológico. (Tarda unos 10 minutos)
      <v-btn href="https://github.com/jaimevalero/gifted-children-helper/raw/master/examples/example_report.pdf" target="_blank" color="primary" class="mt-2">
        <v-icon left>mdi-download</v-icon> <!-- Añadir icono de descarga -->
        Descargar reporte de ejemplo ficticio
      </v-btn>
    </v-alert>
    <v-alert type="info" class="mt-2">
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
.main-info {
  padding-top: 0;
}

.v-alert {
  margin-bottom: 8px !important;
}
</style>
