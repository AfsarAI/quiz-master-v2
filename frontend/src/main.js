import "bootstrap";
import "bootstrap/dist/css/bootstrap.min.css";
import "bootstrap/dist/js/bootstrap.bundle.min.js";
import "bootstrap-icons/font/bootstrap-icons.css";
import "@fortawesome/fontawesome-free/css/all.css";

import { createApp } from "vue";
import App from "./App.vue";
import router from "./router";
import store from "./store";
import ObserveDirective from "./directives/objerve";

const app = createApp(App);

// Initialize user data when app loads
store.dispatch("initializeUser");

// Check dark mode from localStorage and set Vuex state
const storedDarkMode = JSON.parse(localStorage.getItem("isDarkMode"));
if (storedDarkMode !== null) {
  store.commit("toggleDarkMode", storedDarkMode); // Update Vuex state based on localStorage
}

app.directive("observe", ObserveDirective);

// Use router and store
app.use(store).use(router);

// Mount the app
app.mount("#app");
