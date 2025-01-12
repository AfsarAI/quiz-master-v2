<template>
  <div class="dashboard">
    <h1>{{ user.fullName }}, {{ userName }}</h1>

    <button @click="logout">Logout</button>
  </div>
</template>

<script>
import { computed } from "vue";
import { useStore } from "vuex";
import { useRouter } from "vue-router"; // Import the router

export default {
  name: "DashboardView",
  setup() {
    const store = useStore();
    const router = useRouter();

    const user = computed(() => store.state.user);
    const userRole = computed(() => {
      return store.state.user.roles.length > 0
        ? store.state.user.roles[0]
        : "No Role Assigned";
    });
    const userName = computed(() => user.value?.fullName || "Guest");

    const logout = () => {
      store.commit("logout");
      router.push("/"); // Redirect to home page
    };

    return { user, userRole, userName, logout };
  },
};
</script>
