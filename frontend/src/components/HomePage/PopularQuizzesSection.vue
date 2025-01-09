<template>
  <section class="popular-quizzes-section section py-5 bg-light">
    <div class="container">
      <h2 class="text-center mb-5">Popular Quizzes</h2>
      <div class="row g-4">
        <div class="col-md-4" v-for="quiz in popularQuizzes" :key="quiz.id">
          <div class="card h-100 border-0 shadow-sm">
            <img :src="quiz.image" class="card-img-top" :alt="quiz.title" />
            <div class="card-body">
              <h3 class="card-title h5">{{ quiz.title }}</h3>
              <p class="card-text">{{ quiz.description }}</p>
              <router-link
                :to="'/quiz/' + quiz.id"
                class="btn btn-outline-primary"
                >Start Quiz</router-link
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
  setup() {
    const popularQuizzes = [
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
    ];

    return {
      popularQuizzes,
    };
  },
};
</script>
