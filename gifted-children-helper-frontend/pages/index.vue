<template>
  <v-app>
    <v-container class="py-5">
      <v-row justify="center">
        <v-col cols="12" md="8" lg="6">
          <v-card class="pa-4">
            <MainInfo />
            <EntryForm :isAuthenticated="isAuthenticated" :minWords="minWords" />
            <TermsAndPolicy @accept-change="onAcceptChange" />
            <v-btn v-if="!isAuthenticated" @click="loginWithGoogle" color="primary">Login with Google</v-btn>
            <v-snackbar v-model="snackbar" :timeout="3000" right>
              User logged in successfully!
            </v-snackbar>
          </v-card>
        </v-col>
      </v-row>
    </v-container>
  </v-app>
</template>

<script>
import EntryForm from '~/components/EntryForm.vue';
import MainInfo from '~/components/MainInfo.vue';
import TermsAndPolicy from '~/components/TermsAndPolicy.vue';

export default {
  name: 'IndexPage',
  components: {
    EntryForm,
    MainInfo,
    TermsAndPolicy
  },
  data() {
    return {
      isAuthenticated: false,
      dataPolicyAccepted: false,
      minWords: 200, // Minimum word count for the form
      snackbar: false // Snackbar visibility
    }
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
    }
  }
}
</script>

<style>
@import 'https://cdn.jsdelivr.net/npm/vuetify@2.6.4/dist/vuetify.min.css';
</style>
