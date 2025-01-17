<template>
  <div class="login-container" :data-bs-theme="isDarkMode ? 'dark' : 'light'">
    <div class="container">
      <div class="row justify-content-center align-items-center min-vh-100">
        <div class="col-md-6">
          <div class="card shadow-lg border-0">
            <div class="card-body p-5">
              <h2 class="text-center text-primary mb-4">
                Access Your Dashboard
              </h2>

              <div
                v-if="alertMessage"
                :class="`alert alert-${alertType} mt-3`"
                role="alert"
              >
                {{ alertMessage }}
              </div>
              <h6 class="text-muted mt-2" v-if="alertMessage">
                Please ensure your email and password are correct.
              </h6>

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
import { useStore } from "vuex";
import { computed } from "vue";

export default {
  name: "LoginPage",
  setup() {
    const email = ref("");
    const password = ref("");
    const showPassword = ref(false);
    const isLoading = ref(false);
    const alertMessage = ref("");
    const alertType = ref("");
    const router = useRouter();
    const store = useStore();
    const isDarkMode = computed(() => store.state.isDarkMode);

    const togglePassword = () => {
      showPassword.value = !showPassword.value;
    };

    const closeAlert = () => {
      alertMessage.value = "";
    };

    const showAlert = (message, type) => {
      alertMessage.value = message;
      alertType.value = type;

      setTimeout(() => {
        alertMessage.value = "";
      }, 5000);
    };

    const login = async () => {
      isLoading.value = true;

      try {
        const userData = {
          email: email.value.trim(),
          password: password.value.trim(),
        };

        const response = await fetch("http://127.0.0.1:5000/api/user/login", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify(userData),
        });

        if (!response.ok) {
          // Handle invalid login scenario
          handleError("Invalid email or password. Please try again.", "danger");
          return;
        }

        const data = await response.json();
        console.log(data);

        // Validate the response for required fields
        if (data.token && data.roles) {
          handleSuccess(data);
        } else {
          router.push("/");
        }
      } catch (error) {
        // Handle network or server error
        handleError("An error occurred. Please try again later.", "danger");
        console.log(error);
      } finally {
        // Always stop the loading indicator
        isLoading.value = false;
      }
    };

    // Helper function to handle success scenario
    const handleSuccess = (data) => {
      showAlert("Login successful!", "success");
      store.dispatch("addToast", {
        message: "Login successful!",
        type: "success",
      });

      // Clear input fields
      clearInputFields();

      const minimaldata = {
        id: data.id,
        roles: data.roles,
        fullname: data.fullname,
        token: data.token,
      };

      try {
        // Store user data in localStorage and Vuex
        localStorage.removeItem("user"); // Clear previous user data
        localStorage.setItem("user", JSON.stringify(minimaldata));
        console.log("User saved in localStorage successfully:", minimaldata);
        store.dispatch("login", minimaldata);
      } catch (error) {
        console.error("Error saving user to localStorage:", error);
        alert("Failed to save user data. Storage limit exceeded.");
      }

      // Redirect to role-specific dashboard
      const userRole = data.roles[0]?.name || null;
      const userId = data.id;

      if (userRole && userId) {
        router.push(`${userRole}/${userId}/dashboard`);
      } else {
        router.push("/");
      }
    };

    // Helper function to handle errors
    const handleError = (message, type) => {
      showAlert(message, type);
      store.dispatch("addToast", { message, type });
      clearInputFields();
    };

    // Helper function to clear input fields
    const clearInputFields = () => {
      email.value = "";
      password.value = "";
    };

    return {
      isDarkMode,
      email,
      password,
      showPassword,
      isLoading,
      togglePassword,
      login,
      alertMessage,
      alertType,
      closeAlert,
    };
  },
};
</script>

<style scoped>
.alert {
  animation: fadeIn 0.3s ease, fadeOut 0.5s 4.5s ease-in-out;
}
@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(-10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
@keyframes fadeOut {
  from {
    opacity: 1;
  }
  to {
    opacity: 0;
  }
}

.login-container {
  background: linear-gradient(135deg, #3a0ca3, #4361ee, #8e44ad);
  min-height: 100vh;
  position: relative;
  overflow: hidden;
}

.login-container::before {
  content: "";
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: url('data:image/svg+xml;charset=utf8,%3Csvg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1440 320"%3E%3Cpath fill="%23ffffff" fill-opacity="0.05" d="M0,96L48,112C96,128,192,160,288,186.7C384,213,480,235,576,213.3C672,192,768,128,864,128C960,128,1056,192,1152,208C1248,224,1344,192,1392,176L1440,160L1440,320L1392,320C1344,320,1248,320,1152,320C1056,320,960,320,864,320C768,320,672,320,576,320C480,320,384,320,288,320C192,320,96,320,48,320L0,320Z"%3E%3C/path%3E%3C/svg%3E')
    no-repeat bottom;
  background-size: cover;
}

[data-bs-theme="dark"] .login-container {
  background: #34495e;
}

.card {
  /* background-color: rgba(255, 255, 255, 0.9); */
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
</style>
