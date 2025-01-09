<template>
  <div id="app" :class="{ 'dark-mode': isDarkMode }">
    <AppNavbar />
    <main class="content">
      <router-view />
    </main>
    <AppFooter />
    <DarkModeToggle />
  </div>
</template>

<script setup>
import { computed } from "vue";
import { useStore } from "vuex";
import AppNavbar from "@/components/Navbar.vue";
import AppFooter from "@/components/Footer.vue";
import DarkModeToggle from "@/components/DarkModeToggle.vue";

const store = useStore();
const isDarkMode = computed(() => store.state.isDarkMode);
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

.dark-mode {
  background-color: #2c3e50;
  color: #f1f1f1;
}

/* Global styles for dark mode */
.dark-mode .bg-light {
  background-color: #34495e !important;
  color: #f1f1f1;
}

.dark-mode .text-dark {
  color: #f1f1f1 !important;
}

.dark-mode .btn-light {
  background-color: #f1f1f1;
  color: #2c3e50;
}

.dark-mode .card {
  background-color: #34495e;
  color: #f1f1f1;
}
</style>
