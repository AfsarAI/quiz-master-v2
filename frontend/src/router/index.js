import { createRouter, createWebHistory } from "vue-router";
import store from "../store"; // Vuex Store
import HomeView from "../views/HomeView.vue";

const routes = [
  {
    path: "/",
    name: "home",
    component: HomeView,
    meta: {
      title: "Home",
    },
  },
  {
    path: "/about",
    name: "about",
    component: () =>
      import(/* webpackChunkName: "about" */ "../views/AboutView.vue"),
    meta: { title: "About" },
  },
  {
    path: "/register",
    name: "register",
    component: () =>
      import(/* webpackChunkName: "register" */ "../views/RegisterView.vue"),
    meta: { title: "Register" },
  },
  {
    path: "/login",
    name: "login",
    component: () =>
      import(/* webpackChunkName: "login" */ "../views/LoginView.vue"),
    meta: { title: "Login" },
  },
  {
    path: "/:role/:user_id/dashboard",
    name: "dashboard",
    component: () =>
      import(/* webpackChunkName: "dashboard" */ "../views/DashboardView.vue"),
    meta: { requiresLogin: true, title: "Dashboard" },
  },
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
  linkActiveClass: "active",
});

router.beforeEach((to, from, next) => {
  document.title = to.meta.title || "Default Title";

  // Check if the route requires login
  if (to.matched.some((record) => record.meta.requiresLogin)) {
    const isAuthenticated = store.state.user.loggedIn;

    if (!isAuthenticated) {
      // If user is not authenticated, redirect to login page
      next("/login");
      console.log("User is not logged in, redirecting to login...");
    } else {
      // If authenticated, check for role access and route parameters
      const userRole = store.state.user.roles[0]?.name; // Assuming the role is a string, not a value object
      if (to.name === "dashboard" && userRole !== to.params.role) {
        alert("Access Denied: Invalid Role");
        next("/"); // Redirect to home if role mismatch
      } else {
        next(); // Allow navigation if authenticated and authorized
      }
    }
  } else {
    // No login required for the route
    next();
  }
});

export default router;
