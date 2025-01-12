<template>
  <section class="cta-section section py-5 text-white text-center">
    <div class="container border rounded">
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
.container {
  padding: 40px;
  background: linear-gradient(135deg, #3a0ca3, #4361ee, #4cc9f0);
}

[data-bs-theme="dark"] .container {
  background: linear-gradient(135deg, #1a0029, #2b0057, #3a0085);
}
</style>
