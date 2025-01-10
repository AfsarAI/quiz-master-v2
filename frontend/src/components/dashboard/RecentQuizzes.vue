<template>
  <div class="card h-100 border-0 shadow-sm">
    <div class="card-body">
      <h5 class="card-title">Recent Quizzes</h5>
      <ul class="list-group list-group-flush">
        <li
          v-for="quiz in quizzes"
          :key="quiz.id"
          class="list-group-item d-flex justify-content-between align-items-center"
        >
          {{ quiz.title }}
          <span
            :class="[
              'badge',
              quiz.score >= 70 ? 'bg-success' : 'bg-warning',
              'rounded-pill',
            ]"
          >
            {{ quiz.score }}%
          </span>
        </li>
      </ul>
    </div>
  </div>
</template>

<script>
export default {
  name: "RecentQuizzes",
  props: {
    quizzes: {
      type: Array,
      required: true,
    },
  },
};
</script>
