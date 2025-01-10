<template>
  <div class="dashboard">
    <h1 class="mb-4">
      Welcome, {{ user.fullName }}! with role : {{ user.roles[0] }}
    </h1>
    <div class="row">
      <div class="col-md-4 mb-4">
        <DashboardCard
          title="Quizzes Completed"
          :value="quizzesCompleted"
          icon="bi-check-circle"
        />
      </div>
      <div class="col-md-4 mb-4">
        <DashboardCard
          title="Average Score"
          :value="`${averageScore}%`"
          icon="bi-graph-up"
        />
      </div>
      <div class="col-md-4 mb-4">
        <DashboardCard
          title="Ranking"
          :value="`#${ranking}`"
          icon="bi-trophy"
        />
      </div>
    </div>
    <div class="row">
      <div class="col-md-6 mb-4">
        <RecentQuizzes :quizzes="recentQuizzes" />
      </div>
      <div class="col-md-6 mb-4">
        <RecommendedQuizzes :quizzes="recommendedQuizzes" />
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted } from "vue";
import { useStore } from "vuex";
import DashboardCard from "@/components/dashboard/DashboardCard.vue";
import RecentQuizzes from "@/components/dashboard/RecentQuizzes.vue";
import RecommendedQuizzes from "@/components/dashboard/RecommendedQuizzes.vue";

export default {
  name: "DashboardView",
  components: {
    DashboardCard,
    RecentQuizzes,
    RecommendedQuizzes,
  },
  setup() {
    const store = useStore();
    const user = computed(() => store.state.user);

    const quizzesCompleted = ref(0);
    const averageScore = ref(0);
    const ranking = ref(0);
    const recentQuizzes = ref([]);
    const recommendedQuizzes = ref([]);

    onMounted(async () => {
      // Fetch user dashboard data from API
      // This is a placeholder. Replace with actual API calls.
      quizzesCompleted.value = 15;
      averageScore.value = 85;
      ranking.value = 42;
      recentQuizzes.value = [
        { id: 1, title: "Math Quiz", score: 90 },
        { id: 2, title: "Science Quiz", score: 75 },
        { id: 3, title: "History Quiz", score: 60 },
      ];
      recommendedQuizzes.value = [
        { id: 4, title: "Geography Quiz" },
        { id: 5, title: "Literature Quiz" },
        { id: 6, title: "General Knowledge Quiz" },
      ];
    });

    return {
      user,
      quizzesCompleted,
      averageScore,
      ranking,
      recentQuizzes,
      recommendedQuizzes,
    };
  },
};
</script>

<style scoped>
.dashboard {
  padding: 20px;
}
</style>
