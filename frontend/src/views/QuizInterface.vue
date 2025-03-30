<template>
  <div class="quiz-container" :class="{ 'dark-mode': isDarkMode }">
    <div v-if="userProfile && quizData">
      <!-- Instructions Page -->
      <div v-if="!isQuizStarted" class="instructions-page">
        <div class="instructions-card">
          <h1 class="exam-title">{{ quizData.title }}</h1>
          <div class="user-info">
            <div class="user-photo">
              <img
                v-if="userProfile && userProfile.profile_url"
                :src="userProfile.profile_url"
                alt="User Photo"
              />
              <div v-else class="avatar-placeholder">
                <span>{{ getUserInitials() }}</span>
              </div>
            </div>
            <div class="user-details">
              <p><strong>Name:</strong> {{ userProfile?.fullname }}</p>
              <p><strong>ID:</strong> {{ userProfile?.id }}</p>
              <p><strong>Duration:</strong> {{ quizData.duration }} minutes</p>
            </div>
          </div>

          <div class="instructions-content">
            <h3>Instructions:</h3>
            <ul>
              <li
                v-for="(instruction, index) in quizData.instructions"
                :key="index"
              >
                {{ instruction }}
              </li>
              <li>
                The questions panel on the right shows the status of each
                question:
              </li>
              <div class="legend">
                <div class="legend-item">
                  <span class="status-indicator not-visited"></span> Not Visited
                </div>
                <div class="legend-item">
                  <span class="status-indicator current"></span> Current
                  Question
                </div>
                <div class="legend-item">
                  <span class="status-indicator answered"></span> Answered
                </div>
                <div class="legend-item">
                  <span class="status-indicator not-answered"></span> Not
                  Answered
                </div>
                <div class="legend-item">
                  <span class="status-indicator marked"></span> Marked for
                  Review
                </div>
              </div>
              <li>
                You can navigate between questions using the question panel or
                navigation buttons.
              </li>
              <li>
                Click "Submit Exam" only when you are sure you want to finish
                the exam.
              </li>
              <li>
                Your answers are automatically saved when you navigate to
                another question.
              </li>
              <li v-if="hasInProgressQuiz" class="resume-notice">
                You have an in-progress quiz. You can resume from where you left
                off.
              </li>
            </ul>
          </div>

          <div class="start-buttons">
            <button
              v-if="hasInProgressQuiz"
              @click="resumeQuiz"
              class="btn-secondary resume-btn"
            >
              Resume Quiz
            </button>
            <button @click="startQuiz" class="btn-primary start-btn">
              {{ hasInProgressQuiz ? "Restart Quiz" : "Start Exam" }}
            </button>
          </div>
        </div>
      </div>

      <!-- Exam Interface -->
      <div v-else class="exam-interface">
        <!-- Header -->
        <div class="exam-header">
          <div class="exam-info">
            <h2>{{ quizData.title }}</h2>
          </div>
          <div class="header-right">
            <div class="timer-container">
              <div class="timer" :class="{ 'timer-warning': timeLeft < 300 }">
                {{ formattedTime }}
              </div>
            </div>
            <div class="user-profile">
              <div v-if="userProfile && userProfile.photo" class="user-avatar">
                <img :src="userProfile.photo" alt="User Photo" />
              </div>
              <div v-else class="user-avatar-placeholder">
                <span>{{ getUserInitials() }}</span>
              </div>
              <div class="user-brief">
                <p>
                  {{ userProfile?.name || "User" }} | ID:
                  {{ userProfile?.id || "N/A" }}
                </p>
              </div>
            </div>
          </div>
        </div>

        <!-- Main Content -->
        <div class="exam-content">
          <!-- Question Area -->
          <div class="question-area">
            <div class="question-header">
              <h3>Question {{ currentQuestionIndex + 1 }}</h3>
              <div class="question-actions">
                <button
                  @click="markForReview"
                  class="btn-secondary mark-btn"
                  :class="{
                    marked: questionStatus[currentQuestionIndex] === 'marked',
                  }"
                >
                  {{
                    questionStatus[currentQuestionIndex] === "marked"
                      ? "Unmark"
                      : "Mark for Review"
                  }}
                </button>
              </div>
            </div>

            <div class="question-content">
              <p class="question-text">{{ currentQuestion.question_text }}</p>

              <div class="options-list">
                <div
                  v-for="(option, optIndex) in currentQuestion.options"
                  :key="optIndex"
                  class="option-item"
                  :class="{
                    selected: userAnswers[currentQuestionIndex] === optIndex,
                  }"
                  @click="selectOption(optIndex)"
                >
                  <div class="option-marker">
                    {{ ["A", "B", "C", "D"][optIndex] }}
                  </div>
                  <div class="option-text">{{ option }}</div>
                </div>
              </div>
            </div>

            <div class="navigation-buttons">
              <button
                @click="previousQuestion"
                class="btn-secondary"
                :disabled="currentQuestionIndex === 0"
              >
                Previous
              </button>
              <button
                @click="clearResponse"
                class="btn-secondary"
                :disabled="!userAnswers[currentQuestionIndex]"
              >
                Clear Response
              </button>
              <button
                @click="saveAndNext"
                class="btn-primary"
                :disabled="
                  currentQuestionIndex === quizData.questions.length - 1
                "
              >
                Save & Next
              </button>
            </div>
          </div>

          <!-- Questions Panel -->
          <div class="questions-panel">
            <div class="panel-header">
              <h3>Questions</h3>
            </div>

            <div class="question-numbers">
              <div
                v-for="(_, index) in quizData.questions"
                :key="index"
                class="question-number"
                :class="getQuestionStatusClass(index)"
                @click="goToQuestion(index)"
              >
                {{ index + 1 }}
              </div>
            </div>

            <div class="panel-summary">
              <div class="summary-item">
                <span class="status-indicator answered"></span>
                <span
                  >Answered: {{ getQuestionCountByStatus("answered") }}</span
                >
              </div>
              <div class="summary-item">
                <span class="status-indicator not-answered"></span>
                <span
                  >Not Answered:
                  {{ getQuestionCountByStatus("not-answered") }}</span
                >
              </div>
              <div class="summary-item">
                <span class="status-indicator not-visited"></span>
                <span
                  >Not Visited:
                  {{ getQuestionCountByStatus("not-visited") }}</span
                >
              </div>
              <div class="summary-item">
                <span class="status-indicator marked"></span>
                <span>Marked: {{ getQuestionCountByStatus("marked") }}</span>
              </div>
            </div>

            <button @click="confirmSubmit" class="btn-submit">
              Submit Exam
            </button>
          </div>
        </div>
      </div>
    </div>
    <div v-else>
      <div class="position-absolute top-50 start-50 translate-middle">
        <div class="spinner-border text-primary" role="status">
          <span class="visually-hidden">Loading...</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, reactive, computed, onMounted, onBeforeUnmount } from "vue";
import { useRouter } from "vue-router";
import { useRoute } from "vue-router";
import { useStore } from "vuex";

export default {
  name: "QuizPage",
  setup() {
    // ===== SETUP AND INITIALIZATION =====
    const router = useRouter();
    const route = useRoute();
    const store = useStore();
    const quizId = route.params.quiz_id;

    // Get user ID from store
    const userId = computed(() => store.state.user?.id);
    const role = ref(null);

    // Get dark mode from store
    const isDarkMode = computed(() => store.getters.isDarkMode);

    // Flag to track if there's an in-progress quiz
    const hasInProgressQuiz = ref(false);

    // Flag to prevent auto-saving during submission
    const isSubmitting = ref(false);

    // Quiz state variables
    const isQuizStarted = ref(false);
    const timeLeft = ref(0);
    const timeTaken = ref(0);
    let timer;

    // User profile data
    const userProfile = ref(null);
    const quizData = reactive({
      title: "",
      duration: 0,
      questions: [],
    });

    // User answers and question status tracking
    const userAnswers = ref([]);
    const questionStatus = ref([]);
    const visitedQuestions = ref([]);
    const currentQuestionIndex = ref(0);

    // ===== COMPUTED PROPERTIES =====

    // Format time for display
    const formattedTime = computed(() => {
      const minutes = Math.floor(timeLeft.value / 60);
      const seconds = timeLeft.value % 60;
      return `${minutes}:${seconds < 10 ? "0" : ""}${seconds}`;
    });

    // Get current question
    const currentQuestion = computed(() => {
      return quizData.questions[currentQuestionIndex.value] || {};
    });

    // ===== HELPER FUNCTIONS =====

    // Initialize question status
    const initializeQuestionStatus = () => {
      questionStatus.value = Array(quizData.questions.length).fill(
        "not-visited"
      );
      userAnswers.value = Array(quizData.questions.length).fill(null);
      visitedQuestions.value = [];
    };

    // Get user initials for avatar placeholder
    const getUserInitials = () => {
      if (userProfile.value && userProfile.value.name) {
        const names = userProfile.value.name.split(" ");
        if (names.length >= 2) {
          return `${names[0][0]}${names[1][0]}`.toUpperCase();
        }
        return names[0][0].toUpperCase();
      }
      return "U";
    };

    // Generate a unique storage key for this quiz and user
    const getStorageKey = () => {
      return `quizState_${quizId}_${userId.value}`;
    };

    // ===== LOCAL STORAGE FUNCTIONS =====

    // Save quiz state to localStorage
    const saveQuizStateToLocalStorage = () => {
      // Don't save if we're in the process of submitting
      if (isSubmitting.value) {
        console.log("Skipping save during submission");
        return;
      }

      const stateToSave = {
        quizId,
        userId: userId.value,
        isStarted: isQuizStarted.value,
        currentQuestion: currentQuestionIndex.value,
        userAnswers: userAnswers.value,
        questionStatus: questionStatus.value,
        visitedQuestions: visitedQuestions.value,
        timeLeft: timeLeft.value,
        timeTaken: timeTaken.value,
        timestamp: new Date().getTime(),
        duration: quizData.duration,
      };

      try {
        localStorage.setItem(getStorageKey(), JSON.stringify(stateToSave));
        console.log("Quiz state saved to localStorage");

        // Also update the Vuex store
        store.dispatch("saveQuizState", stateToSave);
      } catch (error) {
        console.error("Error saving quiz state to localStorage:", error);
      }
    };

    // Load quiz state from localStorage
    const loadQuizStateFromLocalStorage = () => {
      try {
        const savedState = JSON.parse(localStorage.getItem(getStorageKey()));

        if (savedState && savedState.quizId === quizId) {
          console.log("Found saved quiz state");

          // Check if the saved state is still valid (not expired)
          const currentTime = new Date().getTime();
          const savedTime = savedState.timestamp;
          const elapsedSeconds = Math.floor((currentTime - savedTime) / 1000);

          // If the elapsed time is less than the quiz duration, the quiz is still valid
          if (elapsedSeconds < savedState.duration * 60) {
            hasInProgressQuiz.value = true;
            return savedState;
          } else {
            console.log("Saved quiz state has expired. Starting fresh.");
            localStorage.removeItem(getStorageKey());
          }
        }
      } catch (error) {
        console.error("Error loading quiz state from localStorage:", error);
      }

      return null;
    };

    // ===== QUIZ CONTROL FUNCTIONS =====

    // Start the timer
    const startTimer = () => {
      // Clear any existing timer
      if (timer) {
        clearInterval(timer);
      }

      timer = setInterval(() => {
        if (timeLeft.value > 0) {
          timeLeft.value--;
          timeTaken.value++;

          // Save state every 10 seconds
          if (timeLeft.value % 10 === 0) {
            saveQuizStateToLocalStorage();
          }
        } else {
          clearInterval(timer);
          alert("Time is up! Submitting your exam automatically.");
          submitExam();
        }
      }, 1000);
    };

    // Resume quiz from saved state
    const resumeQuiz = () => {
      const savedState = loadQuizStateFromLocalStorage();

      if (savedState) {
        isQuizStarted.value = true;
        currentQuestionIndex.value = savedState.currentQuestion;
        userAnswers.value = savedState.userAnswers;
        questionStatus.value = savedState.questionStatus;
        visitedQuestions.value = savedState.visitedQuestions || [];

        // Calculate remaining time
        const currentTime = new Date().getTime();
        const savedTime = savedState.timestamp;
        const elapsedSeconds = Math.floor((currentTime - savedTime) / 1000);

        // Adjust timeLeft based on elapsed time since the quiz was saved
        timeLeft.value = Math.max(0, savedState.timeLeft - elapsedSeconds);
        timeTaken.value = savedState.timeTaken + elapsedSeconds;

        // Start timer
        startTimer();

        // Update store
        store.dispatch("saveQuizState", {
          quizId,
          isStarted: isQuizStarted.value,
          currentQuestion: currentQuestionIndex.value,
          userAnswers: userAnswers.value,
          questionStatus: questionStatus.value,
          timeLeft: timeLeft.value,
          timeTaken: timeTaken.value,
        });
      } else {
        // If no valid saved state, start a new quiz
        startQuiz();
      }
    };

    // Start the quiz
    const startQuiz = async () => {
      try {
        // Record quiz start in database
        const response = await fetch(
          `http://127.0.0.1:5000/api/user/dashboard/quiz/${quizId}/submit`,
          {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
              "Authentication-Token": store.state.user?.token,
            },
            body: JSON.stringify({
              quizId,
              userId: userId.value,
              startTime: new Date().toISOString(),
            }),
          }
        );

        if (!response.ok) {
          console.error("Failed to record quiz start");
        }
      } catch (error) {
        console.error("Error recording quiz start:", error);
      }

      // Clear any existing saved state
      localStorage.removeItem(getStorageKey());
      store.dispatch("clearSavedQuizState", { quizId, userId: userId.value });

      // Initialize quiz state
      isQuizStarted.value = true;
      timeLeft.value = quizData.duration * 60;
      timeTaken.value = 0;
      initializeQuestionStatus();
      currentQuestionIndex.value = 0;

      // Mark first question as current
      questionStatus.value[0] = "current";
      visitedQuestions.value = [0];

      // Start timer
      startTimer();

      // Save initial state
      saveQuizStateToLocalStorage();
    };

    // ===== QUESTION NAVIGATION AND INTERACTION =====

    // Navigate to a specific question
    const goToQuestion = (index) => {
      // Update status of current question before changing
      updateCurrentQuestionStatus();

      // Set new current question
      currentQuestionIndex.value = index;

      // Mark as visited if not already
      if (!visitedQuestions.value.includes(index)) {
        visitedQuestions.value.push(index);
      }

      // Update status of new current question
      questionStatus.value[index] = "current";

      // Save state
      saveQuizStateToLocalStorage();
    };

    // Update status of current question based on answer
    const updateCurrentQuestionStatus = () => {
      const index = currentQuestionIndex.value;

      // Don't change if marked for review
      if (questionStatus.value[index] === "marked") {
        return;
      }

      if (
        userAnswers.value[index] !== null &&
        userAnswers.value[index] !== undefined
      ) {
        questionStatus.value[index] = "answered";
      } else if (visitedQuestions.value.includes(index)) {
        questionStatus.value[index] = "not-answered";
      }
    };

    // Select an option for the current question
    const selectOption = (optIndex) => {
      userAnswers.value[currentQuestionIndex.value] = optIndex;
      saveQuizStateToLocalStorage();
    };

    // Clear response for current question
    const clearResponse = () => {
      userAnswers.value[currentQuestionIndex.value] = null;
      saveQuizStateToLocalStorage();
    };

    // Save answer and go to next question
    const saveAndNext = () => {
      if (currentQuestionIndex.value < quizData.questions.length - 1) {
        updateCurrentQuestionStatus();
        currentQuestionIndex.value++;

        // Mark as visited if not already
        if (!visitedQuestions.value.includes(currentQuestionIndex.value)) {
          visitedQuestions.value.push(currentQuestionIndex.value);
        }

        questionStatus.value[currentQuestionIndex.value] = "current";
        saveQuizStateToLocalStorage();
      }
    };

    // Go to previous question
    const previousQuestion = () => {
      if (currentQuestionIndex.value > 0) {
        updateCurrentQuestionStatus();
        currentQuestionIndex.value--;
        questionStatus.value[currentQuestionIndex.value] = "current";
        saveQuizStateToLocalStorage();
      }
    };

    // Mark question for review
    const markForReview = () => {
      const index = currentQuestionIndex.value;
      questionStatus.value[index] =
        questionStatus.value[index] === "marked"
          ? userAnswers.value[index] !== null &&
            userAnswers.value[index] !== undefined
            ? "answered"
            : "not-answered"
          : "marked";
      saveQuizStateToLocalStorage();
    };

    // ===== QUESTION STATUS HELPERS =====

    // Get CSS class for question number based on status
    const getQuestionStatusClass = (index) => {
      if (index === currentQuestionIndex.value) return "current";
      return questionStatus.value[index];
    };

    // Count questions by status
    const getQuestionCountByStatus = (status) => {
      if (status === "not-visited") {
        return quizData.questions.length - visitedQuestions.value.length;
      }
      return questionStatus.value.filter((s) => s === status).length;
    };

    // ===== API CALLS =====

    // Fetch user profile
    const fetchUserProfile = async () => {
      try {
        const response = await fetch(
          `http://127.0.0.1:5000/api/user/${userId.value}/data`,
          {
            method: "GET",
            headers: {
              "Content-Type": "application/json",
              "Authentication-Token": store.state.user?.token,
            },
          }
        );
        if (response.ok) {
          userProfile.value = await response.json();
        }
      } catch (error) {
        console.error("Failed to fetch user profile:", error);
        alert("Failed to fetch user profile. Please try again later.");
        router.push("/");
      }
    };

    // Fetch quiz data from API
    const fetchQuizData = async () => {
      try {
        const response = await fetch(
          `http://127.0.0.1:5000/api/user/dashboard/quiz/${quizId}/quiz-data`,
          {
            method: "GET",
            headers: {
              "Content-Type": "application/json",
              "Authentication-Token": store.state.user?.token,
            },
          }
        );
        if (!response.ok) {
          throw new Error("Failed to fetch quiz data");
        }
        const data = await response.json();
        quizData.title = data.title;
        quizData.duration = data.duration;
        quizData.instructions = data.instructions;
        quizData.questions = data.questions;

        // Initialize after fetching data
        initializeQuestionStatus();

        // Check if there's a saved state
        const savedState = loadQuizStateFromLocalStorage();
        hasInProgressQuiz.value = !!savedState;
      } catch (error) {
        console.error("Failed to fetch quiz data:", error);
        alert("Failed to fetch quiz data. Please try again later.");
        router.push("/");
        // Initialize with mock data if fetch fails
        initializeQuestionStatus();

        // Still check for saved state with mock data
        const savedState = loadQuizStateFromLocalStorage();
        hasInProgressQuiz.value = !!savedState;
      }
    };

    // ===== QUIZ SUBMISSION =====

    // Confirm before submitting
    const confirmSubmit = () => {
      const unansweredCount = userAnswers.value.filter(
        (a) => a === null || a === undefined
      ).length;

      if (unansweredCount > 0) {
        const confirm = window.confirm(
          `You have ${unansweredCount} unanswered questions. Are you sure you want to submit?`
        );
        if (confirm) {
          submitExam();
        }
      } else {
        submitExam();
      }
    };

    // Submit the exam
    const submitExam = async () => {
      // Set submitting flag to prevent auto-saving
      isSubmitting.value = true;

      // Stop the timer
      clearInterval(timer);

      // Calculate score
      const score = userAnswers.value.reduce((total, answer, index) => {
        // Convert the correct_option from 1-based to 0-based for comparison
        const correctAnswer = quizData.questions[index].correct_option - 1;
        return total + (answer === correctAnswer ? 1 : 0);
      }, 0);
      console.log("Score:", score);

      // Prepare results object
      const resultsData = {
        quizId,
        quizTitle: quizData.title,
        questions: quizData.questions,
        userAnswers: userAnswers.value,
        score: score,
        totalScore: quizData.questions.length,
        percentage: Math.round((score / quizData.questions.length) * 100),
        timeTaken: timeTaken.value,
      };

      try {
        // Submit results to backend
        const response = await fetch(
          `http://127.0.0.1:5000/api/user/dashboard/quiz/${quizId}/submit`,
          {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
              "Authentication-Token": store.state.user?.token,
            },
            body: JSON.stringify({
              quizId,
              userId: userId.value,
              answers: userAnswers.value,
              score: score,
              totalScore: quizData.questions.length,
              percentage: Math.round((score / quizData.questions.length) * 100),
              timeTaken: timeTaken.value,
            }),
          }
        );

        if (!response.ok) {
          console.error("Failed to submit quiz results");
        }
      } catch (error) {
        console.error("Error submitting quiz results:", error);
      }

      // Save results to Vuex store for the results page
      store.dispatch("saveQuizResults", resultsData);

      // Save results to local storage for persistence
      const resultsStorageKey = `quizResults_${quizId}`;
      localStorage.setItem(resultsStorageKey, JSON.stringify(resultsData));

      // Clear quiz state from localStorage
      localStorage.removeItem(getStorageKey());

      // Clear quiz state from store
      store.commit("clearQuizState");

      // Redirect to results page
      const routeRole = router.currentRoute.value.params.role;
      const userRoles = store.state.user?.roles || [];

      if (
        Array.isArray(userRoles) &&
        userRoles.map((r) => r.name).includes(routeRole)
      ) {
        role.value = routeRole;
        const route = `/quiz-master/${role.value}/${userId.value}/dashboard/quiz/${quizId}/result`;
        router.push(route);
      } else {
        console.error("Role in route does not match any user roles.");
        // Fallback route if role doesn't match
        router.push(`/dashboard/quiz/${quizId}/result`);
      }
    };

    // ===== LIFECYCLE HOOKS =====

    onMounted(() => {
      fetchUserProfile();
      fetchQuizData();

      // Set up window beforeunload event to save state when user leaves
      window.addEventListener("beforeunload", () => {
        if (isQuizStarted.value && timeLeft.value > 0 && !isSubmitting.value) {
          saveQuizStateToLocalStorage();
        }
      });
    });

    onBeforeUnmount(() => {
      if (timer) {
        clearInterval(timer);
      }

      // Save state when component is unmounted
      if (isQuizStarted.value && timeLeft.value > 0 && !isSubmitting.value) {
        saveQuizStateToLocalStorage();
      }

      // Remove beforeunload event listener
      window.removeEventListener("beforeunload", () => {});
    });

    return {
      isQuizStarted,
      isDarkMode,
      quizData,
      userProfile,
      userAnswers,
      currentQuestionIndex,
      currentQuestion,
      questionStatus,
      formattedTime,
      timeLeft,
      hasInProgressQuiz,
      getUserInitials,
      startQuiz,
      resumeQuiz,
      goToQuestion,
      selectOption,
      clearResponse,
      saveAndNext,
      previousQuestion,
      markForReview,
      getQuestionStatusClass,
      getQuestionCountByStatus,
      confirmSubmit,
      submitExam,
    };
  },
};
</script>

<style scoped>
.spinner-border {
  width: 3rem;
  height: 3rem;
}
/* Base Styles */
.quiz-container {
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

/* Instructions Page */
.instructions-page {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  padding: 2rem;
}

.instructions-card {
  background: rgba(0, 0, 0, 0.7);
  border-radius: 12px;
  padding: 2rem;
  width: 100%;
  max-width: 800px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
}

.dark-mode .instructions-card {
  background: rgba(30, 30, 30, 0.9);
}

.exam-title {
  color: #ffcd3c;
  text-align: center;
  margin-bottom: 1.5rem;
}

.user-info {
  display: flex;
  align-items: center;
  margin-bottom: 2rem;
  background: rgba(255, 255, 255, 0.1);
  padding: 1rem;
  border-radius: 8px;
}

.user-photo {
  margin-right: 1.5rem;
  width: 100px;
  height: 100px;
}

.user-photo img {
  width: 100%;
  height: 100%;
  border-radius: 50%;
  border: 3px solid #ffcd3c;
  object-fit: cover;
}

.avatar-placeholder {
  width: 100%;
  height: 100%;
  border-radius: 50%;
  border: 3px solid #ffcd3c;
  background-color: #6c757d;
  display: flex;
  justify-content: center;
  align-items: center;
  font-size: 2.5rem;
  font-weight: bold;
  color: white;
}

.user-details {
  flex: 1;
}

.user-details p {
  margin: 0.5rem 0;
}

.instructions-content {
  margin-bottom: 2rem;
}

.instructions-content h3 {
  color: #ffcd3c;
  margin-bottom: 1rem;
}

.instructions-content ul {
  padding-left: 1.5rem;
}

.instructions-content li {
  margin-bottom: 0.75rem;
}

.resume-notice {
  color: #ffcd3c;
  font-weight: bold;
  margin-top: 1rem;
}

.legend {
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
  margin: 1rem 0;
  padding: 1rem;
  background: rgba(255, 255, 255, 0.05);
  border-radius: 8px;
}

.legend-item {
  display: flex;
  align-items: center;
  margin-right: 1rem;
}

.status-indicator {
  display: inline-block;
  width: 20px;
  height: 20px;
  border-radius: 4px;
  margin-right: 0.5rem;
}

.not-visited {
  background-color: #6c757d;
}

.current {
  background-color: #0dcaf0;
}

.answered {
  background-color: #198754;
}

.not-answered {
  background-color: #dc3545;
}

.marked {
  background-color: #6f42c1;
}

.start-buttons {
  display: flex;
  gap: 1rem;
  margin-top: 2rem;
}

.start-btn {
  flex: 1;
  padding: 1rem;
  font-size: 1.25rem;
  font-weight: bold;
}

.resume-btn {
  flex: 1;
  padding: 1rem;
  font-size: 1.25rem;
  font-weight: bold;
}

/* Exam Interface */
.exam-interface {
  display: flex;
  flex-direction: column;
  height: 100vh;
  overflow: hidden;
}

.exam-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.5rem 1rem;
  background: rgba(0, 0, 0, 0.8);
  border-bottom: 2px solid #ffcd3c;
  height: 60px;
}

.dark-mode .exam-header {
  background: rgba(30, 30, 30, 0.9);
}

.exam-info h2 {
  margin: 0;
  color: #ffcd3c;
  font-size: 1.25rem;
}

.header-right {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.user-profile {
  display: flex;
  align-items: center;
}

.user-avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  border: 2px solid #ffcd3c;
  margin-right: 0.5rem;
  overflow: hidden;
}

.user-avatar img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.user-avatar-placeholder {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  border: 2px solid #ffcd3c;
  background-color: #6c757d;
  display: flex;
  justify-content: center;
  align-items: center;
  font-size: 1rem;
  font-weight: bold;
  color: white;
  margin-right: 0.5rem;
}

.user-brief p {
  margin: 0;
  font-size: 0.8rem;
}

.timer-container {
  display: flex;
  align-items: center;
}

.timer {
  background-color: #dc3545;
  color: white;
  padding: 0.25rem 0.75rem;
  border-radius: 4px;
  font-weight: bold;
  font-size: 1rem;
}

.timer-warning {
  animation: pulse 1s infinite;
}

@keyframes pulse {
  0% {
    opacity: 1;
  }
  50% {
    opacity: 0.5;
  }
  100% {
    opacity: 1;
  }
}

.exam-content {
  display: flex;
  flex: 1;
  height: calc(100vh - 60px);
  overflow: hidden;
}

/* Question Area */
.question-area {
  flex: 1;
  padding: 1rem;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  height: 100%;
}

.question-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.question-header h3 {
  color: #ffcd3c;
  margin: 0;
  font-size: 1.1rem;
}

.question-actions {
  display: flex;
  gap: 0.5rem;
}

.mark-btn {
  padding: 0.25rem 0.75rem;
  font-size: 0.9rem;
}

.mark-btn.marked {
  background-color: #6f42c1;
  color: white;
}

.question-content {
  flex: 1;
  background: rgba(0, 0, 0, 0.5);
  padding: 1.5rem;
  border-radius: 8px;
  margin-bottom: 1rem;
  overflow-y: auto;
}

.dark-mode .question-content {
  background: rgba(30, 30, 30, 0.7);
}

.question-text {
  font-size: 1.1rem;
  margin-bottom: 1.5rem;
}

.options-list {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.option-item {
  display: flex;
  align-items: center;
  padding: 0.75rem;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.option-item:hover {
  background: rgba(255, 255, 255, 0.2);
}

.option-item.selected {
  background: rgba(255, 205, 60, 0.3);
  border: 2px solid #ffcd3c;
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
  font-size: 0.9rem;
}

.option-text {
  flex: 1;
  font-size: 0.95rem;
}

.navigation-buttons {
  display: flex;
  justify-content: space-between;
  gap: 0.75rem;
}

/* Questions Panel */
.questions-panel {
  width: 250px;
  background: rgba(0, 0, 0, 0.8);
  padding: 1rem;
  display: flex;
  flex-direction: column;
  border-left: 2px solid #ffcd3c;
  overflow-y: auto;
}

.dark-mode .questions-panel {
  background: rgba(30, 30, 30, 0.9);
}

.panel-header {
  margin-bottom: 1rem;
}

.panel-header h3 {
  color: #ffcd3c;
  margin: 0;
  text-align: center;
  font-size: 1.1rem;
}

.question-numbers {
  display: grid;
  grid-template-columns: repeat(5, 1fr);
  gap: 0.5rem;
  margin-bottom: 1.5rem;
}

.question-number {
  width: 36px;
  height: 36px;
  display: flex;
  justify-content: center;
  align-items: center;
  background: #6c757d;
  border-radius: 4px;
  cursor: pointer;
  font-weight: bold;
  font-size: 0.9rem;
  transition: all 0.2s ease;
}

.question-number:hover {
  transform: scale(1.05);
}

.question-number.current {
  background-color: #0dcaf0;
}

.question-number.answered {
  background-color: #198754;
}

.question-number.not-answered {
  background-color: #dc3545;
}

.question-number.marked {
  background-color: #6f42c1;
}

.panel-summary {
  margin-top: auto;
  margin-bottom: 1.5rem;
  background: rgba(255, 255, 255, 0.1);
  padding: 0.75rem;
  border-radius: 8px;
  font-size: 0.9rem;
}

.summary-item {
  display: flex;
  align-items: center;
  margin-bottom: 0.5rem;
}

.btn-submit {
  background-color: #dc3545;
  color: white;
  padding: 0.75rem;
  border: none;
  border-radius: 8px;
  font-weight: bold;
  font-size: 1.1rem;
  cursor: pointer;
  transition: all 0.2s ease;
}

.btn-submit:hover {
  background-color: #bb2d3b;
}

/* Button Styles */
.btn-primary {
  background-color: #0d6efd;
  color: white;
  border: none;
  border-radius: 4px;
  padding: 0.5rem 1rem;
  cursor: pointer;
  font-weight: bold;
  transition: all 0.2s ease;
}

.btn-primary:hover {
  background-color: #0b5ed7;
}

.btn-secondary {
  background-color: #6c757d;
  color: white;
  border: none;
  border-radius: 4px;
  padding: 0.5rem 1rem;
  cursor: pointer;
  font-weight: bold;
  transition: all 0.2s ease;
}

.btn-secondary:hover {
  background-color: #5c636a;
}

.btn-secondary:disabled,
.btn-primary:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

/* Responsive Design */
@media (max-width: 992px) {
  .exam-content {
    flex-direction: column;
    height: calc(100vh - 60px);
    overflow-y: auto;
  }

  .questions-panel {
    width: 100%;
    border-left: none;
    border-top: 2px solid #ffcd3c;
    order: -1;
  }

  .question-numbers {
    grid-template-columns: repeat(10, 1fr);
  }

  .exam-header {
    flex-wrap: wrap;
  }

  .question-area {
    height: auto;
  }

  .start-buttons {
    flex-direction: column;
  }
}

@media (max-width: 768px) {
  .question-numbers {
    grid-template-columns: repeat(5, 1fr);
  }

  .navigation-buttons {
    flex-direction: column;
  }

  .exam-header {
    padding: 0.5rem;
    height: auto;
  }

  .question-area {
    padding: 0.75rem;
  }
}
</style>
