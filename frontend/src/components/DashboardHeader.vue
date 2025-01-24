<template>
  <header class="dashboard-header">
    <div class="header-content">
      <h1 class="welcome-text">Welcome, {{ userName }}</h1>
      <div class="header-actions">
        <button
          @click="toggleDarkMode"
          class="btn btn-icon"
          :title="isDarkMode ? 'Switch to Light Mode' : 'Switch to Dark Mode'"
        >
          <i class="bi" :class="isDarkMode ? 'bi-sun' : 'bi-moon'"></i>
        </button>
        <button @click.prevent="logout" class="btn btn-danger">
          <i class="bi bi-box-arrow-right me-2"></i> Logout
        </button>
      </div>
    </div>
  </header>
</template>

<script setup>
import { ref, onMounted, watch } from "vue";
import { useRouter } from "vue-router";
import { useStore } from "vuex";

const router = useRouter();
const store = useStore();
const userName = ref(store.state.user?.fullName || "User");
const isDarkMode = ref(store.state.isDarkMode);

const toggleDarkMode = () => {
  store.commit("toggleDarkMode");
};

const logout = () => {
  if (confirm("Are you sure you want to logout?")) {
    store.dispatch("logout");
    router.push({ name: "login" });
  }
};

watch(
  () => store.state.isDarkMode,
  (newValue) => {
    isDarkMode.value = newValue;
    document.documentElement.setAttribute(
      "data-bs-theme",
      newValue ? "dark" : "light"
    );
  }
);

onMounted(() => {
  document.documentElement.setAttribute(
    "data-bs-theme",
    isDarkMode.value ? "dark" : "light"
  );
});
</script>

<style scoped>
.dashboard-header {
  background: linear-gradient(
    135deg,
    var(--bs-primary) 0%,
    var(--bs-info) 100%
  );
  background-color: rgba(var(--bs-primary-rgb), 0.9);
  /* background-color: transparent; */
  color: white;
  padding: 0.75rem 1rem;
  width: 75%;
  margin: 0 auto;
  z-index: 1000;
  transition: all 0.3s ease;
  border-radius: 0 0 15px 15px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 1rem;
}

.welcome-text {
  font-size: 1.25rem;
  font-weight: 600;
  margin: 0;
  opacity: 0;
  animation: fadeIn 0.5s ease-out forwards;
}

.header-actions {
  display: flex;
  gap: 1rem;
  align-items: center;
}

.btn {
  transition: all 0.3s ease;
}

.btn-icon {
  background: rgba(255, 255, 255, 0.2);
  border: none;
  color: white;
  font-size: 1.2rem;
  padding: 0.5rem;
  border-radius: 50%;
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s ease;
}

.btn-icon:hover {
  background: rgba(255, 255, 255, 0.3);
  transform: scale(1.1);
}

.btn-danger {
  background-color: #dc3545;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 20px;
  font-weight: 600;
  display: flex;
  align-items: center;
}

.btn-danger:hover {
  background-color: #c82333;
  transform: translateY(-2px);
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
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

[data-bs-theme="dark"] .dashboard-header {
  background: linear-gradient(135deg, #2c3e50 0%, #34495e 100%);
  background-color: rgba(var(--bs-primary-rgb), 0.9);
}

[data-bs-theme="dark"] .btn-danger {
  background-color: #e74c3c;
}

[data-bs-theme="dark"] .btn-danger:hover {
  background-color: #c0392b;
}

@media (max-width: 768px) {
  .welcome-text {
    font-size: 1rem;
  }

  .btn-danger {
    padding: 0.4rem 0.8rem;
    font-size: 0.9rem;
  }

  .btn-icon {
    width: 36px;
    height: 36px;
    font-size: 1rem;
  }
}
</style>
