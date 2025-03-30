<template>
  <div class="container container-fluid py-4">
    <div class="row">
      <div class="col-md-6">
        <h1 class="mb-4">User Quizzes</h1>
      </div>
      <div v-if="!loading" class="col-md-6">
        <input
          v-model="searchQuery"
          type="text"
          class="form-control"
          placeholder="Search quizzes..."
        />
      </div>
    </div>

    <div v-if="loading" class="text-center">
      <div class="position-absolute top-50 start-50 translate-middle">
        <div class="spinner-border text-primary" role="status">
          <span class="visually-hidden">Loading...</span>
        </div>
      </div>
    </div>

    <div v-else>
      <div v-if="quizzes.length === 0" class="alert alert-warning text-center">
        No quizzes available.
      </div>
      <div v-else class="row g-4">
        <div class="col-md-4" v-for="quiz in filteredQuizzes" :key="quiz.id">
          <div class="card quiz-card h-100">
            <div class="card-body d-flex flex-column">
              <div class="d-flex justify-content-between align-items-center">
                <h5 class="card-title mb-0">{{ quiz.title }}</h5>
                <span
                  class="badge rounded-circle text-white d-flex justify-content-center align-items-center"
                  style="background-color: red; width: 30px; height: 30px"
                >
                  {{ quiz.attempt_count }}
                </span>
              </div>
              <div class="p-2">
                <p class="card-text text-muted">
                  <strong>Quiz Type:</strong> {{ quiz.quiz_type }}
                </p>
                <p class="card-text text-muted">
                  <strong>Subject:</strong> {{ quiz.subject?.name || "N/A" }}
                </p>
                <p class="card-text text-muted">
                  <strong>Chapter:</strong> {{ quiz.chapter?.name || "N/A" }}
                </p>
              </div>

              <div
                class="d-flex justify-content-center align-items-center gap-3 my-2"
              >
                <span
                  class="badge bg-info text-muted rounded-pill px-3 py-1 d-flex align-items-center"
                >
                  <i class="bi bi-question-circle me-1"></i>
                  Questions: {{ quiz.questions.length }}
                </span>
                <span
                  class="badge bg-warning text-muted rounded-pill px-3 py-1 d-flex align-items-center"
                >
                  <i class="bi bi-clock me-1"></i>
                  Duration: {{ quiz.duration }} minutes
                </span>
              </div>

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
import { ref, onMounted, computed } from "vue";
import { useStore } from "vuex";
import { useRouter } from "vue-router";

export default {
  setup() {
    const store = useStore();
    const router = useRouter();
    const quizzes = ref([]);
    const loading = ref(false);
    const searchQuery = ref("");

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
          `http://localhost:5000/api/user/${userId.value}/dashboard/all/quizzes`,
          {
            method: "GET",
            headers: {
              "Content-Type": "application/json",
              "Authentication-Token": store.state.user?.token,
            },
          }
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

    // Search filter
    const filteredQuizzes = computed(() => {
      return quizzes.value.filter(
        (quiz) =>
          quiz.title
            ?.toLowerCase()
            .includes(searchQuery.value?.toLowerCase() || "") ||
          quiz.quiz_type
            ?.toLowerCase()
            .includes(searchQuery.value?.toLowerCase() || "")
      );
    });

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
      searchQuery,
      filteredQuizzes,
    };
  },
};
</script>

<style scoped>
.spinner-border {
  width: 3rem;
  height: 3rem;
}
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
