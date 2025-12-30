<template>
  <div class="dashboard">
    <h1>Teacher Dashboard</h1>

    <!-- Existing Assignments -->
    <h3>Assignments</h3>
    <div v-if="assignments.length === 0">
      No assignments created yet.
    </div>

   <div v-for="a in assignments" :key="a.id" class="assignment-card">
   <button @click="viewSubmissions(a.id)">
  View Submissions
</button>

  <h3>
    {{ a.subject }} – Exp {{ a.experiment_no }}
  </h3>

  <table class="rules-table">
    <thead>
      <tr>
        <th>Section</th>
        <th>Requirement</th>
      </tr>
    </thead>
    <tbody>
      <tr v-for="row in formatRules(a.rules)" :key="row.label">
        <td>{{ row.label }}</td>
        <td>{{ row.value }}</td>
      </tr>
    </tbody>
  </table>
</div>


    <!-- Create Assignment Button -->
    <button class="create-btn" @click="showBuilder = true">
      + Create Assignment
    </button>

    <!-- Rule Builder Modal -->
    <div v-if="showBuilder" class="modal-overlay">
      <div class="modal">
        <TeacherRuleBuilder @save="handleSave" @close="showBuilder = false" />
      </div>
    </div>
  </div>
</template>

<script>
import TeacherRuleBuilder from "@/components/TeacherRuleBuilder.vue";
import { collection, addDoc, getDocs, query, where } from "firebase/firestore";
import { db } from "@/firebase";


export default {
  name: "TeacherDashboard",
  components: { TeacherRuleBuilder },
  data() {
    return {
      showBuilder: false,
      assignments: [] 
    };
  },
  mounted() {
  this.fetchAssignments();
}
,
  methods: {
    async handleSave(ruleSet) {
  await addDoc(collection(db, "assignments"), {
    teacher_id: this.teacherId,
    subject: ruleSet.subject,
    experiment_no: ruleSet.experiment_no,
    title: ruleSet.experiment,
    rules: ruleSet,
    created_at: new Date(),
    active: true
  });

  this.showBuilder = false;
  this.fetchAssignments(); // refresh list
},
viewSubmissions(assignmentId) {
  this.$router.push(`/teacher/assignment/${assignmentId}/submissions`);
}
,
async fetchAssignments() {
    const q = query(
      collection(db, "assignments"),
      where("teacher_id", "==", this.teacherId)
    );

    const snapshot = await getDocs(q);
    this.assignments = snapshot.docs.map(doc => ({
      id: doc.id,
      ...doc.data()
    }));
  },
  formatRules(rules) {
    const rows = [];

    if (rules.aim?.required)
      rows.push({ label: "Aim", value: "Required" });

    if (rules.theory?.required)
      rows.push({
        label: "Theory",
        value: `${rules.theory.min_words}–${rules.theory.max_words} words`
      });

    if (rules.code?.required) {
      let val = "Required";
      if (rules.code.check_comments) val += ", comments";
      if (rules.code.check_indentation) val += ", indentation";
      rows.push({ label: "Code", value: val });
    }

    if (rules.output?.required)
      rows.push({
        label: "Output",
        value: rules.output.type.replaceAll("_", " ")
      });

    if (rules.methodology?.required)
      rows.push({
        label: "Methodology",
        value: rules.methodology.formats.join(" / ")
      });

    if (rules.conclusion?.required)
      rows.push({
        label: "Conclusion",
        value: `${rules.conclusion.min_words}–${rules.conclusion.max_words} words`
      });

    rows.push({
      label: "Plagiarism Threshold",
      value: `${rules.plagiarism_threshold}%`
    });

    return rows;
  }
  },
  computed: {
  teacherId() {
    return this.$route.params.teacherId;
  }
}

};
</script>

<style scoped>
.dashboard {
  padding: 30px;
}

.create-btn {
  margin-top: 20px;
  padding: 10px 16px;
  background: #4f46e5;
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
}

.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0,0,0,0.4);
  display: flex;
  align-items: center;
  justify-content: center;
}

.modal {
  background: white;
  width: 80%;
  max-height: 90vh;
  overflow-y: auto;
  border-radius: 10px;
  padding: 20px;
}
.assignment-card {
  margin: 20px 0;
  padding: 15px;
  border-radius: 10px;
  background: #fafafa;
  box-shadow: 0 4px 10px rgba(0,0,0,0.05);
}

.rules-table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 10px;
}

.rules-table th,
.rules-table td {
  border: 1px solid #ddd;
  padding: 8px;
  text-align: left;
}

.rules-table th {
  background-color: #f0f0f0;
}

</style>
