<template>
  <div id="app">
    <AppNavbar />
    <div class="content">
      <router-view />
    </div>
    <AppFooter />
  </div>
</template>

<script>
import AppNavbar from "@/components/Navbar.vue";
import AppFooter from "@/components/Footer.vue";
export default {
  name: "App",
  components: {
    AppNavbar,
    AppFooter,
  },
};
</script>

<style>
/* Add this CSS to style the layout */
#app {
  display: flex;
  flex-direction: column;
  min-height: 100vh; /* Ensure the app takes full viewport height */
}

.content {
  flex: 1; /* Pushes the footer down if content is small */
}
</style>
