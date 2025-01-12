<template>
  <div id="app" :data-bs-theme="isDarkMode ? 'dark' : 'light'">
    <AppNavbar />
    <router-view />
    <AppFooter />
    <DarkModeToggle />
    <ToastNotifications ref="toast" />
  </div>
</template>

<script setup>
import { computed, watch, onMounted } from "vue";
import { useStore } from "vuex";
import AppNavbar from "@/components/Navbar.vue";
import AppFooter from "@/components/Footer.vue";
import DarkModeToggle from "@/components/DarkModeToggle.vue";
import ToastNotifications from "@/components/ToastNotifications.vue";

// Access Vuex store
const store = useStore();

// Reactive computed property for dark mode state
const isDarkMode = computed(() => store.state.isDarkMode);

// When the component is mounted, check localStorage for dark mode preference
onMounted(() => {
  const storedDarkMode = JSON.parse(localStorage.getItem("isDarkMode")); // Use correct key
  if (storedDarkMode !== null) {
    store.commit("toggleDarkMode", storedDarkMode); // Set Vuex state based on localStorage
  }
});

watch(isDarkMode, (newVal) => {
  localStorage.setItem("isDarkMode", newVal ? "true" : "false"); // Save to correct key
  const body = document.body;
  if (newVal) {
    body.classList.add("dark-mode");
    body.classList.remove("light-mode");
  } else {
    body.classList.add("light-mode");
    body.classList.remove("dark-mode");
  }
});
</script>

<style>
#app {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
  transition: background-color 0.3s ease, color 0.3s ease;
}

.content {
  flex: 1;
}

/* Light Mode */
[data-bs-theme="light"] {
  background-color: #ffffff; /* Light mode body background */
  color: #333; /* Dark text color */
}

/* Dark Mode */
[data-bs-theme="dark"] {
  background-color: #121212; /* Dark mode body background */
  color: #f1f1f1; /* Light text color */
}
</style>
