<template>
  <aside class="sidebar" :class="{ collapsed: isSidebarCollapsed }">
    <div class="sidebar-header">
      <h3 v-if="!isSidebarCollapsed" class="mb-0">Quiz Master</h3>
      <button @click="toggleSidebar" class="btn btn-link sidebar-toggle">
        <i
          class="bi"
          :class="isSidebarCollapsed ? 'bi-chevron-right' : 'bi-chevron-left'"
        ></i>
      </button>
    </div>
    <nav class="sidebar-nav">
      <ul class="nav flex-column">
        <li class="nav-item" v-for="item in sidebarItems" :key="item.id">
          <a
            class="nav-link"
            href="#"
            @click="setActiveSection(item.id)"
            :class="{ active: activeSection === item.id }"
          >
            <i :class="item.icon"></i>
            <span v-if="!isSidebarCollapsed">{{ item.name }}</span>
          </a>
        </li>
      </ul>
    </nav>
  </aside>
</template>

<script>
import { computed } from "vue";
import { useStore } from "vuex";

export default {
  name: "SideBar",
  props: {
    isSidebarCollapsed: Boolean,
  },
  setup(props, { emit }) {
    const store = useStore();
    const activeSection = computed(() => store.state.activeSection);
    const user = computed(() => store.state.user);

    const sidebarItems = computed(() => {
      if (user.value.roles.includes("Admin")) {
        return [
          { id: "overview", name: "Overview", icon: "bi bi-speedometer2" },
          { id: "classes", name: "Classes", icon: "bi bi-book" },
          { id: "quizzes", name: "Quizzes", icon: "bi bi-question-circle" },
          { id: "users", name: "Users", icon: "bi bi-people" },
        ];
      } else {
        return [
          { id: "overview", name: "Overview", icon: "bi bi-speedometer2" },
          { id: "quizzes", name: "Quizzes", icon: "bi bi-question-circle" },
          { id: "progress", name: "Progress", icon: "bi bi-graph-up" },
          { id: "profile", name: "Profile", icon: "bi bi-person" },
        ];
      }
    });

    const toggleSidebar = () => {
      emit("toggle-sidebar");
    };

    const setActiveSection = (sectionId) => {
      store.dispatch("updateActiveSection", sectionId);
    };

    return {
      activeSection,
      sidebarItems,
      toggleSidebar,
      setActiveSection,
    };
  },
};
</script>

<style scoped>
.sidebar {
  width: 250px;
  background-color: #ffffff;
  box-shadow: 2px 0 5px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
}

[data-bs-theme="dark"] .sidebar {
  background-color: #34495e;
}

.sidebar.collapsed {
  width: 60px;
}

.sidebar-header {
  padding: 1rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.sidebar-toggle {
  background: none;
  border: none;
  color: #4361ee;
  font-size: 1.2rem;
}

.sidebar-nav {
  padding: 1rem 0;
}

.sidebar-nav .nav-link {
  color: #333;
  padding: 0.5rem 1rem;
  display: flex;
  align-items: center;
  transition: all 0.3s ease;
}

[data-bs-theme="dark"] .sidebar-nav .nav-link {
  color: #f1f1f1;
}

.sidebar-nav .nav-link:hover,
.sidebar-nav .nav-link.active {
  background-color: #f8f9fa;
  color: #4361ee;
}

[data-bs-theme="dark"] .sidebar-nav .nav-link:hover,
[data-bs-theme="dark"] .sidebar-nav .nav-link.active {
  background-color: #2c3e50;
  color: #5dade2;
}

.sidebar-nav .nav-link i {
  margin-right: 0.5rem;
  font-size: 1.2rem;
}
</style>
