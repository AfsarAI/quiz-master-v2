// Import required modules
import { createRouter, createWebHistory } from "vue-router";
import store from "../store"; // Vuex store
// import HomeView from "../views/HomeView.vue";
import DashboardView from "../views/DashboardView.vue";
import App from "@/App.vue";

// Define routes
const routes = [
  {
    path: "/quiz-master",
    component: App,
    meta: { title: "Home" },
    children: [
      {
        path: "",
        name: "home",
        component: () => import("../views/HomeView.vue"),
        meta: { title: "Home" },
      },
      {
        path: "about",
        name: "about",
        component: () => import("../views/AboutView.vue"),
        meta: { title: "About" },
      },
      {
        path: "register",
        name: "register",
        component: () => import("../views/RegisterView.vue"),
        meta: { title: "Register" },
      },
      {
        path: "login",
        name: "login",
        component: () => import("../views/LoginView.vue"),
        meta: { title: "Login" },
      },
      {
        path: ":role(admin|user)/:user_id/dashboard",
        name: "dashboard",
        component: DashboardView,
        meta: { requiresLogin: true, title: "Dashboard" },
        beforeEnter: (to, from, next) => {
          const validRoles = ["admin", "user"];
          const role = to.params.role;
          if (!validRoles.includes(role)) {
            next("/unauthorized");
          } else {
            next();
          }
        },
        children: [
          // admin specific
          {
            path: "overview",
            name: "Overview",
            component: () =>
              import("../components/AdminDash/AdminOverview.vue"),
            meta: {
              title: "Overview",
              requiresLogin: true,
              roles: ["admin"],
            },
          },
          {
            path: "classes",
            name: "classes",
            component: () => import("../components/AdminDash/AdminClasses.vue"),
            meta: {
              title: "Admin Classes",
              requiresLogin: true,
              roles: ["admin"],
            },
          },
          {
            path: "quizzes",
            name: "Quizzes",
            component: () => import("../components/AdminDash/AdminQuizzes.vue"),
            meta: {
              title: "Quizzes",
              requiresLogin: true,
              roles: ["admin"],
            },
          },
          {
            path: "users",
            name: "users",
            component: () => import("../components/AdminDash/AdminUsers.vue"),
            meta: { title: "Users", requiresLogin: true, roles: ["admin"] },
          },

          // users specific
          {
            path: "home",
            name: "userHome",
            component: () => import("../components/UserDash/UserHome.vue"),
            meta: { title: "User Home", requiresLogin: true, roles: ["user"] },
          },
          {
            path: "quiz",
            name: "Quiz",
            component: () => import("../components/UserDash/UserQuizzes.vue"),
            meta: { title: "User Quiz", requiresLogin: true, roles: ["user"] },
          },
          {
            path: "progress",
            name: "progress",
            component: () => import("../components/UserDash/UserProgress.vue"),
            meta: { title: "Progress", requiresLogin: true, roles: ["user"] },
          },
          {
            path: "profile",
            name: "profile",
            component: () => import("../components/UserDash/UserProfile.vue"),
            meta: { title: "Profile", requiresLogin: true, roles: ["user"] },
          },
        ],
      },
    ],
  },
  {
    path: "/",
    redirect: "/quiz-master",
  },
];

// Create router instance
const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
  linkActiveClass: "active",
});

// Global navigation guard
router.beforeEach((to, from, next) => {
  document.title = to.meta.title || "Default Title";

  if (to.matched.some((record) => record.meta.requiresLogin)) {
    const isAuthenticated = store.state.user.loggedIn;

    if (!isAuthenticated) {
      next("/login");
    } else {
      const userRole = store.state.user.roles[0]?.name;
      if (to.params.role !== userRole) {
        next("/unauthorized");
      } else {
        if (
          to.matched.some(
            (record) =>
              record.meta.roles && !record.meta.roles.includes(userRole)
          )
        ) {
          alert("You do not have access to this page.");
          next(false);
          window.history.back();
        } else {
          next();
        }
      }
    }
  } else {
    next();
  }

  // // Check if the route exists
  // if (!to.matched.length) {
  //   alert("The page you are trying to access does not exist on our website.");
  //   next(false);
  //   window.history.back();
  //   return;
  // }
});

export default router;
