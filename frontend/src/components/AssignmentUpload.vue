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
        <input type="file" class="file-input" />
      </div>

      <!-- Buttons -->
      <div class="button-group">
        <button class="check-btn">Check</button>
        <button class="submit-btn">Submit</button>
      </div>
    </div>
  </div>
</template>

<script>
import { doc, getDoc } from "firebase/firestore";
import { db } from "@/firebase";

export default {
  name: "AssignmentUpload",
  data() {
    return {
      assignment: null
    };
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
</style>
