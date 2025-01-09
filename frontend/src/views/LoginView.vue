<template>
  <div class="login-container">
    <div class="container">
      <div class="row justify-content-center align-items-center min-vh-100">
        <div class="col-md-6">
          <div class="card shadow-lg border-0">
            <div class="card-body p-5">
              <h2 class="text-center text-primary mb-4">
                Access Your Dashboard
              </h2>
              <form @submit.prevent="login">
                <div class="mb-3">
                  <label for="email" class="form-label">Email:</label>
                  <div class="input-group">
                    <span class="input-group-text">
                      <i class="bi bi-envelope"></i>
                    </span>
                    <input
                      v-model="email"
                      type="email"
                      id="email"
                      class="form-control"
                      placeholder="Enter your email"
                      required
                    />
                  </div>
                </div>
                <div class="mb-3">
                  <label for="password" class="form-label">Password:</label>
                  <div class="input-group">
                    <span class="input-group-text">
                      <i class="bi bi-lock"></i>
                    </span>
                    <input
                      v-model="password"
                      :type="showPassword ? 'text' : 'password'"
                      id="password"
                      class="form-control"
                      placeholder="Enter your password"
                      required
                    />
                    <button
                      class="btn btn-outline-secondary"
                      type="button"
                      @click="togglePassword"
                    >
                      <i
                        :class="showPassword ? 'bi bi-eye-slash' : 'bi bi-eye'"
                      ></i>
                    </button>
                  </div>
                </div>
                <div class="d-grid gap-2">
                  <button
                    type="submit"
                    class="btn btn-primary btn-lg"
                    :disabled="isLoading"
                  >
                    <span
                      v-if="isLoading"
                      class="spinner-border spinner-border-sm me-2"
                      role="status"
                      aria-hidden="true"
                    ></span>
                    {{ isLoading ? "Logging in..." : "Login" }}
                  </button>
                </div>
              </form>
              <p class="text-center mt-3">
                Don't have an account?
                <router-link
                  to="/register"
                  class="text-decoration-none fw-bold"
                >
                  Register here
                </router-link>
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref } from "vue";
import { useRouter } from "vue-router";

export default {
  name: "LoginPage",
  setup() {
    const email = ref("");
    const password = ref("");
    const showPassword = ref(false);
    const isLoading = ref(false);
    const router = useRouter();

    const togglePassword = () => {
      showPassword.value = !showPassword.value;
    };

    const login = async () => {
      isLoading.value = true;
      try {
        const response = await fetch(`${location.origin}/login`, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            email: email.value,
            password: password.value,
          }),
        });

        if (response.ok) {
          const data = await response.json();
          localStorage.setItem("user", JSON.stringify(data));
          console.log("Token:", data.token);
          router.push("/admin/dashboard");
        } else {
          console.error("Login failed", response.statusText);
          // You might want to show an error message to the user here
        }
      } catch (error) {
        console.error("Error during login:", error);
        // You might want to show an error message to the user here
      } finally {
        isLoading.value = false;
      }
    };

    return {
      email,
      password,
      showPassword,
      isLoading,
      togglePassword,
      login,
    };
  },
};
</script>

<style scoped>
.login-container {
  background: linear-gradient(135deg, #3498db, #8e44ad);
  min-height: 100vh;
  position: relative;
  overflow: hidden;
}

.card {
  background-color: rgba(255, 255, 255, 0.9);
  backdrop-filter: blur(10px);
}

.form-control:focus,
.btn:focus {
  box-shadow: 0 0 0 0.25rem rgba(13, 110, 253, 0.25);
}

.btn-primary {
  background-color: #3498db;
  border-color: #3498db;
  transition: all 0.3s ease;
}

.btn-primary:hover {
  background-color: #2980b9;
  border-color: #2980b9;
}

.text-primary {
  color: #3498db !important;
}

.input-group-text {
  background-color: #f8f9fa;
}
</style>
