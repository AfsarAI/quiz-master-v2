<template>
  <nav
    :class="[
      'navbar',
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
      <router-link to="/" class="navbar-brand fw-bold">
        Quiz Master
      </router-link>
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
            <router-link to="/" class="nav-link" exact>Home</router-link>
          </li>
          <li class="nav-item">
            <router-link to="/register" class="btn btn-outline-primary ms-2">
              Register
            </router-link>
          </li>
          <li class="nav-item">
            <router-link to="/login" class="btn btn-outline-primary ms-2">
              Login
            </router-link>
          </li>
        </ul>
      </div>
    </div>
  </nav>
</template>

<script>
import { computed } from "vue";
import { useStore } from "vuex";

export default {
  name: "AppNavbar",
  setup() {
    const store = useStore();
    const isDarkMode = computed(() => store.state.isDarkMode);

    return {
      isDarkMode,
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

.dark-mode .navbar-brand:hover,
.dark-mode .nav-link:hover,
.dark-mode .navbar-nav .nav-link.router-link-exact-active,
.dark-mode .navbar-nav .nav-link.router-link-active {
  color: #5dade2;
}

.dark-mode .btn-outline-primary {
  color: #5dade2;
  border-color: #5dade2;
}

.dark-mode .btn-outline-primary:hover,
.dark-mode .navbar-nav .btn-outline-primary.router-link-exact-active,
.dark-mode .navbar-nav .btn-outline-primary.router-link-active {
  color: #fff;
  background-color: #5dade2;
  border-color: #5dade2;
}
</style>
