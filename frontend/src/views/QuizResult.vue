<template>
  <div
    class="results-container"
    :class="{ 'dark-mode': isDarkMode }"
    :data-bs-theme="isDarkMode ? 'dark' : 'light'"
  >
    <div class="results-page">
      <div class="results-card">
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
                  correct:
                    results.userAnswers[index] === question.correctAnswer,
                  incorrect:
                    results.userAnswers[index] &&
                    results.userAnswers[index] !== question.correctAnswer,
                  unanswered: !results.userAnswers[index],
                }"
              >
                {{
                  results.userAnswers[index]
                    ? results.userAnswers[index] === question.correctAnswer
                      ? "Correct"
                      : "Incorrect"
                    : "Not Attempted"
                }}
              </div>
            </div>

            <p class="question-text">{{ question.question }}</p>

            <div class="options-analysis">
              <div
                v-for="(option, optIndex) in question.options"
                :key="optIndex"
                class="option-item"
                :class="{
                  'user-selected': results.userAnswers[index] === option,
                  'correct-answer': option === question.correctAnswer,
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

        <button @click="goToDashboard" class="btn-primary">
          Back to Dashboard
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted, watch } from "vue";
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

    const isDarkMode = ref(false);
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

    // Format time taken for display
    const formatTimeTaken = (seconds) => {
      const minutes = Math.floor(seconds / 60);
      const remainingSeconds = seconds % 60;
      return `${minutes} min ${remainingSeconds} sec`;
    };

    // Go back to dashboard
    const goToDashboard = () => {
      router.push("/dashboard");
    };

    // Fetch results from API if not in store
    const fetchResults = async () => {
      try {
        const response = await fetch(
          `http://127.0.0.1:5000/api/user/dashboard/quiz/${quizId}/results`
        );
        if (response.ok) {
          const data = await response.json();
          results.value = data;
        } else {
          console.error("Failed to fetch quiz results");
          router.push("/dashboard");
        }
      } catch (error) {
        console.error("Error fetching quiz results:", error);
        router.push("/dashboard");
      }
    };

    // Watch for dark mode changes from system or user preference
    watch(
      () => store.state.theme?.darkMode,
      (newValue) => {
        isDarkMode.value = newValue;
      },
      { immediate: true }
    );

    onMounted(() => {
      // Check if results are in the store
      const storedResults = store.state.quiz?.quizResults;
      if (storedResults && storedResults.quizId === quizId) {
        results.value = storedResults;
      } else {
        // If not in store, fetch from API
        fetchResults();
      }

      // Check if dark mode is enabled in the store
      if (
        store.state.theme &&
        typeof store.state.theme.darkMode !== "undefined"
      ) {
        isDarkMode.value = store.state.theme.darkMode;
      } else {
        // Check system preference if store doesn't have the value
        const prefersDark = window.matchMedia(
          "(prefers-color-scheme: dark)"
        ).matches;
        isDarkMode.value = prefersDark;
        // Set in store
        if (store.state.theme) {
          store.commit("theme/setDarkMode", prefersDark);
        }
      }
    });

    return {
      isDarkMode,
      results,
      formatTimeTaken,
      goToDashboard,
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

.btn-primary {
  background-color: #0d6efd;
  color: white;
  border: none;
  border-radius: 4px;
  padding: 0.75rem 1.5rem;
  cursor: pointer;
  font-weight: bold;
  transition: all 0.2s ease;
  display: block;
  margin: 2rem auto 0;
}

.btn-primary:hover {
  background-color: #0b5ed7;
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
}
</style>
