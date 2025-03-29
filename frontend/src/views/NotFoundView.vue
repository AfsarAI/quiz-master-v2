<template>
  <div class="not-found-container">
    <h1>404 - Page Not Found</h1>
    <p>Oops! The page you're looking for doesn't exist.</p>
    <div class="button-group">
      <router-link to="/" class="btn">Go to Home</router-link>
      <router-link to="/login" class="btn">Login</router-link>
      <router-link to="/register" class="btn">Register</router-link>
    </div>
  </div>
</template>

<script>
export default {
  name: "NotFoundView",
};
</script>

<style scoped>
.not-found-container {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  height: 100vh;
  background-color: #e9ecef;
  color: #495057;
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
