<template>
  <div :class="{ dark: isDarkMode }">
    <h1>User Quizzes</h1>
    <div v-if="loading">Loading...</div>
    <div v-else>
      <div v-if="quizzes.length === 0">No quizzes available</div>
      <ul v-else>
        <li v-for="quiz in quizzes" :key="quiz.id">{{ quiz.title }}</li>
      </ul>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from "vue";

export default {
  setup() {
    const quizzes = ref([]);
    const loading = ref(false);
    const isDarkMode = ref(false);

    const fetchAllQuizzes = async () => {
      loading.value = true;
      try {
        const response = await fetch("/api/quizzes/all");
        quizzes.value = await response.json();
      } catch (error) {
        console.error("Error fetching all quizzes:", error);
      } finally {
        loading.value = false;
      }
    };

    onMounted(() => {
      fetchAllQuizzes();
      isDarkMode.value =
        window.matchMedia &&
        window.matchMedia("(prefers-color-scheme: dark)").matches;
    });

    return {
      quizzes,
      loading,
      isDarkMode,
    };
  },
};
</script>

<style scoped>
.dark {
  background-color: #121212;
  color: #ffffff;
}

button {
  margin-right: 10px;
}

h1 {
  margin-bottom: 20px;
}

ul {
  list-style-type: none;
  padding: 0;
}

li {
  padding: 10px;
  border-bottom: 1px solid #ccc;
}

.dark li {
  border-bottom: 1px solid #444;
}
</style>
