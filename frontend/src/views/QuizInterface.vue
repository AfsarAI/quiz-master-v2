<template>
  <div class="quiz-container">
    <!-- Instructions Page -->
    <div v-if="!isQuizStarted" class="instructions-page">
      <div class="instructions-card">
        <h1 class="exam-title">{{ quizData.title }}</h1>
        <div class="user-info">
          <div class="user-photo">
            <img
              v-if="userProfile && userProfile.photo"
              :src="userProfile.photo"
              alt="User Photo"
            />
            <div v-else class="avatar-placeholder">
              <span>{{ getUserInitials() }}</span>
            </div>
          </div>
          <div class="user-details">
            <p><strong>Name:</strong> {{ userProfile?.name || "User" }}</p>
            <p><strong>ID:</strong> {{ userProfile?.id || "N/A" }}</p>
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
                <span class="status-indicator current"></span> Current Question
              </div>
              <div class="legend-item">
                <span class="status-indicator answered"></span> Answered
              </div>
              <div class="legend-item">
                <span class="status-indicator not-answered"></span> Not Answered
              </div>
              <div class="legend-item">
                <span class="status-indicator marked"></span> Marked for Review
              </div>
            </div>
            <li>
              You can navigate between questions using the question panel or
              navigation buttons.
            </li>
            <li>
              Click "Submit Exam" only when you are sure you want to finish the
              exam.
            </li>
            <li>
              Your answers are automatically saved when you navigate to another
              question.
            </li>
          </ul>
        </div>

        <button @click="startQuiz" class="btn-primary start-btn">
          Start Exam
        </button>
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
            <p class="question-text">{{ currentQuestion.question }}</p>

            <div class="options-list">
              <div
                v-for="(option, optIndex) in currentQuestion.options"
                :key="optIndex"
                class="option-item"
                :class="{
                  selected: userAnswers[currentQuestionIndex] === option,
                }"
                @click="selectOption(option)"
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
              :disabled="currentQuestionIndex === quizData.questions.length - 1"
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
              <span>Answered: {{ getQuestionCountByStatus("answered") }}</span>
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

          <button @click="confirmSubmit" class="btn-submit">Submit Exam</button>
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

    const isQuizStarted = ref(false);
    const timeLeft = ref(0);
    const timeTaken = ref(0);
    let timer;

    // User profile data
    const userProfile = ref(null);

    // Mock quiz data - will be replaced with API data
    const quizData = reactive({
      title: "General Knowledge Quiz",
      duration: 30,
      instructions: [
        "Each question has four options, choose the correct one.",
        "You can navigate between questions using the question panel or navigation buttons.",
        "Your time will end automatically if the timer runs out.",
        "Questions marked for review will be highlighted in purple.",
        "You can change your answers any time before submitting the exam.",
      ],
      questions: [
        {
          question: "What is the capital of France?",
          options: ["London", "Berlin", "Paris", "Madrid"],
          correctAnswer: "Paris",
        },
        {
          question: "Which planet is known as the Red Planet?",
          options: ["Venus", "Mars", "Jupiter", "Saturn"],
          correctAnswer: "Mars",
        },
        {
          question: "Who wrote 'Romeo and Juliet'?",
          options: [
            "Charles Dickens",
            "William Shakespeare",
            "Jane Austen",
            "Mark Twain",
          ],
          correctAnswer: "William Shakespeare",
        },
        {
          question: "What is the chemical symbol for gold?",
          options: ["Go", "Gd", "Au", "Ag"],
          correctAnswer: "Au",
        },
        {
          question: "Which country is home to the kangaroo?",
          options: ["New Zealand", "South Africa", "Australia", "Brazil"],
          correctAnswer: "Australia",
        },
      ],
    });

    // User answers and question status tracking
    const userAnswers = ref([]);
    const questionStatus = ref([]);
    const visitedQuestions = ref([]);

    // Initialize question status
    const initializeQuestionStatus = () => {
      questionStatus.value = Array(quizData.questions.length).fill(
        "not-visited"
      );
      userAnswers.value = Array(quizData.questions.length).fill(null);
      visitedQuestions.value = [];
    };

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

    // Current question index
    const currentQuestionIndex = ref(0);

    // Fetch user profile
    const fetchUserProfile = async () => {
      try {
        const response = await fetch("http://127.0.0.1:5000/api/user/profile");
        if (response.ok) {
          userProfile.value = await response.json();
        }
      } catch (error) {
        console.error("Failed to fetch user profile:", error);
        // Set default profile if fetch fails
        userProfile.value = {
          name: "Test User",
          id: "TEST123",
          photo: null,
        };
      }
    };

    // Fetch quiz data from API
    const fetchQuizData = async () => {
      try {
        const response = await fetch();
        `http://127.0.0.1:5000/api/user/dashboard/quiz/${quizId}/quiz-data`;
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
      } catch (error) {
        console.error("Failed to fetch quiz data:", error);
        // Initialize with mock data if fetch fails
        initializeQuestionStatus();
      }
    };

    // Start the quiz
    const startQuiz = async () => {
      try {
        // Record quiz start in database
        const response = await fetch(
          `http://127.0.0.1:5000/api/user/dashboard/quiz/${quizId}/start`,
          {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
            },
            body: JSON.stringify({
              quizId,
              userId: userProfile.value?.id || "user123",
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

      isQuizStarted.value = true;
      timeLeft.value = quizData.duration * 60;

      // Mark first question as current
      questionStatus.value[0] = "current";
      visitedQuestions.value.push(0);

      // Start timer
      timer = setInterval(() => {
        if (timeLeft.value > 0) {
          timeLeft.value--;
          timeTaken.value = quizData.duration * 60 - timeLeft.value;
        } else {
          clearInterval(timer);
          alert("Time is up! Submitting your exam automatically.");
          submitExam();
        }
      }, 1000);

      // Save quiz state to Vuex store
      store.commit("setQuizState", {
        quizId,
        isStarted: true,
        currentQuestion: 0,
        userAnswers: userAnswers.value,
        questionStatus: questionStatus.value,
        timeLeft: timeLeft.value,
      });
    };

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

      // Update store
      updateStore();
    };

    // Update status of current question based on answer
    const updateCurrentQuestionStatus = () => {
      const index = currentQuestionIndex.value;

      // Don't change if marked for review
      if (questionStatus.value[index] === "marked") {
        return;
      }

      if (userAnswers.value[index]) {
        questionStatus.value[index] = "answered";
      } else if (visitedQuestions.value.includes(index)) {
        questionStatus.value[index] = "not-answered";
      }
    };

    // Select an option for the current question
    const selectOption = (option) => {
      userAnswers.value[currentQuestionIndex.value] = option;
      updateStore();
    };

    // Clear response for current question
    const clearResponse = () => {
      userAnswers.value[currentQuestionIndex.value] = null;
      updateStore();
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
        updateStore();
      }
    };

    // Go to previous question
    const previousQuestion = () => {
      if (currentQuestionIndex.value > 0) {
        updateCurrentQuestionStatus();
        currentQuestionIndex.value--;
        questionStatus.value[currentQuestionIndex.value] = "current";
        updateStore();
      }
    };

    // Mark question for review
    const markForReview = () => {
      const index = currentQuestionIndex.value;
      questionStatus.value[index] =
        questionStatus.value[index] === "marked"
          ? userAnswers.value[index]
            ? "answered"
            : "not-answered"
          : "marked";
      updateStore();
    };

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

    // Update Vuex store with current state
    const updateStore = () => {
      store.commit("setQuizState", {
        quizId,
        isStarted: isQuizStarted.value,
        currentQuestion: currentQuestionIndex.value,
        userAnswers: userAnswers.value,
        questionStatus: questionStatus.value,
        timeLeft: timeLeft.value,
        timeTaken: timeTaken.value,
      });
    };

    // Confirm before submitting
    const confirmSubmit = () => {
      const unansweredCount = userAnswers.value.filter((a) => !a).length;

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
      clearInterval(timer);

      // Calculate score
      const score = userAnswers.value.reduce((total, answer, index) => {
        return (
          total + (answer === quizData.questions[index].correctAnswer ? 1 : 0)
        );
      }, 0);

      try {
        // Submit results to backend
        const response = await fetch(
          `http://127.0.0.1:5000/api/user/dashboard/quiz/${quizId}/submit`,
          {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
            },
            body: JSON.stringify({
              quizId,
              userId: userProfile.value?.id || "user123",
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
      store.commit("setQuizResults", {
        quizId,
        quizTitle: quizData.title,
        questions: quizData.questions,
        userAnswers: userAnswers.value,
        score: score,
        totalScore: quizData.questions.length,
        percentage: Math.round((score / quizData.questions.length) * 100),
        timeTaken: timeTaken.value,
      });

      // Clear quiz state
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
      }
    };

    // Lifecycle hooks
    onMounted(() => {
      fetchUserProfile();
      fetchQuizData();

      // Check if there's a saved state in the store
      const savedState = store.state.quiz?.quizState;
      if (savedState && savedState.quizId === quizId) {
        isQuizStarted.value = savedState.isStarted;
        currentQuestionIndex.value = savedState.currentQuestion;
        userAnswers.value = savedState.userAnswers;
        questionStatus.value = savedState.questionStatus;
        timeLeft.value = savedState.timeLeft;
        timeTaken.value = savedState.timeTaken || 0;

        // Restart timer if quiz was in progress
        if (isQuizStarted.value && timeLeft.value > 0) {
          timer = setInterval(() => {
            if (timeLeft.value > 0) {
              timeLeft.value--;
              timeTaken.value = quizData.duration * 60 - timeLeft.value;
            } else {
              clearInterval(timer);
              submitExam();
            }
          }, 1000);
        }
      }
    });

    onBeforeUnmount(() => {
      if (timer) {
        clearInterval(timer);
      }
    });

    return {
      isQuizStarted,
      quizData,
      userProfile,
      userAnswers,
      currentQuestionIndex,
      currentQuestion,
      questionStatus,
      formattedTime,
      timeLeft,
      getUserInitials,
      startQuiz,
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

.start-btn {
  display: block;
  width: 100%;
  padding: 1rem;
  font-size: 1.25rem;
  font-weight: bold;
  margin-top: 2rem;
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
