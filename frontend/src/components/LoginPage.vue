<template> 
  <div class="auth-page">
    <div class="auth-card">
      <h2>Login</h2>

      <input v-model="email" placeholder="Email" />
      <input v-model="password" type="password" placeholder="Password" />

      <button @click="login">Login</button>

      <p class="switch-auth">
        Don’t have an account?
        <router-link to="/signup" class="signup-link">Create account</router-link>
      </p>
    </div>
  </div>
</template>

<script>
import { signInWithEmailAndPassword } from "firebase/auth";
import { auth, db } from "@/firebase";
import { doc, getDoc, updateDoc } from "firebase/firestore";

export default {
  name: "LoginPage",
  data() {
    return {
      email: "",
      password: ""
    };
  },
  methods: {
    async login() {
  if (!this.email || !this.password) {
    alert("Email and password required");
    return;
  }

  try {
    // Sign in with Firebase Auth
    const userCred = await signInWithEmailAndPassword(auth, this.email, this.password);
    const user = userCred.user;

    // Check if email is verified
    if (!user.emailVerified) {
      alert("Please verify your email before logging in.");
      return;
    }

    // OPTIONAL: Update Firestore verified field if not already true
    const userDocRef = doc(db, "users", user.uid);
    const userSnapshot = await getDoc(userDocRef);

    if (userSnapshot.exists() && !userSnapshot.data().verified) {
      await updateDoc(userDocRef, { verified: true });
    }

    // Redirect to User Dashboard
    this.$router.push("/dashboard/user");

  } catch (error) {
    alert("Invalid email or password");
  }
}

  }
};
</script>

<style scoped>
.auth-page {
  min-height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
}

.auth-card {
  background: var(--card-bg);
  padding: 32px;
  width: 360px;
  border-radius: 16px;
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.12);
}

h2 {
  text-align: center;
  margin-bottom: 20px;
  font-family: Montserrat;
}

input {
  width: 100%;
  padding: 10px;
  margin-bottom: 14px;
  border-radius: 8px;
  border: 1px solid #ccc;
  font-family: Roboto;
}

input:focus {
  outline: none;
  border-color: var(--primary-color);
}

button {
  width: 100%;
  padding: 10px;
  background: #FFC107;
  color: #000;
  border: none;
  border-radius: 8px;
  font-weight: 500;
  cursor: pointer;
  transition: background 0.2s;
}

button:hover {
  background: #e0a800;
}

.switch-auth {
  margin-top: 16px;
  text-align: center;
  font-size: 14px;
  color: var(--text-secondary);
}

.signup-link {
  color: var(--primary-color);
  font-weight: 500;
  cursor: pointer;
  text-decoration: none;
  margin-left: 4px;
}

.signup-link:hover {
  text-decoration: underline;
}
</style>
