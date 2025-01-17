<template>
  <header class="dashboard-header">
    <h1 class="mb-0">Welcome, {{ userName }}</h1>
    <div class="header-actions">
      <button @click="toggleDarkMode" class="btn btn-outline-primary me-2">
        <i class="bi" :class="isDarkMode ? 'bi-sun' : 'bi-moon'"></i>
        {{ isDarkMode ? "Light" : "Dark" }} Mode
      </button>
      <button @click.prevent="logout" class="btn btn-outline-danger">
        <i class="bi bi-box-arrow-right"></i> Logout
      </button>
    </div>
  </header>
</template>

<script>
import { useStore } from "vuex";
import { useRouter } from "vue-router";
import { computed } from "vue";

export default {
  name: "DashboardHeader",
  setup() {
    const store = useStore();
    const router = useRouter();

    const userName = computed(() => store.state.user.fullName);
    const isDarkMode = computed(() => store.state.isDarkMode);

    const toggleDarkMode = () => {
      store.commit("toggleDarkMode");
    };

    const logout = () => {
      const confirmLogout = confirm("Are you sure you want to log out?");
      if (!confirmLogout) {
        return;
      }

      try {
        store.dispatch("logout");
        store.dispatch("addToast", {
          message: "Logout successful!",
          type: "success",
        });
        router.push("/");
      } catch (error) {
        console.error("Logout failed:", error);
        store.dispatch("addToast", {
          message: "An error occurred while logging out. Please try again.",
          type: "danger",
        });
      }
    };

    return {
      toggleDarkMode,
      isDarkMode,
      logout,
      userName,
    };
  },
};
</script>

<style scoped>
.dashboard-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
}
</style>
