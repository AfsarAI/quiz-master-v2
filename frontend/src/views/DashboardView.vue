<template>
  <div
    class="dashboard-container"
    :class="{ 'sidebar-collapsed': isSidebarCollapsed }"
  >
    <SideBar
      :isSidebarCollapsed="isSidebarCollapsed"
      :role="role"
      @toggle-sidebar="toggleSidebar"
    />
    <main class="main-content">
      <DashboardHeader />
      <div class="dashboard-content">
        <component :is="currentDashboard" />
      </div>
    </main>
  </div>
</template>

<script>
import { ref, computed } from "vue";
import { useRoute } from "vue-router";
import SideBar from "@/components/SideBar.vue";
import DashboardHeader from "@/components/DashboardHeader.vue";
import UserDashboard from "@/components/UserDashboard.vue";
import AdminDashboard from "@/components/AdminDashboard.vue";

export default {
  name: "DashboardView",
  components: {
    SideBar,
    DashboardHeader,
    UserDashboard,
    AdminDashboard,
  },
  setup() {
    const route = useRoute();
    const isSidebarCollapsed = ref(false);

    const toggleSidebar = () => {
      isSidebarCollapsed.value = !isSidebarCollapsed.value;
    };

    const role = computed(() => route.params.role);

    const currentDashboard = computed(() => {
      return role.value === "admin" ? AdminDashboard : UserDashboard;
    });

    return {
      isSidebarCollapsed,
      toggleSidebar,
      currentDashboard,
      role,
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
