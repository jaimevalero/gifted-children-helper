<template>
  <v-card>
    <v-card-title>{{ title }}</v-card-title>
    <v-card-text>
      <v-progress-linear :value="progress" height="10"></v-progress-linear>
      <v-textarea
        v-model="log"
        label="Report Status Log"
        rows="10"
        readonly
      ></v-textarea>
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
    }
  },
  data() {
    return {
      progress: 0,
      title: 'Report Status',
      log: '',
      intervalId: null // Add an interval ID to manage the polling
    };
  },
  watch: {
    status(newStatus) {
      this.updateStatus(newStatus);
    }
  },
  methods: {
    updateStatus(newStatus) {
      // Update the progress, title, and log based on the new status
      this.progress = newStatus.progress;
      this.title = newStatus.title;
      this.log += `${newStatus.text}\n`;
    },
    async pollStatus() {
      try {
        const apiUrl = process.env.VUE_APP_API_URL;
        if (!apiUrl) {
          throw new Error('API URL is not defined in environment variables');
        }

        console.log('Polling status for uuid:', this.status.uuid);
        const response = await fetch(`${apiUrl}/report_status/${this.status.uuid}`);
        const data = await response.json();
        this.updateStatus(data);
        if (data.progress === 1) {
          clearInterval(this.intervalId); // Stop polling when progress reaches 1
        }
      } catch (error) {
        console.error('Error polling status:', error);
      }
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
