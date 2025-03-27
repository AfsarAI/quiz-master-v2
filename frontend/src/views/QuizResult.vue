<template>
  <div class="results-container">
    <div class="results-page">
      <div class="results-card" v-if="results">
        <h1>Exam Results</h1>

        <div class="results-summary">
          <div class="result-item">
            <h3>Score</h3>
            <div class="score">
              {{ results.score }} / {{ results.totalScore }}
            </div>
            <div class="percentage">{{ results.percentage }}%</div>
          </div>

          <div class="result-item">
            <h3>Time Taken</h3>
            <div class="time-taken">
              {{ formatTimeTaken(results.timeTaken) }}
            </div>
          </div>
        </div>

        <div class="results-details">
          <h3>Question Analysis</h3>

          <div
            class="question-analysis"
            v-for="(question, index) in results.questions"
            :key="index"
          >
            <div class="question-header">
              <h4>Question {{ index + 1 }}</h4>
              <div
                class="question-result"
                :class="{
                  correct: results.userAnswers[index] === question.answer,
                  incorrect:
                    results.userAnswers[index] &&
                    results.userAnswers[index] !== question.answer,
                  unanswered: !results.userAnswers[index],
                }"
              >
                {{
                  results.userAnswers[index]
                    ? results.userAnswers[index] === question.answer
                      ? "Correct"
                      : "Incorrect"
                    : "Not Attempted"
                }}
              </div>
            </div>

            <p class="question-text">
              {{ question.question || question.question_text }}
            </p>

            <div class="options-analysis">
              <div
                v-for="(option, optIndex) in question.options"
                :key="optIndex"
                class="option-item"
                :class="{
                  'user-selected': results.userAnswers[index] === option,
                  'correct-answer':
                    question.answer === option ||
                    question.correct_option === option,
                }"
              >
                <div class="option-marker">
                  {{ ["A", "B", "C", "D"][optIndex] }}
                </div>
                <div class="option-text">{{ option }}</div>
              </div>
            </div>
          </div>
        </div>

        <div class="action-buttons">
          <button @click="goToDashboard" class="btn-primary">
            Back to Dashboard
          </button>
          <button @click="restartExam" class="btn-secondary">
            Restart Exam
          </button>
        </div>
      </div>
      <div v-else class="loading-container">
        <div class="loading-spinner"></div>
        <p>Loading results...</p>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted, onBeforeUnmount } from "vue";
import { useRouter } from "vue-router";
import { useRoute } from "vue-router";
import { useStore } from "vuex";

export default {
  name: "QuizResults",
  setup() {
    const router = useRouter();
    const route = useRoute();
    const store = useStore();
    const quizId = route.params.quiz_id;
    const userId = ref(null);
    const role = ref(null);

    if (!store.state.user?.id) {
      console.error("User ID not found. Please ensure the user is logged in.");
    } else {
      userId.value = store.state.user.id;
    }

    // Initialize with default values to prevent undefined errors
    const results = ref({
      quizId: "",
      quizTitle: "",
      questions: [],
      userAnswers: [],
      score: 0,
      totalScore: 0,
      percentage: 0,
      timeTaken: 0,
    });

    // Add this after the results ref declaration
    const isNavigatingAway = ref(false);
    const isLoading = ref(true);

    // Local storage key for results
    const getResultsStorageKey = () => {
      return `quizResults_${quizId}`;
    };

    // Save results to local storage
    const saveResultsToLocalStorage = (resultsData) => {
      try {
        localStorage.setItem(
          getResultsStorageKey(),
          JSON.stringify(resultsData)
        );
        console.log("Quiz results saved to localStorage");
      } catch (error) {
        console.error("Error saving quiz results to localStorage:", error);
      }
    };

    // Load results from local storage
    const loadResultsFromLocalStorage = () => {
      try {
        const savedResults = JSON.parse(
          localStorage.getItem(getResultsStorageKey())
        );
        if (savedResults && savedResults.quizId === quizId) {
          console.log("Found saved quiz results");
          return savedResults;
        }
      } catch (error) {
        console.error("Error loading quiz results from localStorage:", error);
      }
      return null;
    };

    // Format time taken for display
    const formatTimeTaken = (seconds) => {
      const minutes = Math.floor(seconds / 60);
      const remainingSeconds = seconds % 60;
      return `${minutes} min ${remainingSeconds} sec`;
    };

    // Go back to dashboard
    const goToDashboard = () => {
      // Set flag to prevent re-saving
      isNavigatingAway.value = true;
      // Clear results from local storage when navigating away
      localStorage.removeItem(getResultsStorageKey());
      // Clear from store as well
      store.commit("clearQuizResults");
      router.push({
        path: `/quiz-master/user/${userId.value}/dashboard/quiz`,
        replace: true,
      });
    };

    // Restart the exam
    const restartExam = () => {
      // Set flag to prevent re-saving
      isNavigatingAway.value = true;
      // Clear any existing quiz state
      localStorage.removeItem(getResultsStorageKey());

      // Clear any existing quiz state in localStorage
      const quizStateKey = `quizState_${quizId}_${
        store.state.user?.id || "guest"
      }`;
      localStorage.removeItem(quizStateKey);

      // Clear quiz state from store
      store.commit("clearQuizState");
      // Clear quiz results from store
      store.commit("clearQuizResults");

      // Navigate back to the quiz page
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

    // Fetch results from API if not in store or local storage
    const fetchResults = async () => {
      try {
        isLoading.value = true;
        const response = await fetch(
          `http://127.0.0.1:5000/api/user/dashboard/quiz/${quizId}/results`
        );
        if (response.ok) {
          const data = await response.json();

          // Log the data structure to debug
          console.log("API response data:", data);

          // Process the data to ensure it has the expected structure
          const processedData = {
            ...data,
            questions: data.questions.map((q) => ({
              ...q,
              // Ensure both question and question_text are available
              question: q.question || q.question_text,
              question_text: q.question_text || q.question,
              // Ensure both answer and correct_option are available
              answer: q.answer || q.correct_option,
              correct_option: q.correct_option || q.answer,
            })),
          };

          results.value = processedData;
          // Save fetched results to local storage
          saveResultsToLocalStorage(processedData);
        } else {
          console.error("Failed to fetch quiz results");
          router.push("/dashboard");
        }
      } catch (error) {
        console.error("Error fetching quiz results:", error);
        router.push("/dashboard");
      } finally {
        isLoading.value = false;
      }
    };

    onMounted(() => {
      console.log("Component mounted, quizId:", quizId);

      // First check if results are in local storage
      const localResults = loadResultsFromLocalStorage();
      if (localResults) {
        console.log("Loaded quiz results from localStorage", localResults);
        results.value = localResults;
        isLoading.value = false;
        return;
      }

      // Then check if results are in the store
      const storedResults = store.state.quiz?.quizResults;
      console.log("Store results:", storedResults);

      if (storedResults && storedResults.quizId === quizId) {
        results.value = storedResults;
        // Save to local storage for persistence
        saveResultsToLocalStorage(storedResults);
        isLoading.value = false;
      } else {
        // If not in store or local storage, fetch from API
        fetchResults();
      }
    });

    // Save results to local storage when component is unmounted (but not when going to dashboard)
    onBeforeUnmount(() => {
      if (results.value.quizId && !isNavigatingAway.value) {
        saveResultsToLocalStorage(results.value);
      }
    });

    return {
      results,
      isLoading,
      formatTimeTaken,
      goToDashboard,
      restartExam,
      isNavigatingAway, // Add this to the returned object
    };
  },
};
</script>

<style scoped>
/* Base Styles */
.results-container {
  min-height: 100vh;
  width: 100%;
  background: linear-gradient(135deg, #3a0ca3, #4361ee, #8e44ad);
  color: white;
  font-family: "Segoe UI", Tahoma, Geneva, Verdana, sans-serif;
}

.dark-mode {
  background: #1e1e1e;
  color: #ffffff;
}

.results-page {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  padding: 2rem;
}

.results-card {
  background: rgba(0, 0, 0, 0.7);
  border-radius: 12px;
  padding: 2rem;
  width: 100%;
  max-width: 900px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
}

.dark-mode .results-card {
  background: rgba(30, 30, 30, 0.9);
}

.results-card h1 {
  color: #ffcd3c;
  text-align: center;
  margin-bottom: 2rem;
}

.results-summary {
  display: flex;
  justify-content: space-around;
  margin-bottom: 2rem;
  flex-wrap: wrap;
  gap: 1.5rem;
}

.result-item {
  text-align: center;
  padding: 1.5rem;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 8px;
  min-width: 200px;
  flex: 1;
}

.result-item h3 {
  color: #ffcd3c;
  margin-top: 0;
  margin-bottom: 1rem;
}

.score,
.percentage,
.time-taken {
  font-size: 2rem;
  font-weight: bold;
}

.results-details {
  margin-top: 2rem;
}

.results-details h3 {
  color: #ffcd3c;
  margin-bottom: 1.5rem;
}

.question-analysis {
  background: rgba(255, 255, 255, 0.1);
  border-radius: 8px;
  padding: 1.5rem;
  margin-bottom: 1.5rem;
}

.question-analysis .question-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.question-analysis h4 {
  margin: 0;
  color: white;
}

.question-result {
  padding: 0.5rem 1rem;
  border-radius: 4px;
  font-weight: bold;
}

.question-result.correct {
  background-color: #198754;
}

.question-result.incorrect {
  background-color: #dc3545;
}

.question-result.unanswered {
  background-color: #6c757d;
}

.options-analysis {
  margin-top: 1rem;
}

.options-analysis .option-item {
  margin-bottom: 0.75rem;
  display: flex;
  align-items: center;
  padding: 0.75rem;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 8px;
}

.option-item.user-selected {
  border: 2px solid #0dcaf0;
}

.option-item.correct-answer {
  border: 2px solid #198754;
  background: rgba(25, 135, 84, 0.2);
}

.option-item.user-selected.correct-answer {
  background: rgba(25, 135, 84, 0.4);
}

.option-marker {
  width: 36px;
  height: 36px;
  display: flex;
  justify-content: center;
  align-items: center;
  background: rgba(0, 0, 0, 0.5);
  border-radius: 50%;
  margin-right: 1rem;
  font-weight: bold;
}

.option-text {
  flex: 1;
}

.action-buttons {
  display: flex;
  gap: 1rem;
  margin-top: 2rem;
}

.btn-primary,
.btn-secondary {
  flex: 1;
  background-color: #0d6efd;
  color: white;
  border: none;
  border-radius: 4px;
  padding: 0.75rem 1.5rem;
  cursor: pointer;
  font-weight: bold;
  transition: all 0.2s ease;
}

.btn-primary:hover {
  background-color: #0b5ed7;
}

.btn-secondary {
  background-color: #6c757d;
}

.btn-secondary:hover {
  background-color: #5c636a;
}

/* Loading Styles */
.loading-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  background: rgba(0, 0, 0, 0.7);
  border-radius: 12px;
  padding: 3rem;
  width: 100%;
  max-width: 400px;
}

.loading-spinner {
  width: 50px;
  height: 50px;
  border: 5px solid rgba(255, 255, 255, 0.3);
  border-radius: 50%;
  border-top-color: #ffcd3c;
  animation: spin 1s ease-in-out infinite;
  margin-bottom: 1rem;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

/* Responsive Design */
@media (max-width: 768px) {
  .results-card {
    padding: 1.5rem;
  }

  .results-summary {
    flex-direction: column;
  }

  .result-item {
    width: 100%;
  }

  .score,
  .percentage,
  .time-taken {
    font-size: 1.5rem;
  }

  .action-buttons {
    flex-direction: column;
  }
}
</style>
