<template>
  <div
    class="container bg-light p-4 rounded shadow-lg mt-4"
    style="max-width: 500px"
  >
    <h3
      class="text-center text-primary bg-light border-primary border rounded mb-4 p-3"
    >
      Access Your Dashboard
    </h3>
    <form @submit.prevent="login">
      <!-- Email Input -->
      <div class="mb-3">
        <label for="email" class="form-label">Email:</label>
        <input
          v-model="email"
          type="email"
          id="email"
          class="form-control"
          placeholder="Enter your email"
          required
        />
      </div>

      <!-- Password Input -->
      <div class="mb-3">
        <label for="password" class="form-label">Password:</label>
        <input
          v-model="password"
          type="password"
          id="password"
          class="form-control"
          placeholder="Enter your password"
          required
        />
      </div>

      <!-- Login Button -->
      <button type="submit" class="btn btn-primary btn-lg w-100 mt-3">
        Login
      </button>

      <!-- Register Link -->
      <p class="text-center mt-3">
        Don't have an account?
        <router-link
          to="/register"
          class="text-decoration-none text-primary fw-bold"
        >
          Register here
        </router-link>
      </p>
    </form>
  </div>
</template>

<script>
export default {
  data() {
    return {
      email: "",
      password: "",
    };
  },
  methods: {
    async login() {
      try {
        const response = await fetch(`${location.origin}/login`, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            email: this.email,
            password: this.password,
          }),
        });

        if (response.ok) {
          const data = await response.json();
          localStorage.setItem("user", JSON.stringify(data));
          this.$store.commit("setUser", data);
          console.log("Token:", data.token);
          this.$router.push("/admin/dashboard");
        } else {
          console.error("Login failed", response.statusText);
        }
      } catch (error) {
        console.error("Error during login:", error);
      }
    },
  },
};
</script>

<style scoped>
.container {
  max-width: 500px;
}
h3 {
  background-color: lightblue;
}
form {
  margin-top: 1rem;
}
</style>
