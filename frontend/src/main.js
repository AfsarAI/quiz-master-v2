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
console.log(storedDarkMode);
if (storedDarkMode !== null) {
  store.commit("toggleDarkMode", storedDarkMode); // Update Vuex state based on localStorage
}

// for localStorage size ceck!
function calculateLocalStorageSize() {
  let totalSize = 0; // Total storage size in bytes
  const details = []; // Array to store details of each key

  for (let i = 0; i < localStorage.length; i++) {
    const key = localStorage.key(i); // Get the key
    const value = localStorage.getItem(key); // Get the value of the key
    const size = new Blob([value]).size; // Calculate size of the value in bytes

    totalSize += size;
    details.push({ key, size: size / 1024 }); // Convert size to KB
  }

  console.log("Key-wise size in KB:", details);
  console.log("Total size in MB:", totalSize / 1024 / 1024, "MB");
}

calculateLocalStorageSize();

app.directive("observe", ObserveDirective);

// Use router and store
app.use(store).use(router);

// Mount the app
app.mount("#app");
