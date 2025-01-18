<template>
  <v-card>
    <v-card-title>{{ title || 'Report Status' }}</v-card-title>
    <v-card-text>
      <v-progress-linear ref="progressBar" :value="progress" height="10"></v-progress-linear> <!-- Add ref to progress bar -->
      <div v-html="renderedLog"></div> <!-- Render the Markdown as HTML -->
      <p v-if="status && status.progress !== undefined">Progress: {{ status.progress }}</p>
    </v-card-text>
  </v-card>
</template>

<script>
export default {
  name: 'ReportStatus',
  props: {
    status: {
      type: Object,
      required: true
    },
    uuid: {
      type: String,
      required: true
    },
    idToken: { // Add idToken prop
      type: String,
      required: true
    }
  },
  data() {
    return {
      progress: 0, // Initialize progress to 0
      title: 'Report Status',
      log: '',
      intervalId: null, // Add an interval ID to manage the polling
      error: null, // Add an error property to handle errors
      lastStatus: null // Add a property to store the last status
    };
  },
  computed: {
    renderedLog() {
      // Convert the Markdown log to HTML using a simple function
      return this.convertMarkdownToHtml(this.log);
    }
  },
  watch: {
    status(newStatus) {
      this.updateStatus(newStatus);
    },
    uuid: {
      immediate: true,
      handler(newUuid) {
        if (newUuid) {
          this.fetchReportStatus(newUuid);
        }
      }
    }
  },
  methods: {
    updateStatus(newStatus) {
      // Update the progress, title, and log based on the new status
      if (JSON.stringify(newStatus) !== JSON.stringify(this.lastStatus)) {
        if (newStatus.progress !== undefined) {
          this.progress = Math.max(0, Math.min(newStatus.progress, 1)); // Ensure progress is between 0 and 1
          this.updateProgressBar(this.progress); // Update the progress bar using JavaScript
        }
        this.title = newStatus.title || 'Report Status';
        let logEntry = newStatus.log || '';
        if (!logEntry.endswith('\n')) {
          logEntry += '\n'; // Ensure the log entry ends with a newline
        }
        this.log += logEntry;
        this.lastStatus = newStatus; // Update the last status
      }
    },
    updateProgressBar(progress) {
      // Update the progress bar using pure JavaScript
      const progressBar = document.querySelector('[ref="progressBar"] .v-progress-linear__bar');
      if (progressBar) {
        progressBar.style.width = `${progress * 100}%`;
      }
    },
    async pollStatus() {
      try {
        const apiUrl = process.env.VUE_APP_API_URL;
        if (!apiUrl) {
          throw new Error('API URL is not defined in environment variables');
        }

        const response = await fetch(`${apiUrl}/report_status/${this.uuid}`, {
          headers: {
            'Authorization': `Bearer ${this.idToken}` // Send the ID token in the Authorization header
          }
        });
        if (!response.ok) {
          throw new Error('Failed to fetch report status');
        }
        const data = await response.json();
        this.updateStatus(data);
        if (data.progress === 1) {
          clearInterval(this.intervalId); // Stop polling when progress reaches 1
        }
      } catch (error) {
        this.error = 'Error fetching report status. Please try again later.';
      }
    },
    async fetchReportStatus(uuid) {
      try {
        const apiUrl = process.env.VUE_APP_API_URL;
        const response = await fetch(`${apiUrl}/report_status/${uuid}`, {
          headers: {
            'Authorization': `Bearer ${this.idToken}` // Send the ID token in the Authorization header
          }
        });
        if (!response.ok) {
          throw new Error('Failed to fetch report status');
        }
        const status = await response.json();
        this.$emit('update:status', status); // Emit the updated status to the parent component
      } catch (error) {
        this.error = 'Error fetching report status. Please try again later.';
      }
    },
    convertMarkdownToHtml(markdown) {
      // Simple Markdown to HTML conversion
      return markdown
    }
  },
  mounted() {
    this.progress = 0.5; // Set initial progress to 0.5
    this.updateProgressBar(this.progress); // Update the progress bar with the initial value
    this.intervalId = setInterval(this.pollStatus, 3000); // Start polling every 3 seconds
  },
  beforeDestroy() {
    clearInterval(this.intervalId); // Clear the interval when the component is destroyed
  }
}
</script>

<style scoped>
.v-card {
  margin-top: 20px;
}
</style>
