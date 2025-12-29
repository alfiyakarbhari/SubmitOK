<template>
  <div class="verify-page">
    <div class="verify-card">
      <h2>Email Verification</h2>

      <p v-if="loading">Verifying your email, please wait...</p>
      <p v-if="success">✅ Your email has been verified! You can now <router-link to="/login">login</router-link>.</p>
      <p v-if="error" style="color:red">{{ error }}</p>
    </div>
  </div>
</template>

<script>
import { getAuth, applyActionCode } from "firebase/auth";
import { doc, updateDoc } from "firebase/firestore";
import { db } from "@/firebase";

export default {
  name: "VerifyEmail",
  data() {
    return {
      loading: true,
      success: false,
      error: ""
    };
  },
  async mounted() {
    this.loading = true;
    const auth = getAuth();

    // Get oobCode from URL
    const urlParams = new URLSearchParams(window.location.search);
    const oobCode = urlParams.get("oobCode");

    if (!oobCode) {
      this.error = "Invalid verification link.";
      this.loading = false;
      return;
    }

    try {
      // Apply the verification code to verify the email
      await applyActionCode(auth, oobCode);

      // Get current user and update Firestore
      const user = auth.currentUser;
      if (user) {
        const userDocRef = doc(db, "users", user.uid);
        await updateDoc(userDocRef, { verified: true });
      }

      this.success = true;
      this.loading = false;
    } catch (err) {
      this.error = err.message;
      this.loading = false;
    }
  }
};
</script>

<style scoped>
.verify-page {
  min-height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
}

.verify-card {
  background: var(--card-bg);
  padding: 32px;
  width: 380px;
  border-radius: 16px;
  box-shadow: 0 20px 40px rgba(0,0,0,0.12);
  text-align: center;
}

h2 {
  font-family: Montserrat;
  margin-bottom: 20px;
}

p {
  font-family: Roboto;
  font-size: 16px;
}
</style>
