<template>
  <v-form @submit.prevent="handleSubmit">
    <v-divider class="my-4"></v-divider> <!-- Añadir un divisor para separar las secciones -->
    <v-card-title class="text-h5">Formulario de entrada</v-card-title> <!-- Añadir el título del formulario -->

    <v-container>
      <v-row dense>
        <v-col cols="12">
          <v-textarea
            outlined
            label="1. Descripción del Niño/a"
            v-model="description"
            rows="6"
            placeholder="Incluye edad, lugar de residencia, personalidad, y características principales.
Ejemplo:
Juan es un niño de 8 años que vive en Madrid con su hermano Enrique de 5 años. Es un niño muy curioso y le encanta explorar su entorno."
            prepend-inner-icon="mdi-account-child"
          />
        </v-col>
        <v-col cols="12">
          <v-textarea
            outlined
            label="2. Dinámica Familiar"
            v-model="family_dynamics"
            rows="6"
            placeholder="Describe cómo interactúa con la familia, rutinas en casa, y relación con hermanos.
Ejemplo:
Juan tiene una relación muy cercana con su hermano Enrique. Juegan juntos todos los días y comparten muchas actividades."
            prepend-inner-icon="mdi-home-heart"
          />
        </v-col>
        <v-col cols="12">
          <v-textarea
            outlined
            label="3. Comportamiento y Manejo Emocional"
            v-model="emotional_behavior"
            rows="6"
            placeholder="Explica cómo se comporta en diferentes situaciones y gestiona sus emociones.
Ejemplo:
Juan suele ser muy tranquilo, pero a veces se frustra cuando no puede hacer algo a la primera. Sin embargo, es muy perseverante y siempre intenta hasta lograrlo."
            prepend-inner-icon="mdi-emoticon-happy"
          />
        </v-col>
        <v-col cols="12">
          <v-textarea
            outlined
            label="4. Habilidades y Desarrollo"
            v-model="skills_development"
            rows="6"
            placeholder="Describe las habilidades del niño/a y áreas de desarrollo (académico, físico, creativo, social).
Ejemplo:
Juan es muy bueno en matemáticas y le encanta resolver problemas. También es muy creativo y le gusta dibujar y construir cosas con bloques."
            prepend-inner-icon="mdi-school"
          />
        </v-col>
        <v-col cols="12">
          <v-textarea
            outlined
            label="5. Contexto Escolar y Extraescolar"
            v-model="school_context"
            rows="6"
            placeholder="Comenta sobre su progreso académico y actividades fuera de la escuela.
Ejemplo:
En el colegio, Juan suele aburrirse con tareas repetitivas y ha manifestado interés por proyectos más desafiantes. Participa en un taller de robótica después de clases, donde trabaja con estudiantes mayores y disfruta la experiencia. Sus profesores reconocen su talento, pero a veces no saben cómo manejar sus necesidades específicas."
            prepend-inner-icon="mdi-book-open-variant"
          />
        </v-col>
        <v-col cols="12">
          <v-textarea
            outlined
            label="6. Problemas y Situaciones Difíciles"
            v-model="problems_difficulties"
            rows="6"
            placeholder="Indica los problemas principales y cuándo suelen ocurrir.
Ejemplo:
Juan a veces tiene dificultades para concentrarse en clase, especialmente cuando está cansado. También puede ser un poco tímido en situaciones nuevas."
            prepend-inner-icon="mdi-alert-circle"
          />
        </v-col>
        <v-col cols="12">
          <v-textarea
            outlined
            label="7. Observaciones Adicionales"
            v-model="additional_observations"
            rows="6"
            placeholder="Añade cualquier otro detalle que consideres importante.
Ejemplo:
Juan es un niño muy cariñoso y siempre está dispuesto a ayudar a los demás. Le gusta mucho la naturaleza y disfruta de las actividades al aire libre."
            prepend-inner-icon="mdi-comment-text"
          />
        </v-col>
        <v-col cols="12">
          <p v-if="totalWordCount < minWords" class="error--text">Por favor debe rellenar al menos {{ minWords }} palabras. Palabras actuales: {{ totalWordCount }}</p>
        </v-col>
        <v-col cols="12">
          <TermsAndPolicy @accept-change="onAcceptChange" :default-checked="dataPolicyAccepted" />
          <p v-if="!dataPolicyAccepted" class="error--text">
            Debes aceptar los términos de servicio.
          </p>
        </v-col>
        <v-col cols="12" class="text-right">
          <v-btn  v-if="!computedIsAuthenticated" elevation="2" @click="loginWithGoogle" color="secondary" class="my-3">
            <v-icon left>mdi-google</v-icon> <!-- Añadir icono de Google -->
            Iniciar sesión con Google
          </v-btn>
          <p v-if="!computedIsAuthenticated" class="error--text">Debes estar logado con Google.</p>

        </v-col>
        <v-col cols="12" class="text-right">
          <v-btn
            :disabled="!computedIsAuthenticated || totalWordCount < minWords || !dataPolicyAccepted"
            color="green"
            type="submit"
          >
            <v-icon left>mdi-send</v-icon> <!-- Añadir icono de envío -->
            Enviar
          </v-btn>
        </v-col>
        <v-snackbar v-model="loginSuccessSnackbar" :timeout="3000" right>
          ¡Usuario logado con éxito!
        </v-snackbar>
      </v-row>
    </v-container>
  </v-form>
</template>

<script>
// Import the TermsAndPolicy component
import TermsAndPolicy from './TermsAndPolicy.vue';
import Cookies from 'js-cookie'; // Import js-cookie for handling cookies

export default {
  name: 'EntryForm',
  components: {
    TermsAndPolicy // Register the component
  },
  props: {
    isAuthenticated: {
      type: Boolean,
      required: true
    },
    dataPolicyAccepted: {
      type: Boolean,
      required: true,
      default: process.env.NODE_ENV === 'development' // Default to true in development
    }
  },
  data() {
    return {
      description: '',
      family_dynamics: '',
      emotional_behavior: '',
      skills_development: '',
      school_context: '',
      problems_difficulties: '',
      additional_observations: '',
      minWords: 0, // Ensure the default value is set to 200
      idToken: '', // Add a new data property for the ID token
      loginSuccessSnackbar: false // Add a new data property for the snackbar
    }
  },
  computed: {
    totalWordCount() {
      // Calculate the total word count from all textareas
      return (
        this.description.split(' ').filter(word => word).length +
        this.family_dynamics.split(' ').filter(word => word).length +
        this.emotional_behavior.split(' ').filter(word => word).length +
        this.skills_development.split(' ').filter(word => word).length +
        this.school_context.split(' ').filter(word => word).length +
        this.problems_difficulties.split(' ').filter(word => word).length +
        this.additional_observations.split(' ').filter(word => word).length
      );
    },
    computedIsAuthenticated: {
      get() {
        return this.isAuthenticated;
      },
      set(value) {
        this.$emit('update:isAuthenticated', value);
      }
    }
  },
  created() {
    // Retrieve authentication state and ID token from cookies
    const isAuthenticated = Cookies.get('isAuthenticated') === 'true';
    const idToken = Cookies.get('idToken');
    if (isAuthenticated && idToken) {
      this.computedIsAuthenticated = true;
      this.idToken = idToken;
      this.loginSuccessSnackbar = true; // Show the snackbar if the user is authenticated
    }
    else {
      this.computedIsAuthenticated = false;
    }
  },
  methods: {
    handleSubmit() {
      if (!this.computedIsAuthenticated) {
        console.error('User is not authenticated');
        return;
      }
      if (this.totalWordCount < this.minWords) {
        console.error(`Minimum ${this.minWords} words required. Current: ${this.totalWordCount}`);
        return;
      }
      console.log('ID Token before emitting form data:', this.idToken); // Log the ID token
      // Emit form data to parent component
      this.$emit('submit', {
        description: this.description,
        family_dynamics: this.family_dynamics,
        emotional_behavior: this.emotional_behavior,
        skills_development: this.skills_development,
        school_context: this.school_context,
        problems_difficulties: this.problems_difficulties,
        additional_observations: this.additional_observations,
        totalWordCount: this.totalWordCount,
        idToken: this.idToken // Include the ID token in the emitted data
      });
    },
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
        this.computedIsAuthenticated = true; // Use the computed property to update isAuthenticated
        const profile = googleUser.getBasicProfile();
        this.idToken = googleUser.getAuthResponse().id_token; // Get the ID token
        console.log('ID Token after login:', this.idToken); // Log the ID token
        console.log('Logged in as:', profile.getName());
        this.loginSuccessSnackbar = true; // Show the snackbar on successful login
        this.$emit('update:isAuthenticated', true); // Emit the authentication status to the parent component

        // Save authentication state and ID token in cookies
        Cookies.set('isAuthenticated', 'true', { expires: 7 });
        Cookies.set('idToken', this.idToken, { expires: 7 });
      } catch (error) {
        console.error('Error signing in with Google:', error);
      }
    },
    onAcceptChange(accepted) {
      this.$emit('update:dataPolicyAccepted', accepted);
      if (accepted) {
        this.warmupBackend();
      }
    },

    warmupBackend() {
      try {
        const apiUrl = process.env.VUE_APP_API_URL;
        if (!apiUrl) {
          console.warn('API URL is not defined in environment variables');
          return;
        }

        // Fire and forget request to warm up the backend
        fetch(`${apiUrl}/health`).catch(err => {
          console.debug('Warmup request sent to backend');
          // Intentionally not handling the error as this is just a warmup
        });
      } catch (error) {
        // Silently fail as this is just a warmup request
        console.debug('Failed to send warmup request');
      }
    },

  }
}
</script>

<style scoped>
</style>

