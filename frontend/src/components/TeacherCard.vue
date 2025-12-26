<template>
  <div class="card" @click="$emit('click', teacher)">
    <h3>{{ teacher.name }}</h3>
    <p>{{ teacher.email }}</p>
  </div>
</template>

<script>
export default {
  name: "TeacherCard",
  props: {
    teacher: Object
  }
};
</script>

<style scoped>
.card {
  background: var(--card-bg);
  border-radius: 14px;
  padding: 20px;
  box-shadow: 0 10px 25px rgba(0,0,0,0.1);
  text-align: center;
  cursor: pointer;
  transition: transform 0.2s, box-shadow 0.2s;
}

.card:hover {
  transform: translateY(-3px);
  box-shadow: 0 15px 30px rgba(0,0,0,0.15);
}

h3 {
  font-family: 'Montserrat', sans-serif;
  color: var(--primary-color);
  margin-bottom: 8px;
}

p {
  color: var(--text-secondary);
  font-size: 0.9rem;
}
</style>
