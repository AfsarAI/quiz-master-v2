<template>
  <div class="card h-100 border-0 shadow-sm">
    <div class="card-body">
      <h5 class="card-title">Recommended Quizzes</h5>
      <ul class="list-group list-group-flush">
        <li
          v-for="quiz in quizzes"
          :key="quiz.id"
          class="list-group-item d-flex justify-content-between align-items-center"
        >
          {{ quiz.title }}
          <router-link
            :to="`/quizzes/${quiz.id}`"
            class="btn btn-primary btn-sm"
            >Start Quiz</router-link
          >
        </li>
      </ul>
    </div>
  </div>
</template>

<script>
export default {
  name: "RecommendedQuizzes",
  props: {
    quizzes: {
      type: Array,
      required: true,
    },
  },
};
</script>
