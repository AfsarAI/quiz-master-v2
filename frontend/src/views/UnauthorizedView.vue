<template>
  <div class="unauthorized-container">
    <h1>403 - Unauthorized Access</h1>
    <p>You do not have permission to view that page!</p>
    <p>First you have to login!</p>
    <div class="button-group">
      <router-link to="/" class="btn">Go to Home</router-link>
      <router-link to="/quiz-master/register" class="btn">Register</router-link>
      <router-link to="/quiz-master/login" class="btn">Login</router-link>
    </div>
  </div>
</template>

<script>
export default {
  name: "UnauthorizedView",
};
</script>

<style scoped>
.unauthorized-container {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  height: 100vh;
  background-color: #f8d7da;
  color: #721c24;
  font-family: "Segoe UI", sans-serif;
}

h1 {
  font-size: 3rem;
  margin-bottom: 1rem;
}

p {
  font-size: 1.2rem;
  margin-bottom: 2rem;
}

.button-group {
  display: flex;
  gap: 1rem;
}

.btn {
  background-color: #007bff;
  color: white;
  text-decoration: none;
  padding: 0.8rem 1.5rem;
  border-radius: 5px;
  transition: background-color 0.3s;
}

.btn:hover {
  background-color: #0056b3;
}
</style>
