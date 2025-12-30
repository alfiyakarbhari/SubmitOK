<template>
  <div class="page">
    <h2>Submissions</h2>

    <div v-if="submissions.length === 0">
      No submissions yet.
    </div>

    <div
      v-for="s in submissions"
      :key="s.id"
      class="submission-card"
    >
      <p><b>Student ID:</b> {{ s.student_id }}</p>
      <p><b>Status:</b> {{ s.status }}</p>
      <p><b>Grade:</b> {{ s.grade ?? "Not graded" }}</p>

      <button type="button" @click="downloadFile(s.file_url)">
  View File
</button>


      <div class="grade-box">
        <input
          type="number"
          v-model="s.tempGrade"
          placeholder="Enter grade"
        />
        <button @click="gradeSubmission(s)">
          Submit Grade
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      submissions: []
    };
  },
  async mounted() {
    const assignmentId = this.$route.params.assignmentId;

    const res = await axios.get(
      `http://127.0.0.1:8000/assignment-submissions/${assignmentId}`
    );

    this.submissions = res.data.map(s => ({
      ...s,
      tempGrade: ""
    }));
  },
  methods: {
    async gradeSubmission(s) {
      await axios.post(
        "http://127.0.0.1:8000/grade-submission",
        new URLSearchParams({
          submission_id: s.id,
          grade: s.tempGrade
        })
      );

      s.grade = s.tempGrade;
      s.status = "graded";
    },
    downloadFile(url) {
  const link = document.createElement("a");
  link.href = url + "?fl_attachment=true";
  link.setAttribute("download", "");
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
}

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

.grade-box {
  margin-top: 10px;
  display: flex;
  gap: 10px;
}
</style>
