<template>
  <button @click="toggleDarkMode" class="dark-mode-toggle">
    <i :class="isDarkMode ? 'bi bi-sun' : 'bi bi-moon'"></i>
  </button>
</template>

<script>
import { computed } from "vue";
import { useStore } from "vuex";

export default {
  name: "DarkModeToggle",
  setup() {
    const store = useStore();
    const isDarkMode = computed(() => store.state.isDarkMode);

    const toggleDarkMode = () => {
      store.commit("toggleDarkMode"); // Toggle Dark Mode and store it in localStorage
    };

    return {
      isDarkMode,
      toggleDarkMode,
    };
  },
};
</script>

<style scoped>
.dark-mode-toggle {
  position: fixed;
  bottom: 20px;
  right: 20px;
  background-color: rgba(52, 152, 219, 0.7);
  color: white;
  border: none;
  border-radius: 50%;
  width: 50px;
  height: 50px;
  font-size: 24px;
  cursor: pointer;
  transition: all 0.3s ease;
  z-index: 1000;
}

.dark-mode-toggle:hover {
  background-color: rgba(41, 128, 185, 0.9);
}

[data-bs-theme="dark"] .dark-mode-toggle {
  background-color: rgba(241, 196, 15, 0.7);
  color: #333;
}

[data-bs-theme="dark"] .dark-mode-toggle:hover {
  background-color: rgba(243, 156, 18, 0.9);
}
</style>
