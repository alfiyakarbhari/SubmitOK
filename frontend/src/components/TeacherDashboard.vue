<template>
  <div class="dashboard-wrapper">
    <!-- Navbar -->
    <nav class="navbar">
      <h2 class="logo">SubmitOK</h2>
      <button class="logout-btn" @click="logout">Logout</button>
    </nav>

    <!-- Dashboard Content -->
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
import { collection, getDocs, addDoc } from "firebase/firestore";
import { db, auth } from "@/firebase";
import { signOut } from "firebase/auth";

export default {
  components: { TeacherCard, AddTeacherModal },
  data() {
    return {
      showModal: false,
      teachers: []
    }
  },
  methods: {
    // Navigate to teacher page
    goToTeacherPage(teacher) {
      alert(`Navigate to ${teacher.name}'s page`);
      this.$router.push(`/teacher/${teacher.id}`);
    },

    // Add new teacher
    async addTeacher(newTeacher) {
      const fullName = `${newTeacher.firstName} ${newTeacher.lastName}`;
      const email =
        `${newTeacher.firstName}.${newTeacher.lastName}`.toLowerCase() +
        "@school.com";
      const department = newTeacher.department;

      // Save to Firestore
      const docRef = await addDoc(collection(db, "teachers"), {
        name: fullName,
        email: email,
        department: department
      });

      // Update UI
      this.teachers.push({
        id: docRef.id,
        name: fullName,
        email: email,
        department: department
      });

      // Close modal
      this.showModal = false;
    },

    // Logout
    async logout() {
      try {
        await signOut(auth);
        this.$router.push("/login/teacher"); // Redirect to teacher login
      } catch (error) {
        console.error("Logout error:", error);
      }
    }
  },
  async mounted() {
    // Fetch teachers from Firestore
    const snapshot = await getDocs(collection(db, "teachers"));
    this.teachers = snapshot.docs.map(doc => ({
      id: doc.id,
      ...doc.data()
    }));
  }
};
</script>

<style scoped>
/* Navbar with pastel color */
.navbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px 30px;
  background-color: #B2DFDB; /* pastel teal */
  border-bottom: 1px solid #ddd;
  border-radius: 0 0 14px 14px;
  margin-bottom: 20px;
}

.logo {
  font-family: 'Montserrat', sans-serif;
  font-weight: 600;
  font-size: 1.5rem;
  color: var(--primary-color);
  margin: 0;
}

.logout-btn {
  padding: 8px 16px;
  background-color: #FFC107;
  color: #000;
  border: none;
  border-radius: 8px;
  font-weight: 500;
  cursor: pointer;
  transition: background 0.2s;
}

.logout-btn:hover {
  background-color: #e0a800;
}

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
  color: black;
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
