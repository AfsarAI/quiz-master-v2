<template>
  <div class="container container-fluid py-4">
    <h1 class="mb-4">User Quizzes</h1>

    <div v-if="loading" class="text-center">
      <p class="fs-5">Loading...</p>
    </div>

    <div v-else>
      <div v-if="quizzes.length === 0" class="alert alert-warning text-center">
        No quizzes available.
      </div>
      <div v-else class="row g-4">
        <div class="col-md-4" v-for="quiz in quizzes" :key="quiz.id">
          <div class="card quiz-card h-100">
            <div class="card-body d-flex flex-column">
              <h5 class="card-title">{{ quiz.title }}</h5>
              <p class="card-text text-muted">Subject: {{ quiz.subject }}</p>
              <span class="badge bg-info mb-1"
                >Questions: {{ quiz.questions }}</span
              >
              <span class="badge bg-info mb-3"
                >Duration: {{ quiz.duration }} minutes</span
              >
              <button
                class="btn btn-primary mt-auto"
                @click="navigateToQuiz(quiz.id)"
              >
                Take Quiz
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from "vue";
import { useStore } from "vuex";
import { useRouter } from "vue-router";

export default {
  setup() {
    const store = useStore();
    const router = useRouter();
    const quizzes = ref([]);
    const loading = ref(false);

    const userId = ref(null);
    const role = ref(null);

    if (!store.state.user?.id) {
      console.error("User ID not found. Please ensure the user is logged in.");
    } else {
      userId.value = store.state.user.id;
    }

    const fetchAllQuizzes = async () => {
      loading.value = true;
      try {
        const response = await fetch(
          "http://localhost:5000/api/user/dashboard/all/quizzes"
        );
        if (!response.ok) {
          throw new Error("Failed to fetch quizzes");
        }
        quizzes.value = await response.json();
      } catch (error) {
        console.error("Error fetching quizzes:", error);
      } finally {
        loading.value = false;
      }
    };

    const navigateToQuiz = (quizId) => {
      const routeRole = router.currentRoute.value.params.role;
      const userRoles = store.state.user?.roles || [];

      if (
        Array.isArray(userRoles) &&
        userRoles.map((r) => r.name).includes(routeRole)
      ) {
        role.value = routeRole;
        const route = `/quiz-master/${role.value}/${userId.value}/dashboard/quiz/${quizId}/interface`;
        router.push(route);
      } else {
        console.error("Role in route does not match any user roles.");
      }
    };

    onMounted(fetchAllQuizzes);

    return {
      quizzes,
      loading,
      navigateToQuiz,
    };
  },
};
</script>

<style scoped>
.container {
  max-width: 1200px;
  margin: 0 auto;
}

.quiz-card {
  border-radius: 12px;
  overflow: hidden;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.05);
}

.quiz-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.1);
}

.card-title {
  font-size: 1.25rem;
  font-weight: 600;
}

.card-text {
  font-size: 0.9rem;
  margin-bottom: 1rem;
}

button {
  background-color: var(--bs-primary);
  border-radius: 20px;
  transition: background-color 0.3s;
}

button:hover {
  background-color: var(--bs-dark);
}

.alert {
  font-size: 1.1rem;
}
</style>
