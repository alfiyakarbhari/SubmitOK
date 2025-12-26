<template>
  <div class="login-wrapper">
    <div class="login-card">
      <h1 class="title">Teacher Login</h1>
      <p class="subtitle">
        Welcome back! Please login to manage student submissions.
      </p>

      <form @submit.prevent="handleLogin">
        <div class="form-group">
          <label>Email</label>
          <input
            type="email"
            v-model="email"
            placeholder="teacher@example.com"
            required
          />
        </div>

        <div class="form-group">
          <label>Password</label>
          <input
            type="password"
            v-model="password"
            placeholder="Enter your password"
            required
          />
        </div>

        <button class="login-btn" type="submit">
          Login
        </button>
      </form>

      <p class="footer-text">
        Only authorized faculty members can access this portal.
      </p>
    </div>
  </div>
</template>

<script>
export default {
  name: "TeacherLogin",
  data() {
    return {
      email: "",
      password: "",
      // Hardcoded credentials
      hardcodedEmail: "teacher@submitok.com",
      hardcodedPassword: "teacher123"
    };
  },
  methods: {
    handleLogin() {
  if (
    this.email === this.hardcodedEmail &&
    this.password === this.hardcodedPassword
  ) {
    this.$router.push({ name: "teacher-dashboard" }); // navigate to components/TeacherDashboard.vue
  } else {
    alert("Invalid email or password!");
  }
}
  }
};
</script>

<style scoped>
.login-wrapper {
  min-height: 100vh;
  background-color: var(--bg-color);
  display: flex;
  justify-content: center;
  align-items: center;
  font-family: 'Roboto', sans-serif;
}

.login-card {
  background: var(--card-bg);
  width: 380px;
  padding: 35px;
  border-radius: 16px;
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.12);
  text-align: center;
}

.title {
  font-size: 2rem;
  font-family: 'Montserrat', sans-serif;
  color: var(--primary-color);
  margin-bottom: 8px;
}

.subtitle {
  font-size: 0.95rem;
  color: var(--text-secondary);
  margin-bottom: 25px;
}

.form-group {
  text-align: left;
  margin-bottom: 18px;
}

label {
  font-size: 0.85rem;
  font-weight: 500;
  color: var(--text-primary);
  display: block;
  margin-bottom: 6px;
}

input {
  width: 100%;
  padding: 10px 12px;
  border-radius: 8px;
  border: 1px solid #ccc;
  font-size: 0.95rem;
  transition: border 0.3s;
}

input:focus {
  outline: none;
  border-color: var(--primary-color);
}

.login-btn {
  width: 100%;
  margin-top: 10px;
  padding: 12px;
  border: none;
  border-radius: 8px;
  background: var(--primary-color);
  color: white;
  font-size: 1rem;
  font-family: 'Roboto', sans-serif;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
}

.login-btn:hover {
  background: #00796b; /* Slightly darker Teal for hover */
  transform: translateY(-1px);
}

.footer-text {
  margin-top: 20px;
  font-size: 0.8rem;
  color: var(--text-muted);
}
</style>
