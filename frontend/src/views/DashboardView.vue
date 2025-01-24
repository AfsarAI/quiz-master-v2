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
    <div class="main-content">
      <div class="dashboard-header-wrapper">
        <DashboardHeader />
      </div>
      <router-view />
    </div>
  </div>
</template>

<script>
import { ref, computed } from "vue";
import { useRoute } from "vue-router";
import SideBar from "@/components/SideBar.vue";
import DashboardHeader from "@/components/DashboardHeader.vue";

export default {
  name: "DashboardView",
  components: {
    SideBar,
    DashboardHeader,
  },
  setup() {
    const route = useRoute();
    const isSidebarCollapsed = ref(false);

    const toggleSidebar = () => {
      isSidebarCollapsed.value = !isSidebarCollapsed.value;
    };

    const role = computed(() => route.params.role);

    return {
      isSidebarCollapsed,
      toggleSidebar,
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
  margin-left: 250px;
  transition: all 0.3s ease;
  display: flex;
  flex-direction: column;
  height: 100vh;
  overflow-y: auto;
}

.sidebar-collapsed .main-content {
  margin-left: 60px;
}

.dashboard-header-wrapper {
  position: sticky;
  top: 0;
  z-index: 1000;
  background-color: var(--bs-body-bg);
  background-color: transparent;
}

.dashboard-content {
  flex: 1;
  padding: 2rem;
}

@media (max-width: 768px) {
  .dashboard-container {
    flex-direction: column;
  }

  .main-content {
    margin-left: 0;
  }

  .sidebar-collapsed .main-content {
    margin-left: 0;
  }
}
</style>
