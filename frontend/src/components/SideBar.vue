<template>
  <aside class="sidebar" :class="{ collapsed: isSidebarCollapsed }">
    <div class="sidebar-header">
      <h3 v-if="!isSidebarCollapsed" class="mb-0">
        <router-link to="/quiz-master" class="navbar-brand fw-bold">
          Quiz Master
        </router-link>
      </h3>
      <button @click="toggleSidebar" class="btn btn-link sidebar-toggle">
        <i
          class="bi"
          :class="isSidebarCollapsed ? 'bi-chevron-right' : 'bi-chevron-left'"
        ></i>
      </button>
    </div>
    <nav class="sidebar-nav">
      <ul class="nav flex-column">
        <li
          v-for="item in filteredMenuItems"
          :key="item.text"
          :class="{ active: isActive(item.route) }"
        >
          <router-link class="nav-link" :to="fullPath(item.route)">
            <i :class="item.icon" class="me-2"></i>
            <span v-if="!isSidebarCollapsed">{{ item.text }}</span>
          </router-link>
        </li>
      </ul>
    </nav>
    <div class="sidebar-footer">
      <button @click="logout" class="btn btn-link nav-link w-100 text-start">
        <i class="bi bi-box-arrow-right me-2"></i>
        <span v-if="!isSidebarCollapsed">Logout</span>
      </button>
    </div>
  </aside>
</template>

<script>
import { computed } from "vue";
import { useRoute, useRouter } from "vue-router";
import { useStore } from "vuex";

export default {
  name: "SideBar",
  props: {
    isSidebarCollapsed: {
      type: Boolean,
      default: false,
    },
    role: {
      type: String,
      required: true,
    },
  },
  emits: ["toggle-sidebar"],
  setup(props, { emit }) {
    const route = useRoute();
    const router = useRouter();
    const store = useStore();

    const basePath = computed(() => {
      const parts = route.path.split("/");
      return parts.slice(0, 4).join("/");
    });

    const menuItems = computed(() => [
      {
        text: "Overview",
        route: "dashboard/overview",
        roles: ["admin"],
        icon: "bi bi-house",
      },
      {
        text: "Classes",
        route: "dashboard/classes",
        roles: ["admin"],
        icon: "bi bi-collection",
      },
      {
        text: "Users",
        route: "dashboard/users",
        roles: ["admin"],
        icon: "bi bi-people",
      },
      {
        text: "Home",
        route: "dashboard/home",
        roles: ["user"],
        icon: "bi bi-house",
      },
      {
        text: "Quizzes",
        route: "dashboard/quizzes",
        roles: ["admin"],
        icon: "bi bi-question-circle",
      },
      {
        text: "Quiz",
        route: "dashboard/quiz",
        roles: ["user"],
        icon: "bi bi-question-circle",
      },
      {
        text: "Progress",
        route: "dashboard/progress",
        roles: ["user"],
        icon: "bi bi-bar-chart",
      },
      {
        text: "Profile",
        route: "dashboard/profile",
        roles: ["user"],
        icon: "bi bi-person",
      },
    ]);

    const filteredMenuItems = computed(() =>
      menuItems.value.filter((item) => item.roles.includes(props.role))
    );

    const toggleSidebar = () => emit("toggle-sidebar");
    const isActive = (path) => route.path.includes(path);

    const fullPath = (route) => `${basePath.value}/${route}`;

    const logout = () => {
      if (confirm("Are you sure you want to logout?")) {
        store.dispatch("logout");
        router.push({ name: "login" });
      }
    };

    return {
      filteredMenuItems,
      toggleSidebar,
      isActive,
      fullPath,
      logout,
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
  display: flex;
  flex-direction: column;
  height: 100vh;
  position: fixed;
  top: 0;
  left: 0;
  z-index: 1000;
  overflow-y: auto;
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
  flex-grow: 1;
}

.sidebar-nav .nav-link {
  color: #333;
  padding: 0.5rem 1rem;
  display: flex;
  align-items: center;
  text-decoration: none;
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

.sidebar-nav .nav-link.active {
  font-weight: bold;
}

.sidebar-nav .nav-link i {
  margin-right: 0.5rem;
  font-size: 1.2rem;
}

.sidebar-footer {
  padding: 1rem;
  border-top: 1px solid #e9ecef;
}

[data-bs-theme="dark"] .sidebar-footer {
  border-top-color: #2c3e50;
}
</style>
