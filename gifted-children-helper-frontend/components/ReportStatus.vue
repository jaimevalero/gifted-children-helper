<template>
  <v-card>
    <v-card-title>{{ title || 'Progreso del informe' }}</v-card-title>
    <v-card-text>
      <!-- Bind progress to model-value -->
      <v-progress-linear indeterminate height="10"></v-progress-linear>
      <div v-html="renderedLog"></div> <!-- Render the Markdown as HTML -->
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
      progress: 0.1, // Initialize progress to 0
      title: '',
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
      console.log('Updating status:', newStatus);
      // Update the progress, title, and log based on the new status
      if (JSON.stringify(newStatus) !== JSON.stringify(this.lastStatus)) {
        if (newStatus.progress !== undefined) {
          console.log('Progress new value:', newStatus.progress);
          this.progress = Math.max(0, Math.min(newStatus.progress, 1)); // Ensure progress is between 0 and 1
          console.log('Progress new value changed', this.progress);
        }
        this.title = newStatus.title || '';
        let logEntry = newStatus.log || '';
        if (!logEntry.endsWith('\n')) {
          logEntry += '\n'; // Ensure the log entry ends with a newline
        }
        this.log += logEntry;
        this.lastStatus = newStatus; // Update the last status
      }
      console.log('Status updated:', newStatus);
      console.log('Progress:', this.progress);

      // print v-progress-linear object
      console.log(this.$refs.progress);

    },
    updateProgressBar(progress) {
      console.log("Actualizando el progreso");
      try {
        console.log(progress);
        // get current value, if not defined, set to 0
        let current_progress = this.progress || 0;
        let new_progress = Math.max(0, Math.min(progress, 1)); // Ensure progress is between 0 and 1

        if (progress < 0 || progress > 1) {
          throw new Error('Progress must be between 0 and 1');
        }
        this.progress = new_progress;
      } catch (error) {
        console.error('Error updating progress:', error);
        this.error = error.message;
        return;
      }
    },
    async pollStatus() {
      try {
        const apiUrl = process.env.VUE_APP_API_URL;
        if (!apiUrl) {
          throw new Error('API URL is not defined in environment variables');
        }
        console.log('Polling status...');
        const response = await fetch(`${apiUrl}/report_status/${this.uuid}`, {
          headers: {
            'Authorization': `Bearer ${this.idToken}` // Send the ID token in the Authorization header
          }
        });
        if (!response.ok) {
          console.error('Failed to fetch report status');
          throw new Error('Failed to fetch report status');
        }
        const data = await response.json();
        console.log(data);
        this.updateStatus(data);
        if (data.progress === 1) {
          console.log('Progress is 1');
          clearInterval(this.intervalId); // Stop polling when progress reaches 1
        }
      } catch (error) {
        console.error('Error fetching report status. Please try again later.');
        this.error = 'Error fetching report status. Please try again later.';
      }
    },
    async fetchReportStatus(uuid) {
      try {
        const apiUrl = process.env.VUE_APP_API_URL;
        console.log('Fetching report status...');
        const response = await fetch(`${apiUrl}/report_status/${uuid}`, {
          headers: {
            'Authorization': `Bearer ${this.idToken}` // Send the ID token in the Authorization header
          }
        });
        if (!response.ok) {
          throw new Error('Failed to fetch report status');
        }
        const status = await response.json();
        console.log(status);
        this.$emit('update:status', status); // Emit the updated status to the parent component
      } catch (error) {
        console.error('Error fetching report status:', error);
        this.error = 'Error fetching report status. Please try again later.';
      }
    },
    convertMarkdownToHtml(markdown) {
      // Simple Markdown to HTML conversion
      // This is a basic implementation and may not cover all Markdown features
      // You can use a library like `markdown-it` for more advanced Markdown parsing
      markdown = markdown.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>'); // Bold text
      markdown = markdown.replace(/\*(.*?)\*/g, '<em>$1</em>'); // Italic text
      markdown = markdown.replace(/`(.*?)`/g, '<code>$1</code>'); // Inline code
      markdown = markdown.replace(/(?:\r\n|\r|\n)/g, '<br>'); // Line breaks
      markdown = markdown.replace(/^-{3,}/g, '<hr>'); // Horizontal rule
      // titles
      markdown = markdown.replace(/^# (.*$)/gim, '<h1>$1</h1>');
      markdown = markdown.replace(/^## (.*$)/gim, '<h2>$1</h2>');
      markdown = markdown.replace(/^### (.*$)/gim, '<h3>$1</h3>');
      markdown = markdown.replace(/^#### (.*$)/gim, '<h4>$1</h4>');
      markdown = markdown.replace(/^##### (.*$)/gim, '<h5>$1</h5>');
      // bold
      markdown = markdown.replace(/\*\*(.*)\*\*/gim, '<strong>$1</strong>');
      markdown = markdown.replace(/\*(.*)\*/gim, '<em>$1</em>');
      // links
      markdown = markdown.replace(/\[(.*?)\]\((.*?)\)/gim, '<a href="$2">$1</a>');
      // lists
      markdown = markdown.replace(/^\*(.*)/gim, '<li>$1</li>');
      markdown = markdown.replace(/^\d\.(.*)/gim, '<li>$1</li>');
      markdown = markdown.replace(/<li>(.*)<\/li>/gim, '<ul><li>$1</li></ul>');
      // subrayado
      markdown = markdown.replace(/__(.*)__/gim, '<u>$1</u>');



      return markdown;
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
