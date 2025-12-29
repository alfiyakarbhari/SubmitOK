<template>
  <div class="page-wrapper">
    <nav class="navbar">
      <h2 class="logo">SubmitOK</h2>
      <button class="back-btn" @click="$router.back()">Back</button>
    </nav>

    <!-- ✅ Teacher name injected here -->
    <h1 class="page-title">
      Assignments by {{ teacherName || "Teacher" }}
    </h1>

    <div v-if="assignments.length > 0" class="assignments-list">
      <ul>
        <li
          v-for="a in assignments"
          :key="a.id"
          class="assignment-item"
        >
          <div class="subject">{{ a.subject }}</div>

          <div class="experiment-no">
            Experiment No: {{ a.experiment_no }}
          </div>

          <!-- ✅ Title is now a clickable link -->
          <router-link
            :to="`/assignment/${a.id}`"
            class="title-link"
          >
            {{ a.experiment }}
          </router-link>
        </li>
      </ul>
    </div>

    <p v-else>No assignments found for this teacher.</p>
  </div>
</template>

<script>
import {
  collection,
  getDocs,
  getDoc,
  doc,
  query,
  where
} from "firebase/firestore";
import { db } from "@/firebase";

export default {
  name: "TeacherAssignments",
  props: ["teacherId"],
  data() {
    return {
      assignments: [],
      teacherName: ""
    };
  },
  async mounted() {
    if (!this.teacherId) return;

    try {
      /* ✅ Fetch teacher name */
      const teacherRef = doc(db, "teachers", this.teacherId);
      const teacherSnap = await getDoc(teacherRef);
      if (teacherSnap.exists()) {
        this.teacherName = teacherSnap.data().name;
      }

      /* ✅ Fetch assignments */
      const assignmentsRef = collection(db, "assignments");
      const q = query(
        assignmentsRef,
        where("teacher_id", "==", this.teacherId)
      );

      const snapshot = await getDocs(q);

      this.assignments = snapshot.docs.map(doc => ({
        id: doc.id,
        experiment: doc.data().title,
        experiment_no: doc.data().experiment_no,
        subject: doc.data().subject
      }));
    } catch (error) {
      console.error("Error fetching assignments:", error);
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
  margin: 20px 0;
}

/* Assignment List */
.assignments-list ul {
  list-style: none;
  padding: 0;
}

/* Assignment Card */
.assignment-item {
  padding: 16px 14px;
  margin-bottom: 14px;
  background-color: #f9f9f9;
  border-radius: 12px;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.05);
}

/* Subject */
.assignment-item .subject {
  font-weight: 600;
  text-transform: uppercase;
  color: #009688;
  margin-bottom: 6px;
  font-size: 0.9rem;
}

/* Experiment Number */
.assignment-item .experiment-no {
  font-size: 0.85rem;
  color: #555;
  margin-bottom: 8px;
}

/* Experiment Title Link */
.title-link {
  font-size: 1.1rem;
  font-weight: 500;
  color: #222;
  text-decoration: none;
}

.title-link:hover {
  color: #009688;
  text-decoration: underline;
}
</style>
