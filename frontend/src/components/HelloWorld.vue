<template>
  <div class="container bg-light p-5 rounded shadow-lg mt-4 flex-grow-1">
    <div class="text-center">
      <h1 class="display-4 fw-bold text-primary">Welcome to Quiz Master!</h1>
      <p class="lead mt-3">
        Your ultimate platform to practice mock quizzes and exams for any
        subject. <i class="bi bi-alarm"></i>
      </p>
      <hr class="my-4" />
      <p>
        Whether you're preparing for competitive exams, enhancing your
        knowledge, or just testing your skills, Quiz Master provides a seamless
        and interactive learning experience.
      </p>
      <div class="mt-4">
        <router-link to="/register" class="btn btn-primary btn-lg me-2"
          >Get Started</router-link
        >
        <router-link to="/about" class="btn btn-outline-secondary btn-lg"
          >Learn More</router-link
        >
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "HelloWorld",
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped></style>
