<template>
  <div class="page-wrapper">
    <nav class="navbar">
      <h2 class="logo">SubmitOK</h2>
      <button class="back-btn" @click="$router.back()">Back</button>
    </nav>

    <h1 class="page-title">Upload Assignment</h1>

    <!-- ✅ Assignment Info -->
    <div class="assignment-info" v-if="assignment">
      <div class="experiment-no">
        Experiment No: {{ assignment.experiment_no }}
      </div>
      <div class="experiment-title">
        {{ assignment.title }}
      </div>
    </div>

    <div class="upload-card">
      <!-- File input -->
      <div class="form-group">
        <label class="label">Select File</label>
        <input
  type="file"
  class="file-input"
  @change="e => selectedFile = e.target.files[0]"
/>

      </div>

      <!-- Buttons -->
      <div class="button-group">
        <button class="check-btn" @click="checkSubmission">Check</button>
<button
  class="submit-btn"
  :disabled="!canSubmit || submitted"
  @click="submitAssignment"
>
  Submit
</button>



      </div>
      <div v-if="validationReport">
  <h3>Validation Report</h3>
  <p>Acceptance Score: {{ validationReport.acceptance_score }}%</p>

  <ul>
    <li v-for="(v, k) in validationReport.results" :key="k">
      {{ k }} → {{ v }}
    </li>
  </ul>
</div>
<div v-if="aiSuggestions && aiSuggestions.length">
  <h3>✨ How to Improve Your Submission</h3>

  <div
    v-for="section in aiSuggestions"
    :key="section.rule"
    class="suggestion-section"
  >
    <h4>{{ section.title }}</h4>

    <ul>
      <li v-for="(tip, i) in section.tips" :key="i">
        {{ tip }}
      </li>
    </ul>
  </div>
</div>


    </div>
  </div>
</template>

<script>
import { doc, getDoc } from "firebase/firestore";
import { db } from "@/firebase";
import axios from "axios";
import { auth } from "@/firebase";

export default {
  name: "AssignmentUpload",
  data() {
  return {
    assignment: null,
    selectedFile: null,
    validationReport: null,
    canSubmit: false,
    submitted: false,
    aiSuggestions: [],

  };
}
,
methods: {
  async checkSubmission() {
  if (!this.selectedFile) return;

  const formData = new FormData();
  formData.append("file", this.selectedFile);
  formData.append("assignment_id", this.$route.params.id);

  const res = await axios.post(
    "http://127.0.0.1:8000/check-submission",
    formData
  );

  this.validationReport = res.data.validation_report;
  this.aiSuggestions = res.data.ai_suggestions || [];  // ✅ ADD THIS
  this.canSubmit = this.validationReport.accepted === true;
}
,
  async submitAssignment() {
  if (!this.selectedFile || !this.canSubmit) return;

  const user = auth.currentUser;

  if (!user) {
    alert("User not logged in");
    return;
  }

  const studentId = user.uid; // 🔥 THIS is the Firestore document ID

  try {
    const formData = new FormData();
    formData.append("file", this.selectedFile);
    formData.append("assignment_id", this.$route.params.id);
    formData.append("student_id", studentId);

    const res = await axios.post(
      "http://127.0.0.1:8000/submit-submission",
      formData,
      { headers: { "Content-Type": "multipart/form-data" } }
    );

    alert("Assignment submitted successfully!");
    this.submitted = true;

this.$router.push("/student/submissions");

    console.log(res.data);

  } catch (err) {
    console.error(err);
    alert(err.error);
  }
}

},
  async mounted() {
    try {
      const assignmentId = this.$route.params.id;
      if (!assignmentId) return;

      const assignmentRef = doc(db, "assignments", assignmentId);
      const assignmentSnap = await getDoc(assignmentRef);

      if (assignmentSnap.exists()) {
        this.assignment = assignmentSnap.data();
      }
    } catch (error) {
      console.error("Error fetching assignment:", error);
    }
  }
};
</script>

<style scoped>
.page-wrapper {
  padding: 30px;
  font-family: 'Roboto', sans-serif;
}

/* Navbar */
.navbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background-color: #B2DFDB;
  padding: 16px 30px;
  border-radius: 0 0 14px 14px;
}

.logo {
  font-family: 'Montserrat', sans-serif;
  font-weight: 600;
  font-size: 1.5rem;
  color: #009688;
}

.back-btn {
  padding: 8px 16px;
  background-color: #FFC107;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-weight: 500;
}

/* Title */
.page-title {
  font-family: 'Montserrat', sans-serif;
  font-weight: 600;
  color: #009688;
  margin: 30px 0 10px;
  text-align: center;
}

/* Assignment Info */
.assignment-info {
  text-align: center;
  margin-bottom: 20px;
}

.assignment-info .experiment-no {
  font-size: 0.9rem;
  color: #555;
  margin-bottom: 6px;
}

.assignment-info .experiment-title {
  font-size: 1.2rem;
  font-weight: 600;
  color: #222;
}

/* Upload Card */
.upload-card {
  max-width: 420px;
  margin: 0 auto;
  padding: 24px;
  background-color: #f9f9f9;
  border-radius: 14px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.08);
}

/* Form */
.form-group {
  margin-bottom: 20px;
}

.label {
  display: block;
  margin-bottom: 8px;
  font-weight: 500;
  color: #333;
}

.file-input {
  width: 100%;
}

/* Buttons */
.button-group {
  display: flex;
  justify-content: space-between;
  gap: 12px;
}

.check-btn,
.submit-btn {
  flex: 1;
  padding: 10px;
  border: none;
  border-radius: 8px;
  font-weight: 500;
  cursor: pointer;
}

.check-btn {
  background-color: #B2DFDB;
}

.submit-btn {
  background-color: #FFC107;
}
.suggestion-section {
  margin-top: 16px;
}

.suggestion-section h4 {
  margin-bottom: 8px;
  color: #333;
  font-weight: 600;
}

.suggestion-section ul {
  padding-left: 18px;
}

.suggestion-section li {
  margin-bottom: 6px;
  line-height: 1.4;
}

</style>
