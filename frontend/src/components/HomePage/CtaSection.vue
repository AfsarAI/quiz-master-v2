<template>
  <section class="cta-section section py-5 text-white text-center">
    <div class="container">
      <h2 class="mb-4">Ready to Test Your Knowledge?</h2>
      <p class="lead mb-4">
        Join thousands of learners and start your journey with Quiz Master
        today!
      </p>
      <router-link to="/register" class="btn btn-light btn-lg"
        >Sign Up Now</router-link
      >
    </div>
  </section>
</template>

<script>
export default {
  name: "CtaSection",
};
</script>

<style scoped>
.cta-section {
  background: linear-gradient(135deg, #3498db, #8e44ad);
}
</style>
