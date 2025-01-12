<template>
  <v-app>
    <v-app-bar app color="primary" dark>
      <v-toolbar-title>Gabinete Integral de Psicología</v-toolbar-title>
      <v-spacer></v-spacer>
      <v-btn text href="https://www.asociacionamaci.com/" target="_blank">AMACI</v-btn>
    </v-app-bar>
    <v-main>
      <v-container class="py-5">
        <v-row justify="center">
          <v-col cols="12" md="8" lg="6">
            <v-card class="pa-4">
              <MainInfo />
              <EntryForm
                :isAuthenticated="isAuthenticated"
                :minWords="minWords"
                :dataPolicyAccepted="dataPolicyAccepted"
                @submit="submitForm"
              />
              <TermsAndPolicy @accept-change="onAcceptChange" />
              <p v-if="!dataPolicyAccepted" class="error--text">
                Debes aceptar los términos de servicio.
              </p>
              <v-btn v-if="!isAuthenticated" @click="loginWithGoogle" color="primary">Login with Google</v-btn>
              <v-snackbar v-model="snackbar" :timeout="3000" right>
                ¡Usuario logado con éxito!
              </v-snackbar>
              <v-snackbar v-model="generatingReportSnackbar" :timeout="3000" right>
                Generando informe...
              </v-snackbar>
              <p v-if="!isAuthenticated" class="error--text">
                Debes estar logado con Google.
              </p>
              <ReportStatus :status="reportStatus" /> <!-- Add the new component here -->
            </v-card>
          </v-col>
        </v-row>
      </v-container>
    </v-main>
  </v-app>
</template>

<script>
import EntryForm from '~/components/EntryForm.vue';
import MainInfo from '~/components/MainInfo.vue';
import TermsAndPolicy from '~/components/TermsAndPolicy.vue';
import ReportStatus from '~/components/ReportStatus.vue'; // Import the new component
import { generateUUID } from '~/utils.js'; // Import the generateUUID function

export default {
  name: 'IndexPage',
  components: {
    EntryForm,
    MainInfo,
    TermsAndPolicy,
    ReportStatus // Register the new component
  },
  data() {
    return {
      isAuthenticated: false,
      dataPolicyAccepted: false,
      minWords: 0,
      snackbar: false,
      generatingReportSnackbar: false,
      reportStatus: '' // Add a new data property for report status
    };
  },
  methods: {
    async loginWithGoogle() {
      // Log the attempt to sign in
      console.log('Attempting to sign in with Google');

      try {
        // Ensure the Google Auth instance is available
        if (!this.$googleAuth) {
          throw new Error('Google Auth instance is not available');
        }

        // Sign in with Google using the Google Auth instance
        const googleUser = await this.$googleAuth.signIn();
        this.isAuthenticated = true;
        const profile = googleUser.getBasicProfile();
        console.log('Logged in as:', profile.getName());
        this.snackbar = true; // Show snackbar
      } catch (error) {
        console.error('Error signing in with Google:', error);
      }
    },
    onAcceptChange(accepted) {
      this.dataPolicyAccepted = accepted;
    },
    async submitForm(formData) {
      console.log('Form data:', formData); // Log form data to console
      if (!this.isAuthenticated) {
        console.error('User is not authenticated');
        return;
      }
      if (formData.totalWordCount < this.minWords) {
        console.error(`Minimum ${this.minWords} words required. Current: ${formData.totalWordCount}`);
        return;
      }

      const jobId = generateUUID(); // Generate a UUID for the job
      console.log('Generated Job ID:', jobId);

      this.generatingReportSnackbar = true; // Show generating report snackbar

      try {
        const apiUrl = process.env.VUE_APP_API_URL;
        if (!apiUrl) {
          throw new Error('API URL is not defined in environment variables');
        }

        const response = await fetch(`${apiUrl}/submit`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({ jobId, ...formData })
        });

        if (!response.ok) {
          throw new Error('Failed to submit form');
        }

        const result = await response.json();
        console.log('Form submitted successfully:', result);
        this.snackbar = true;

        // Open WebSocket connection to receive report status updates
        const wsUrl = `${process.env.VUE_APP_WS_URL}?uuid=${jobId}`;
        const socket = new WebSocket(wsUrl);

        socket.onmessage = (event) => {
          this.reportStatus = event.data; // Update report status
        };

        socket.onerror = (error) => {
          console.error('WebSocket error:', error);
        };

        socket.onclose = () => {
          console.log('WebSocket connection closed');
        };

      } catch (error) {
        console.error('Error submitting form:', error);
      } finally {
        this.generatingReportSnackbar = false; // Hide generating report snackbar
      }
    }
  }
}
</script>

<style>
@import 'https://cdn.jsdelivr.net/npm/vuetify@2.6.4/dist/vuetify.min.css';
</style>

