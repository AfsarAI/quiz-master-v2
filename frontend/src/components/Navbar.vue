<template>
  <nav
    :data-bs-theme="isDarkMode ? 'dark' : 'light'"
    :class="[
      'navbar',
      'nav',
      'navbar-expand-lg',
      'shadow',
      'sticky-top',
      {
        'navbar-dark bg-dark': isDarkMode,
        'navbar-light bg-light': !isDarkMode,
      },
    ]"
  >
    <div class="container">
      <router-link to="/" class="navbar-brand fw-bold">Quiz Master</router-link>
      <button
        class="navbar-toggler"
        type="button"
        data-bs-toggle="collapse"
        data-bs-target="#navbarNav"
        aria-controls="navbarNav"
        aria-expanded="false"
        aria-label="Toggle navigation"
      >
        <span class="navbar-toggler-icon"></span>
      </button>

      <div class="collapse navbar-collapse" id="navbarNav">
        <ul class="navbar-nav ms-auto align-items-center">
          <li class="nav-item">
            <router-link :to="{ name: 'home' }" class="nav-link" exact
              >Home</router-link
            >
          </li>
          <template v-if="!isLoggedIn">
            <li class="nav-item">
              <router-link
                :to="{ name: 'register' }"
                class="btn btn-outline-primary ms-2"
              >
                Register
              </router-link>
            </li>
            <li class="nav-item">
              <router-link
                :to="{ name: 'login' }"
                class="btn btn-outline-primary ms-2"
              >
                Login
              </router-link>
            </li>
          </template>

          <template v-else>
            <li class="nav-item">
              <router-link :to="dashboardLink" class="nav-link" exact
                >Dashboard</router-link
              >
            </li>
          </template>
        </ul>
      </div>
    </div>
  </nav>
</template>

<script>
import { computed } from "vue";
import { useStore } from "vuex";
import { useRouter } from "vue-router";

export default {
  name: "AppNavbar",
  setup() {
    const store = useStore();
    const router = useRouter();

    const isDarkMode = computed(() => store.state.isDarkMode);
    const isLoggedIn = computed(() => store.state.user.loggedIn);
    const userRole = computed(() => store.state.user.roles[0].name || "guest");
    const userId = computed(() => store.state.user.id);

    const dashboardLink = computed(() => {
      return `quiz-master/${userRole.value}/${userId.value}/dashboard`;
    });

    const ProfileLink = computed(() => {
      return `/${userRole.value}/${userId.value}/dashboard/profile`;
    });

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
      isDarkMode,
      isLoggedIn,
      userRole,
      dashboardLink,
      ProfileLink,
      toggleDarkMode,
      logout,
    };
  },
};
</script>

<style scoped>
.navbar-brand {
  color: inherit;
}

.navbar-brand:hover {
  color: #3498db;
}

.btn-outline-primary {
  color: #3498db;
  border-color: #3498db;
}

.btn-outline-primary:hover {
  color: #fff;
  background-color: #3498db;
  border-color: #3498db;
}

.navbar-nav .btn-outline-primary.router-link-exact-active,
.navbar-nav .btn-outline-primary.router-link-active {
  color: #fff;
  background-color: #3498db;
  border-color: #3498db;
}

.nav-link {
  color: inherit;
}

.nav-link:hover {
  color: #3498db;
}

.navbar-nav .nav-link.router-link-exact-active,
.navbar-nav .nav-link.router-link-active {
  color: #3498db;
}

[data-bs-theme="dark"] .navbar-brand:hover,
[data-bs-theme="dark"] .nav-link:hover,
[data-bs-theme="dark"] .navbar-nav .nav-link.router-link-exact-active,
[data-bs-theme="dark"] .navbar-nav .nav-link.router-link-active {
  color: #5dade2;
}

[data-bs-theme="dark"] .btn-outline-primary {
  color: #5dade2;
  border-color: #5dade2;
}

[data-bs-theme="dark"] .btn-outline-primary:hover,
[data-bs-theme="dark"]
  .navbar-nav
  .btn-outline-primary.router-link-exact-active,
[data-bs-theme="dark"] .navbar-nav .btn-outline-primary.router-link-active {
  color: #fff;
  background-color: #5dade2;
  border-color: #5dade2;
}
</style>
