<template>
  <v-expansion-panels>
    <v-expansion-panel>
      <v-expansion-panel-header>
        Términos de servicio y política de privacidad
      </v-expansion-panel-header>
      <v-expansion-panel-content>
        <v-card>
          <v-card-text>
            <div v-html="termsAndPolicyHtml"></div>
            <v-checkbox
              v-model="accepted"
              label="Acepto los términos de servicio y la política de privacidad"
              @change="onAcceptChange"
            ></v-checkbox>
          </v-card-text>
        </v-card>
      </v-expansion-panel-content>
    </v-expansion-panel>
  </v-expansion-panels>
</template>

<script>
export default {
  name: 'TermsAndPolicy',
  data() {
    return {
      termsAndPolicyHtml: '',
      accepted: false
    }
  },
  mounted() {
    this.loadTermsAndPolicy();
  },
  methods: {
    async loadTermsAndPolicy() {
      try {
        const response = await fetch('/terms_and_policy.html');
        const text = await response.text();
        this.termsAndPolicyHtml = text; // Load HTML content directly
      } catch (error) {
        console.error('Error loading terms and policy:', error);
      }
    },
    onAcceptChange() {
      this.$emit('accept-change', this.accepted);
    }
  }
}
</script>

<style scoped>
</style>
