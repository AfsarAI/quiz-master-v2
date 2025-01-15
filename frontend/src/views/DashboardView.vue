<template>
  <div
    class="dashboard-container"
    :class="{ 'sidebar-collapsed': isSidebarCollapsed }"
  >
    <SideBar
      :isSidebarCollapsed="isSidebarCollapsed"
      @toggle-sidebar="toggleSidebar"
    />
    <main class="main-content">
      <DashboardHeader />
      <div class="dashboard-content">
        <component :is="currentDashboard"></component>
      </div>
    </main>
  </div>
</template>

<script>
import { ref, computed } from "vue";
import { useStore } from "vuex";
import { useRouter } from "vue-router";
import SideBar from "@/components/SideBar.vue";
import DashboardHeader from "@/components/DashboardHeader.vue";
import AdminDashboard from "@/components/AdminDashboard.vue";
import UserDashboard from "@/components/UserDashboard.vue";

export default {
  name: "DashboardView",
  components: {
    SideBar,
    DashboardHeader,
    AdminDashboard,
    UserDashboard,
  },
  setup() {
    const store = useStore();
    const router = useRouter();

    const user = computed(() => store.state.user);
    const isDarkMode = computed(() => store.state.isDarkMode);
    const isSidebarCollapsed = ref(false);

    const currentDashboard = computed(() => {
      return user.value.roles.includes("Admin")
        ? AdminDashboard
        : UserDashboard;
    });

    const toggleSidebar = () => {
      isSidebarCollapsed.value = !isSidebarCollapsed.value;
    };

    const toggleDarkMode = () => {
      store.commit("toggleDarkMode");
    };

    const logout = () => {
      store.dispatch("logout");
      router.push("/login");
    };

    return {
      isDarkMode,
      isSidebarCollapsed,
      currentDashboard,
      toggleSidebar,
      toggleDarkMode,
      logout,
    };
  },
};
</script>

<style scoped>
.dashboard-container {
  display: flex;
  min-height: 100vh;
}

.main-content {
  flex: 1;
  padding: 2rem;
  transition: all 0.3s ease;
}

@media (max-width: 768px) {
  .dashboard-container {
    flex-direction: column;
  }

  .main-content {
    padding: 1rem;
  }
}
</style>
