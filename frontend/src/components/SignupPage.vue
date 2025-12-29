<template>
  <div class="auth-page">
    <div class="auth-card">
      <h2>Create Account</h2>

      <input v-model="username" placeholder="Username" />
      <input v-model="email" placeholder="Email" />
      <input v-model="password" type="password" placeholder="Password" />

      <button @click="signup">Create Account</button>
      <p class="hint">Username must be unique</p>

      <p class="switch-auth">
        Already have an account?
        <router-link to="/login" class="login-link">Login</router-link>
      </p>
    </div>
  </div>
</template>

<script>
import { 
  createUserWithEmailAndPassword, 
  sendEmailVerification 
} from "firebase/auth";
import { 
  collection, 
  query, 
  where, 
  getDocs, 
  doc, 
  setDoc 
} from "firebase/firestore";
import { auth, db } from "@/firebase";

export default {
  name: "SignupPage",
  data() {
    return {
      email: "",
      password: "",
      username: ""
    };
  },
  methods: {
    async signup() {
      const email = this.email.trim();
      const username = this.username.trim();
      const password = this.password;

      if (!email || !username || !password) {
        alert("All fields are required");
        return;
      }

      if (password.length < 6) {
        alert("Password must be at least 6 characters");
        return;
      }

      try {
        // Check if username exists
        const q = query(collection(db, "users"), where("username", "==", username));
        const snapshot = await getDocs(q);
        if (!snapshot.empty) {
          alert("Username already taken");
          return;
        }

        // Create Firebase Auth user
        const userCred = await createUserWithEmailAndPassword(auth, email, password);
        const uid = userCred.user.uid;

        // Send email verification
        await sendEmailVerification(userCred.user);

        // Save user in Firestore with verified flag
        await setDoc(doc(db, "users", uid), {
          email,
          username,
          created_at: new Date(),
          verified: false
        });

        alert("Account created! Please check your email to verify your account.");
        this.$router.push("/login");

      } catch (error) {
        if (error.code === "auth/email-already-in-use") {
          alert("Email already registered");
        } else if (error.code === "auth/weak-password") {
          alert("Password should be at least 6 characters");
        } else {
          alert(error.message);
        }
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
  width: 380px;
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
  background: #FFC107; /* Amber button */
  color: #000;
  border: none;
  border-radius: 8px;
  font-family: Roboto;
  font-weight: 500;
  cursor: pointer;
  transition: background 0.2s;
}

button:hover {
  background: #e0a800; /* Slightly darker amber */
}

.hint {
  text-align: center;
  color: var(--text-muted);
  margin-top: 10px;
  font-size: 13px;
}

.switch-auth {
  margin-top: 16px;
  text-align: center;
  font-size: 14px;
  color: var(--text-secondary);
}

.login-link {
  color: var(--primary-color);
  font-weight: 500;
  cursor: pointer;
  text-decoration: none;
  margin-left: 4px;
}

.login-link:hover {
  text-decoration: underline;
}
</style>
