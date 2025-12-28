<template>
  <div class="dashboard">
    <h1>Teacher Dashboard</h1>

    <!-- Existing Assignments -->
    <h3>Assignments</h3>
    <div v-if="assignments.length === 0">
      No assignments created yet.
    </div>

    <ul>
      <li v-for="a in assignments" :key="a.id">
        {{ a.subject }} – Exp {{ a.experiment_no }}
      </li>
    </ul>

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

export default {
  name: "TeacherDashboard",
  components: { TeacherRuleBuilder },
  data() {
    return {
      showBuilder: false,
      assignments: [] // later fetched from Firestore
    };
  },
  methods: {
    handleSave(ruleSet) {
      console.log("Rule Set from Builder:", ruleSet);

      // TEMP: add to local list
      this.assignments.push({
        id: Date.now(),
        subject: ruleSet.subject,
        experiment_no: ruleSet.experiment_no,
        rules: ruleSet
      });

      this.showBuilder = false;
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
</style>
