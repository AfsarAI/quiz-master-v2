<template>
  <section class="hero-section section text-white py-5">
    <div class="container">
      <div class="row align-items-center">
        <div class="col-lg-6">
          <h1 class="display-4 fw-bold mb-4">Welcome to Quiz Master!</h1>
          <p class="lead mb-4">
            Your ultimate platform to practice mock quizzes and exams for any
            subject, at any level.
          </p>
          <div class="d-flex gap-3">
            <router-link to="/register" class="btn btn-light btn-lg"
              >Get Started</router-link
            >
            <router-link to="/about" class="btn btn-outline-light btn-lg"
              >Learn More</router-link
            >
          </div>
        </div>
        <div class="col-lg-6 d-none d-lg-block">
          <analog-clock></analog-clock>
        </div>
      </div>
    </div>
  </section>
</template>

<script>
import AnalogClock from "../AnalogClock.vue";

export default {
  name: "HeroSection",
  components: {
    AnalogClock,
  },
};
</script>

<style scoped>
.hero-section {
  background-size: cover;
  padding: 100px 0;
}
</style>
