<template>
  <div class="dashboard-wrapper">
    <!-- Navbar -->
    <nav class="navbar">
      <h2 class="logo">SubmitOK</h2>
      <button class="logout-btn" @click="logout">Logout</button>
    </nav>

    <!-- Dashboard Content -->
    <h1 class="dashboard-title">Welcome to SubmitOK</h1>
    <p class="subtitle">Here are the teachers:</p>

    <div class="grid">
      <!-- Teacher Cards for Users (click disabled) -->
      <UserTeacherCard 
        v-for="t in teachers" 
        :key="t.id" 
        :teacher="t" 
        @click="$router.push(`/teacher-assignments/${t.id}`)"
      />
    </div>
  </div>
</template>

<script>
import UserTeacherCard from '../components/UserTeacherCard.vue';
import { collection, getDocs } from "firebase/firestore";
import { db, auth } from "@/firebase";
import { signOut } from "firebase/auth";

export default {
  name: "UserDashboard",
  components: { UserTeacherCard },
  data() {
    return {
      teachers: []
    };
  },
  async mounted() {
    // Fetch teachers from Firestore
    const snapshot = await getDocs(collection(db, "teachers"));
    this.teachers = snapshot.docs.map(doc => ({
      id: doc.id,
      name: doc.data().name,
      department: doc.data().department
      // Do not include email
    }));
  },
  methods: {
    async logout() {
      try {
        await signOut(auth);
        this.$router.push("/login");
      } catch (error) {
        console.error("Logout error:", error);
      }
    }
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
</style>
