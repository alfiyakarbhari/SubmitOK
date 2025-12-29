<template>
  <div class="welcome-container">
    <h1 class="title">Welcome to SubmitOK</h1>
    <p class="subtitle">
      Smart Academic Submission & Compliance System
    </p>

    <div class="button-group">
      <button class="btn user-btn" @click="goToUserLogin">
        Login as User
      </button>

      <button class="btn teacher-btn" @click="goToTeacherLogin">
        Login as Teacher
      </button>
    </div>
  </div>
</template>

<script>
export default {
  name: "MainWelcome",
  methods: {
  goToUserLogin() {
    this.$router.push("/login");
  },
  goToTeacherLogin() {
    this.$router.push("/login/teacher");
  }
}
};
</script>

<style scoped>
.welcome-container {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  background: #f7f9fc;
  text-align: center;
}

.title {
  font-size: 2.5rem;
  margin-bottom: 10px;
  color: #222;
}

.subtitle {
  font-size: 1.1rem;
  color: #555;
  margin-bottom: 40px;
}

.button-group {
  display: flex;
  gap: 20px;
}

.btn {
  padding: 12px 28px;
  font-size: 1rem;
  border-radius: 8px;
  border: none;
  cursor: pointer;
  transition: 0.3s ease;
}

.user-btn {
  background-color: #009688;
  color: white;
}

.teacher-btn {
  background-color: #3f51b5;
  color: white;
}

.btn:hover {
  opacity: 0.9;
  transform: translateY(-2px);
}
</style>
