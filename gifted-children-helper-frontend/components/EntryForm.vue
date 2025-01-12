<template>
  <form @submit.prevent="submitForm">
    <v-container>
      <v-row dense>
        <v-col cols="12">
          <v-textarea
            outlined
            label="1. Descripción del Niño/a"
            v-model="description"
            rows="10"
            placeholder="Incluye edad, lugar de residencia, personalidad, y características principales.
Ejemplo:
Juan es un niño de 8 años que vive en Madrid con su hermano Enrique de 5 años. Es un niño muy curioso y le encanta explorar su entorno."
          />
        </v-col>
        <v-col cols="12">
          <v-textarea
            outlined
            label="2. Dinámica Familiar"
            v-model="family_dynamics"
            rows="10"
            placeholder="Describe cómo interactúa con la familia, rutinas en casa, y relación con hermanos.
Ejemplo:
Juan tiene una relación muy cercana con su hermano Enrique. Juegan juntos todos los días y comparten muchas actividades."
          />
        </v-col>
        <v-col cols="12">
          <v-textarea
            outlined
            label="3. Comportamiento y Manejo Emocional"
            v-model="emotional_behavior"
            rows="10"
            placeholder="Explica cómo se comporta en diferentes situaciones y gestiona sus emociones.
Ejemplo:
Juan suele ser muy tranquilo, pero a veces se frustra cuando no puede hacer algo a la primera. Sin embargo, es muy perseverante y siempre intenta hasta lograrlo."
          />
        </v-col>
        <v-col cols="12">
          <v-textarea
            outlined
            label="4. Habilidades y Desarrollo"
            v-model="skills_development"
            rows="10"
            placeholder="Describe las habilidades del niño/a y áreas de desarrollo (académico, físico, creativo, social).
Ejemplo:
Juan es muy bueno en matemáticas y le encanta resolver problemas. También es muy creativo y le gusta dibujar y construir cosas con bloques."
          />
        </v-col>
        <v-col cols="12">
          <v-textarea
            outlined
            label="5. Contexto Escolar y Extraescolar"
            v-model="school_context"
            rows="10"
            placeholder="Comenta sobre su progreso académico y actividades fuera de la escuela.
Ejemplo:
Juan tiene muy buen rendimiento académico y participa en un club de ciencias después de la escuela. También le gusta jugar al fútbol con sus amigos."
          />
        </v-col>
        <v-col cols="12">
          <v-textarea
            outlined
            label="6. Problemas y Situaciones Difíciles"
            v-model="problems_difficulties"
            rows="10"
            placeholder="Indica los problemas principales y cuándo suelen ocurrir.
Ejemplo:
Juan a veces tiene dificultades para concentrarse en clase, especialmente cuando está cansado. También puede ser un poco tímido en situaciones nuevas."
          />
        </v-col>
        <v-col cols="12">
          <v-textarea
            outlined
            label="7. Observaciones Adicionales"
            v-model="additional_observations"
            rows="10"
            placeholder="Añade cualquier otro detalle que consideres importante.
Ejemplo:
Juan es un niño muy cariñoso y siempre está dispuesto a ayudar a los demás. Le gusta mucho la naturaleza y disfruta de las actividades al aire libre."
          />
        </v-col>
        <v-col cols="12" class="text-right">
          <v-btn :disabled="!isAuthenticated || totalWordCount < minWords" color="primary" type="submit">Enviar</v-btn>
          <p v-if="!isAuthenticated" class="error--text">You must be logged in with Google to submit the form.</p>
          <p v-if="totalWordCount < minWords" class="error--text">Minimum {{ minWords }} words required. Current: {{ totalWordCount }}</p>
        </v-col>
      </v-row>
    </v-container>
  </form>
</template>

<script>
export default {
  name: 'EntryForm',
  props: {
    isAuthenticated: {
      type: Boolean,
      required: true
    },
    minWords: {
      type: Number,
      required: true
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
      additional_observations: ''
    }
  },
  computed: {
    totalWordCount() {
      // Calculate the total word count from all textareas
      return (
        this.description.split(' ').length +
        this.family_dynamics.split(' ').length +
        this.emotional_behavior.split(' ').length +
        this.skills_development.split(' ').length +
        this.school_context.split(' ').length +
        this.problems_difficulties.split(' ').length +
        this.additional_observations.split(' ').length
      );
    }
  },
  methods: {
    submitForm() {
      if (!this.isAuthenticated) {
        console.error('User is not authenticated');
        return;
      }
      if (this.totalWordCount < this.minWords) {
        console.error(`Minimum ${this.minWords} words required. Current: ${this.totalWordCount}`);
        return;
      }
      console.log('Form submitted with:', this.description, this.family_dynamics, this.emotional_behavior, this.skills_development, this.school_context, this.problems_difficulties, this.additional_observations);
    }
  }
}
</script>

<style scoped>
</style>
