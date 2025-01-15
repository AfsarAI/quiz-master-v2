<template>
  <div class="admin-dashboard">
    <component :is="currentComponent"></component>
  </div>
</template>

<script>
import { computed } from "vue";
import { useStore } from "vuex";
import AdminOverview from "./AdminDash/AdminOverview.vue";
import AdminClasses from "./AdminDash/AdminClasses.vue";
import AdminQuizzes from "./AdminDash/AdminQuizzes.vue";
import AdminUsers from "./AdminDash/AdminUsers.vue";

export default {
  name: "AdminDashboard",
  components: {
    AdminOverview,
    AdminClasses,
    AdminQuizzes,
    AdminUsers,
  },
  setup() {
    const store = useStore();
    const activeSection = computed(() => store.state.activeSection);

    const currentComponent = computed(() => {
      switch (activeSection.value) {
        case "classes":
          return AdminClasses;
        case "quizzes":
          return AdminQuizzes;
        case "users":
          return AdminUsers;
        default:
          return AdminOverview;
      }
    });

    return {
      currentComponent,
    };
  },
};
</script>
