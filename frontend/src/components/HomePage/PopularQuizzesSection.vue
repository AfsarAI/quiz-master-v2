<template>
  <section class="popular-quizzes-section py-5">
    <div class="container">
      <h2 class="text-center mb-5">Popular Quizzes</h2>
      <div class="row">
        <div class="col-md-4" v-for="quiz in popularQuizzes" :key="quiz.id">
          <div class="card mb-4">
            <img :src="quiz.image" class="card-img-top" :alt="quiz.title" />
            <div class="card-body">
              <h5 class="card-title">{{ quiz.title }}</h5>
              <p class="card-text">{{ quiz.description }}</p>
              <a :href="'/quiz/' + quiz.id" class="btn btn-primary"
                >Start Quiz</a
              >
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script>
export default {
  name: "PopularQuizzesSection",
  data() {
    return {
      popularQuizzes: [
        {
          id: 1,
          title: "General Knowledge",
          description: "Test your knowledge on various topics.",
          image: "https://picsum.photos/300/200?random=1",
        },
        {
          id: 2,
          title: "Mathematics",
          description: "Challenge yourself with math problems.",
          image: "https://picsum.photos/300/200?random=2",
        },
        {
          id: 3,
          title: "Science",
          description: "Explore the wonders of science.",
          image: "https://picsum.photos/300/200?random=3",
        },
      ],
    };
  },
};
</script>

<style scoped>
h2 {
  color: #4361ee;
}

.btn-primary {
  background-color: #4361ee;
  border-color: #4361ee;
}

.btn-primary:hover {
  background-color: #3a0ca3;
  border-color: #3a0ca3;
}
</style>
