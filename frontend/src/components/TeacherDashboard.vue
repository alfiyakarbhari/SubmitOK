<template>
  <div class="dashboard-wrapper">
    <h1 class="dashboard-title">Teacher Dashboard</h1>
    <p class="subtitle">Manage and view all teachers</p>

    <div class="grid">
      <!-- Teacher Cards -->
      <TeacherCard 
        v-for="t in teachers" 
        :key="t.id" 
        :teacher="t" 
        @click="goToTeacherPage(t)" 
      />

      <!-- Add Teacher Card -->
      <div class="card add-card" @click="showModal = true">
        <span class="material-icons plus-icon">add</span>
        <p>Add Teacher</p>
      </div>
    </div>

    <!-- Add Teacher Modal -->
    <AddTeacherModal 
      :show="showModal" 
      @close="showModal = false" 
      @create="addTeacher"
    />
  </div>
</template>

<script>
import TeacherCard from '../components/TeacherCard.vue'
import AddTeacherModal from '../components/AddTeacherModal.vue'
import { collection, getDocs } from "firebase/firestore";
import { db } from "@/firebase";
export default {
  components: { TeacherCard, AddTeacherModal },
  data() {
    return {
      showModal: false,
      teachers: [
        
      ]
    }
  },
  methods: {
    // Navigate to teacher page (can integrate router later)
    goToTeacherPage(teacher) {
      alert(`Navigate to ${teacher.name}'s page`);
      // Example: this.$router.push(`/teacher/${teacher.id}`)
      this.$router.push(`/teacher/${teacher.id}`);

    },

    // Add new teacher
    addTeacher(newTeacher) {
      const id = this.teachers.length + 1;
      this.teachers.push({ 
        id, 
        name: `${newTeacher.firstName} ${newTeacher.lastName}`,
        email: `${newTeacher.firstName}.${newTeacher.lastName}`.toLowerCase() + '@school.com'
      });
    }
  },
  async mounted() {
  const snapshot = await getDocs(collection(db, "teachers"));
  this.teachers = snapshot.docs.map(doc => ({
    id: doc.id,
    ...doc.data()
  }));
}
}
</script>

<style scoped>
/* Dashboard Wrapper */
.dashboard-wrapper {
  padding: 30px;
  font-family: 'Roboto', sans-serif;
  background-color: var(--bg-color);
}

/* Titles */
.dashboard-title {
  font-family: 'Montserrat', sans-serif;
  font-weight: 600;
  font-size: 2rem;
  color: var(--primary-color);
  margin-bottom: 5px;
}

.subtitle {
  color: var(--text-secondary);
  margin-bottom: 20px;
}

/* Grid for teacher cards */
.grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(180px, 1fr));
  gap: 20px;
}

/* Add Teacher Card */
.add-card {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  background: var(--accent-color);
  color: white;
  cursor: pointer;
  border-radius: 14px;
  padding: 20px;
  box-shadow: 0 10px 25px rgba(0,0,0,0.1);
  transition: transform 0.2s, box-shadow 0.2s;
}

.add-card:hover {
  transform: translateY(-3px);
  box-shadow: 0 15px 30px rgba(0,0,0,0.15);
}

/* Plus Icon */
.plus-icon {
  font-size: 3rem;
  font-weight: bold;
  line-height: 1;
}

.add-card p {
  font-size: 1rem;
  margin-top: 10px;
}
</style>
