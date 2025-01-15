<template>
  <div class="user-dashboard">
    <component :is="currentComponent"></component>
  </div>
</template>

<script>
import { computed } from "vue";
import { useStore } from "vuex";
import UserOverview from "./UserDash/UserOverview.vue";
import UserQuizzes from "./UserDash/UserQuizzes.vue";
import UserProgress from "./UserDash/UserProgress.vue";
import UserProfile from "./UserDash/UserProfile.vue";

export default {
  name: "UserDashboard",
  components: {
    UserOverview,
    UserQuizzes,
    UserProgress,
    UserProfile,
  },
  setup() {
    const store = useStore();
    const activeSection = computed(() => store.state.activeSection);

    const currentComponent = computed(() => {
      switch (activeSection.value) {
        case "quizzes":
          return UserQuizzes;
        case "progress":
          return UserProgress;
        case "profile":
          return UserProfile;
        default:
          return UserOverview;
      }
    });

    return {
      currentComponent,
    };
  },
};
</script>
