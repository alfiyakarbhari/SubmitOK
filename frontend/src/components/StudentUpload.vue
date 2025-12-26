<template>
  <div class="container">
    <h2>Student Assignment Upload</h2>

    <!-- File Input -->
    <input type="file" @change="handleFileChange" />
    <br /><br />

    <!-- Upload Button -->
    <button :disabled="!selectedFile" @click="uploadFile">
      Upload & Parse
    </button>

    <p v-if="loading">Parsing document...</p>
    <p v-if="error" style="color: red">{{ error }}</p>

    <!-- Result -->
    <div v-if="result" class="result">
      <h3>Parsed Document Result</h3>
      <pre>{{ result }}</pre>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "StudentUpload",
  data() {
    return {
      selectedFile: null,
      result: null,
      loading: false,
      error: null
    };
  },
  methods: {
    handleFileChange(event) {
      this.selectedFile = event.target.files[0];
      this.result = null;
      this.error = null;
    },

    async uploadFile() {
      if (!this.selectedFile) return;

      this.loading = true;
      this.error = null;

      const formData = new FormData();
      formData.append("file", this.selectedFile);

      try {
        const response = await axios.post(
          "http://127.0.0.1:8000/parse",
          formData,
          {
            headers: {
              "Content-Type": "multipart/form-data"
            }
          }
        );

        this.result = JSON.stringify(response.data, null, 2);
      } catch (err) {
        this.error = "Failed to parse document";
        console.error(err);
      } finally {
        this.loading = false;
      }
    }
  }
};
</script>

<style scoped>
.container {
  max-width: 600px;
  margin: 40px auto;
  padding: 20px;
  border: 1px solid #ddd;
  border-radius: 8px;
}

button {
  padding: 8px 16px;
  cursor: pointer;
}

.result {
  margin-top: 20px;
  background: #f5f5f5;
  padding: 10px;
  border-radius: 4px;
}
</style>
