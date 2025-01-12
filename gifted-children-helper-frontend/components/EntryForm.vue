<template>
  <v-form @submit.prevent="handleSubmit">
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
Juan tiene muy buen rendimiento académico y participa en un club de ciencias después de la escuela. También le gusta jugar al fútbol con sus amigos."
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
        <v-col cols="12" class="text-right">
          <v-btn :disabled="!isAuthenticated || totalWordCount < minWords" color="primary" type="submit">Enviar</v-btn>
          <p v-if="totalWordCount < minWords" class="error--text">Minimum {{ minWords }} words required. Current: {{ totalWordCount }}</p>
        </v-col>
      </v-row>
    </v-container>
  </v-form>
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
    },
    dataPolicyAccepted: {
      type: Boolean,
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
    handleSubmit() {
      if (!this.isAuthenticated) {
        console.error('User is not authenticated');
        return;
      }
      if (this.totalWordCount < this.minWords) {
        console.error(`Minimum ${this.minWords} words required. Current: ${this.totalWordCount}`);
        return;
      }
      // Emit form data to parent component
      this.$emit('submit', {
        description: this.description,
        family_dynamics: this.family_dynamics,
        emotional_behavior: this.emotional_behavior,
        skills_development: this.skills_development,
        school_context: this.school_context,
        problems_difficulties: this.problems_difficulties,
        additional_observations: this.additional_observations,
        totalWordCount: this.totalWordCount
      });
    }
  }
}
</script>

<style scoped>
</style>
