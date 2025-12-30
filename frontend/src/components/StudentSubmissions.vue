<template>
  <div class="page">
    <h2>My Submissions</h2>

    <div v-if="submissions.length === 0">
      No submissions yet.
    </div>

    <div
      v-for="s in submissions"
      :key="s.id"
      class="submission-card"
    >
      <p><b>Assignment:</b> {{ s.assignment_id }}</p>
      <p><b>Status:</b> {{ s.status }}</p>
      <p><b>Grade:</b> {{ s.grade ?? "Not graded" }}</p>

    <button type="button" @click="downloadFile(s.file_url)">
  Download File
</button>


    </div>
  </div>
</template>

<script>
import axios from "axios";
import { auth } from "@/firebase";

export default {
  data() {
    return {
      submissions: []
    };
  },
  
  methods: {
 downloadFile(url) {
  const link = document.createElement("a");
  link.href = url + "?fl_attachment=true";
  link.setAttribute("download", "");
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
}

}


,
  async mounted() {
    const user = auth.currentUser;
    if (!user) return;

    const res = await axios.get(
      `http://127.0.0.1:8000/student-submissions/${user.uid}`
    );
    this.submissions = res.data;
  }
};
</script>

<style scoped>
.page {
  padding: 30px;
}
.submission-card {
  border: 1px solid #ddd;
  padding: 15px;
  margin-bottom: 12px;
  border-radius: 8px;
}
</style>
