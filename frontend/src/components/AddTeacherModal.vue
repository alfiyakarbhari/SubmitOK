<template>
  <div class="modal-backdrop" v-if="show">
    <div class="modal-card">
      <h2>Add New Teacher</h2>
      <form @submit.prevent="createTeacher">
        <div class="form-group">
          <label>First Name</label>
          <input type="text" v-model="firstName" placeholder="First Name" required pattern="[A-Za-z]+" />
        </div>
        <div class="form-group">
          <label>Last Name</label>
          <input type="text" v-model="lastName" placeholder="Last Name" required pattern="[A-Za-z]+" />
        </div>
        <button type="submit">Create Teacher</button>
        <button type="button" class="cancel-btn" @click="$emit('close')">Cancel</button>
      </form>
    </div>
  </div>
</template>

<script>
export default {
  name: "AddTeacherModal",
  props: ['show'],
  data() {
    return {
      firstName: '',
      lastName: ''
    }
  },
  methods: {
    createTeacher() {
      if (!this.firstName || !this.lastName) return;
      this.$emit('create', {
        name: `${this.firstName} ${this.lastName}`
      });
      this.firstName = '';
      this.lastName = '';
      this.$emit('close');
    }
  }
}
</script>

<style scoped>
.modal-backdrop {
  position: fixed;
  top: 0; left: 0; right: 0; bottom: 0;
  background: rgba(0,0,0,0.4);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal-card {
  background: var(--card-bg);
  padding: 30px;
  border-radius: 16px;
  width: 350px;
  box-shadow: 0 20px 40px rgba(0,0,0,0.15);
  text-align: center;
}

.modal-card h2 {
  font-family: 'Montserrat', sans-serif;
  color: var(--primary-color);
  margin-bottom: 20px;
}

.form-group {
  margin-bottom: 15px;
  text-align: left;
}

label {
  font-size: 0.85rem;
  font-weight: 500;
  color: var(--text-primary);
  margin-bottom: 6px;
  display: block;
}

input {
  width: 100%;
  padding: 10px 12px;
  border-radius: 8px;
  border: 1px solid #ccc;
}

button {
  margin-top: 12px;
  padding: 10px 20px;
  border-radius: 8px;
  border: none;
  font-weight: 500;
  cursor: pointer;
}

button[type="submit"] {
  background: var(--primary-color);
  color: white;
  margin-right: 10px;
}

.cancel-btn {
  background: #ccc;
  color: #212121;
}
</style>
