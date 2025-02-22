<template>
  <v-app>
    <v-app-bar app color="primary" dark>
      <v-toolbar-title>Gabinete Integral de Psicología</v-toolbar-title>
      <v-spacer></v-spacer>
    </v-app-bar>
    <v-main class="main-content">
      <v-container class="pa-0"> <!-- Eliminamos padding del container -->
        <v-row justify="center" no-gutters> <!-- Eliminamos gutters de la fila -->
          <v-col cols="12" md="10" lg="10">
            <v-card class="mt-0"> <!-- Eliminamos padding superior de la card -->
              <MainInfo />
              <v-divider class="my-4"></v-divider> <!-- Añadir un divisor para separar las secciones -->
              <EntryForm
                :isAuthenticated="isAuthenticated"
                :minWords="minWords"
                :dataPolicyAccepted="dataPolicyAccepted"
                @submit="submitForm"
                @update:isAuthenticated="updateIsAuthenticated"
                @update:dataPolicyAccepted="dataPolicyAccepted = $event"
              >
              </EntryForm>

              <v-snackbar v-model="generatingReportSnackbar" :timeout="3000" right>
                Generando informe...
              </v-snackbar>

              <ReportStatus v-if="reportStatusVisible" :status="reportStatus" :uuid="jobId" :idToken="idToken" />
            </v-card>
          </v-col>
        </v-row>
      </v-container>
    </v-main>
    <v-footer app color="primary" dark class="footer-compact" absolute> <!-- Añadido absolute -->
      <v-col class="text-right py-2" cols="12"> <!-- Reducido el padding vertical de py-3 a py-2 -->
        <v-btn icon href="https://github.com/jaimevalero/gifted-children-helper" target="_blank">
          <v-icon>mdi-github</v-icon>
        </v-btn>
        Hecho con <v-icon color="red">mdi-heart</v-icon> para <a href="https://www.asociacionamaci.com/" target="_blank" class="text-white">AMACI</a>
      </v-col>
    </v-footer>
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
      minWords: 100, // Ensure the minWords value is set to 100
      snackbar: false,
      generatingReportSnackbar: false,
      reportStatus: {}, // Change to an object to hold JSON data
      reportStatusVisible: false, // Add a new data property to control visibility
      idToken: '', // Add a new data property for the ID token
      retryCount: 0, // Add a new data property for retry count
      maxRetries: 5, // Add a new data property for maximum retries
      jobId: '' // Add a new data property for the job ID
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
        this.updateIsAuthenticated(true); // Use the new method to update isAuthenticated
        const profile = googleUser.getBasicProfile();
        this.idToken = googleUser.getAuthResponse().id_token; // Get the ID token
        console.log('ID Token after login:', this.idToken); // Log the ID token
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

      this.idToken = formData.idToken; // Save the idToken to the data property
      console.log('ID Token after form submission:', this.idToken); // Log the ID token

      const jobId = generateUUID(); // Generate a UUID for the job
      this.jobId = jobId; // Save the jobId to the data property
      console.log('Generated Job ID:', jobId);

      this.generatingReportSnackbar = true; // Show generating report snackbar

      try {
        const apiUrl = process.env.VUE_APP_API_URL;
        if (!apiUrl) {
          throw new Error('API URL is not defined in environment variables');
        }

        console.log('API URL:', apiUrl); // Log the API URL to console

        const { totalWordCount, idToken, ...filteredFormData } = formData; // Remove totalWordCount and idToken from formData

        const response = await fetch(`${apiUrl}/generate-report`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${idToken}` // Send the ID token in the Authorization header
          },
          body: JSON.stringify({ uuid: jobId, ...filteredFormData }) // Include uuid in the request body
        });

        if (!response.ok) {
          throw new Error('Failed to submit form');
        }

        const result = await response.json();
        console.log('Form submitted successfully:', result);
        this.snackbar = true;
        this.reportStatusVisible = true; // Show the ReportStatus component
        this.reportStatus = { uuid: jobId, progress: 0 }; // Set the initial report status with progress
        // Poll the report status every 5 seconds
        this.pollReportStatus(jobId);

      } catch (error) {
        console.error('Error submitting form:', error);
      } finally {
        this.generatingReportSnackbar = false; // Hide generating report snackbar
      }
    },
    async pollReportStatus(uuid) {
      try {
        const apiUrl = process.env.VUE_APP_API_URL;
        const response = await fetch(`${apiUrl}/report_status/${uuid}`);
        if (!response.ok) {
          throw new Error('Failed to fetch report status');
        }
        console.log('Report 1');
        const status = await response.json();
        console.log('Report status2:', status);
        this.reportStatus = status;
        console.log('Report generation in progress3');
        if (status.progress < 1) {
          console.log('Report generation in progress');
          setTimeout(() => this.pollReportStatus(uuid), 5000); // Poll again after 5 seconds
          console.log('Report generation in progress2');
        } else {
          console.log('Report generation complete');
        }
      } catch (error) {
        console.error('Error fetching report status:', error);
      }
    },
    updateIsAuthenticated(value) {
      this.isAuthenticated = value;
    }
  }
}
</script>

<style>
/* Ajustes para eliminar espacios innecesarios */
.main-content {
  padding-top: 0 !important;
}

.v-application--wrap {
  min-height: 100vh !important;
}

/* Ajustar el espacio del app-bar */
.v-app-bar + .v-main {
  padding-top: 64px !important; /* altura del navbar */
}

@import 'https://cdn.jsdelivr.net/npm/vuetify@2.6.4/dist/vuetify.min.css';

/* Ajuste para hacer el footer más compacto */
.footer-compact {
  min-height: 40px !important; /* Reducido de 48px por defecto */
  height: auto !important;
  position: fixed !important;
  bottom: 0 !important;
  width: 100% !important;
  z-index: 100 !important;
}

.footer-compact .v-btn {
  margin: 0 4px !important;
}

/* Ocultar footer duplicado de Vuetify */
.v-application .v-footer:not(.footer-compact) {
  display: none !important;
}

/* Ajustar el contenido principal para que no se solape con el footer */
.v-main {
  padding-bottom: 40px !important;
}
</style>

