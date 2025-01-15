<template>
  <div class="quiz-interface">
    <div class="quiz-header">
      <h2>{{ quiz.title }}</h2>
      <div class="quiz-info">
        <span>
          <i class="bi bi-clock"></i> Time Remaining:
          {{ formatTime(timeRemaining) }}
        </span>
        <span>
          <i class="bi bi-list-ol"></i> Question
          {{ currentQuestionIndex + 1 }} of {{ quiz.questions.length }}
        </span>
      </div>
    </div>
    <div class="quiz-content">
      <div class="question-card">
        <h3>{{ currentQuestion.text }}</h3>
        <div class="options">
          <div
            v-for="(option, index) in currentQuestion.options"
            :key="index"
            class="option"
          >
            <input
              type="radio"
              :id="'option' + index"
              :name="'question' + currentQuestionIndex"
              :value="index"
              v-model="selectedAnswer"
            />
            <label :for="'option' + index">{{ option }}</label>
          </div>
        </div>
      </div>
    </div>
    <div class="quiz-footer">
      <button
        @click="previousQuestion"
        :disabled="currentQuestionIndex === 0"
        class="btn btn-secondary"
      >
        Previous
      </button>
      <button
        @click="nextQuestion"
        v-if="currentQuestionIndex < quiz.questions.length - 1"
        class="btn btn-primary"
      >
        Next
      </button>
      <button @click="submitQuiz" v-else class="btn btn-success">
        Submit Quiz
      </button>
    </div>
    <div class="quiz-progress">
      <div
        v-for="(question, index) in quiz.questions"
        :key="index"
        class="progress-indicator"
        :class="{
          current: index === currentQuestionIndex,
          answered: answeredQuestions[index] !== undefined,
        }"
        @click="goToQuestion(index)"
      >
        {{ index + 1 }}
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted, onUnmounted } from "vue";

export default {
  name: "QuizInterface",
  props: {
    quizId: {
      type: String,
      required: true,
    },
  },
  setup(props) {
    const quiz = ref({
      id: props.quizId,
      title: "Sample Quiz",
      questions: [
        {
          text: "What is the capital of France?",
          options: ["London", "Berlin", "Paris", "Madrid"],
          correctAnswer: 2,
        },
        {
          text: "Which planet is known as the Red Planet?",
          options: ["Venus", "Mars", "Jupiter", "Saturn"],
          correctAnswer: 1,
        },
        {
          text: "Who painted the Mona Lisa?",
          options: [
            "Vincent van Gogh",
            "Pablo Picasso",
            "Leonardo da Vinci",
            "Michelangelo",
          ],
          correctAnswer: 2,
        },
      ],
      duration: 600, // 10 minutes in seconds
    });

    const currentQuestionIndex = ref(0);
    const selectedAnswer = ref(null);
    const answeredQuestions = ref({});
    const timeRemaining = ref(quiz.value.duration);

    const currentQuestion = computed(
      () => quiz.value.questions[currentQuestionIndex.value]
    );

    const formatTime = (seconds) => {
      const minutes = Math.floor(seconds / 60);
      const remainingSeconds = seconds % 60;
      return `${minutes}:${remainingSeconds.toString().padStart(2, "0")}`;
    };

    const previousQuestion = () => {
      if (currentQuestionIndex.value > 0) {
        currentQuestionIndex.value--;
        selectedAnswer.value =
          answeredQuestions.value[currentQuestionIndex.value];
      }
    };

    const nextQuestion = () => {
      answeredQuestions.value[currentQuestionIndex.value] =
        selectedAnswer.value;
      if (currentQuestionIndex.value < quiz.value.questions.length - 1) {
        currentQuestionIndex.value++;
        selectedAnswer.value =
          answeredQuestions.value[currentQuestionIndex.value] || null;
      }
    };

    const goToQuestion = (index) => {
      answeredQuestions.value[currentQuestionIndex.value] =
        selectedAnswer.value;
      currentQuestionIndex.value = index;
      selectedAnswer.value = answeredQuestions.value[index] || null;
    };

    const submitQuiz = () => {
      answeredQuestions.value[currentQuestionIndex.value] =
        selectedAnswer.value;
      let score = 0;
      quiz.value.questions.forEach((question, index) => {
        if (answeredQuestions.value[index] === question.correctAnswer) {
          score++;
        }
      });
      alert(
        `Quiz submitted! Your score is ${score} out of ${quiz.value.questions.length}.`
      );
      console.log("Quiz results:", answeredQuestions.value);
    };

    let timer;
    onMounted(() => {
      timer = setInterval(() => {
        if (timeRemaining.value > 0) {
          timeRemaining.value--;
        } else {
          clearInterval(timer);
          submitQuiz();
        }
      }, 1000);
    });

    onUnmounted(() => {
      clearInterval(timer);
    });

    return {
      quiz,
      currentQuestionIndex,
      currentQuestion,
      selectedAnswer,
      answeredQuestions,
      timeRemaining,
      formatTime,
      previousQuestion,
      nextQuestion,
      goToQuestion,
      submitQuiz,
    };
  },
};
</script>

<style scoped>
.quiz-interface {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
}

.quiz-header {
  text-align: center;
  margin-bottom: 20px;
}

.quiz-info {
  display: flex;
  justify-content: space-between;
  margin-top: 10px;
}

.question-card {
  background-color: #f8f9fa;
  border-radius: 8px;
  padding: 20px;
  margin-bottom: 20px;
}

.options {
  display: flex;
  flex-direction: column;
}

.option {
  margin: 10px 0;
}

.quiz-footer {
  display: flex;
  justify-content: space-between;
  margin-top: 20px;
}

.quiz-progress {
  display: flex;
  justify-content: center;
  margin-top: 20px;
}

.progress-indicator {
  width: 30px;
  height: 30px;
  border-radius: 50%;
  background-color: #e9ecef;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 5px;
  cursor: pointer;
}

.progress-indicator.current {
  background-color: #007bff;
  color: white;
}

.progress-indicator.answered {
  background-color: #28a745;
  color: white;
}
</style>
