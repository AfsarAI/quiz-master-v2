<template>
  <nav
    class="navbar nav-underline navbar-dark navbar-expand-lg bg-white shadow sticky-top"
  >
    <div class="container">
      <router-link to="/" class="navbar-brand fw-bold text-gray">
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
export default {
  name: "AppNavbar",
};
</script>

<style scoped>
/* Adjust the navbar brand color for visibility */
.navbar-brand {
  color: #6c757d; /* Neutral gray */
}

.navbar-brand:hover {
  color: #5a6268; /* Darker gray */
}

/* Style for buttons */
.btn-outline-primary {
  color: #007bff;
  border-color: #007bff;
}

.btn-outline-primary:hover {
  color: #fff;
  background-color: #007bff;
  border-color: #0056b3;
}

/* Active state for buttons */
.navbar-nav .btn-outline-primary.router-link-exact-active,
.navbar-nav .btn-outline-primary.router-link-active {
  color: #fff;
  background-color: #007bff;
  border-color: #0056b3;
}

/* Default nav-link styling */
.nav-link {
  color: #6c757d;
}

.nav-link:hover {
  color: #007bff;
}

/* Only change text color for active nav-link (no background change) */
.navbar-nav .nav-link.router-link-exact-active,
.navbar-nav .nav-link.router-link-active {
  color: #007bff;
}

/* Optional: Ensures that nav-link text doesn't change background color */
.navbar-nav .nav-link.router-link-exact-active:hover,
.navbar-nav .nav-link.router-link-active:hover {
  background-color: transparent;
}
</style>
