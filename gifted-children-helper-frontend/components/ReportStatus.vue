<template>
  <v-card>
    <v-card-title>{{ title || 'Report Status' }}</v-card-title>
    <v-card-text>
      <v-progress-linear :value="progress" height="10"></v-progress-linear>
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
        }
        this.title = newStatus.title || 'Report Status';
        let logEntry = newStatus.log || '';
        if (!logEntry.endsWith('\n')) {
          logEntry += '\n'; // Ensure the log entry ends with a newline
        }
        this.log += logEntry;
        this.lastStatus = newStatus; // Update the last status
      }
    },
    async pollStatus() {
      try {
        const apiUrl = process.env.VUE_APP_API_URL;
        if (!apiUrl) {
          throw new Error('API URL is not defined in environment variables');
        }

        console.log('Polling status for uuid:', this.uuid);
        const response = await fetch(`${apiUrl}/report_status/${this.uuid}`);
        if (!response.ok) {
          throw new Error('Failed to fetch report status');
        }
        const data = await response.json();
        this.updateStatus(data);
        if (data.progress === 1) {
          clearInterval(this.intervalId); // Stop polling when progress reaches 1
        }
      } catch (error) {
        console.error('Error polling status:', error);
        this.error = 'Error fetching report status. Please try again later.';
      }
    },
    async fetchReportStatus(uuid) {
      try {
        const apiUrl = process.env.VUE_APP_API_URL;
        const response = await fetch(`${apiUrl}/report_status/${uuid}`);
        if (!response.ok) {
          throw new Error('Failed to fetch report status');
        }
        const status = await response.json();
        this.$emit('update:status', status); // Emit the updated status to the parent component
      } catch (error) {
        console.error('Error fetching report status:', error);
        this.error = 'Error fetching report status. Please try again later.';
      }
    },
    convertMarkdownToHtml(markdown) {
      // Simple Markdown to HTML conversion
      return markdown
        .replace(/^### (.*$)/gim, '<h3>$1</h3>') // Replace level 3 headers
        .replace(/^## (.*$)/gim, '<h2>$1</h2>')  // Replace level 2 headers
        .replace(/^# (.*$)/gim, '<h1>$1</h1>')   // Replace level 1 headers
        .replace(/^\> (.*$)/gim, '<blockquote>$1</blockquote>') // Replace blockquotes
        .replace(/\*\*(.*)\*\*/gim, '<b>$1</b>') // Replace bold text
        .replace(/\*(.*?)\*/gim, '<i>$1</i>')    // Replace italic text, non-greedy
        .replace(/\n$/gim, '<br />')             // Replace new lines with <br />
        .replace(/[#*]/g, '');                   // Remove all '#' and '*' characters

    }
  },
  mounted() {
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
