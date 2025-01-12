<template>
  <section class="features-section section py-5">
    <div class="container">
      <h2 class="text-center mb-5">Why Choose Quiz Master?</h2>
      <div class="row g-4">
        <div class="col-md-4" v-for="(feature, index) in features" :key="index">
          <div class="card h-100 border-0 shadow-sm">
            <div class="card-body text-center">
              <i :class="feature.icon + ' fs-1 text-primary mb-3'"></i>
              <h3 class="card-title h4">{{ feature.title }}</h3>
              <p class="card-text">{{ feature.description }}</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script>
export default {
  name: "FeaturesSection",
  setup() {
    const features = [
      {
        icon: "bi bi-book",
        title: "Comprehensive Coverage",
        description:
          "Access quizzes from various subjects and difficulty levels.",
      },
      {
        icon: "bi bi-graph-up",
        title: "Track Your Progress",
        description:
          "Monitor your performance and see your improvement over time.",
      },
      {
        icon: "bi bi-people",
        title: "Community Learning",
        description: "Engage with peers and compete on leaderboards.",
      },
    ];

    return {
      features,
    };
  },
};
</script>

<style scoped>
h2 {
  color: #4361ee;
}

[data-bs-theme="light"] .card {
  padding: 20px;
  border-radius: 8px;
  background-color: #f4f4f4;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  text-align: center;
  transition: transform 0.3s ease, box-shadow 0.3s ease,
    background-color 0.3s ease, color 0.3s ease;
}
[data-bs-theme="light"] .card:hover {
  transform: scale(1.05); /* Slight zoom */
  box-shadow: 0 8px 15px rgba(0, 0, 0, 0.2); /* Shadow increase */
  background: linear-gradient(135deg, #3a0ca3, #4361ee, #4cc9f0);
  color: white; /* Text color change */
}

[data-bs-theme="dark"] .card {
  padding: 20px;
  border-radius: 8px;
  background-color: #34495e;
  color: #f1f1f1;
  box-shadow: 0 4px 6px rgb(255, 254, 254);
  text-align: center;
  transition: transform 0.3s ease, box-shadow 0.3s ease,
    background-color 0.3s ease, color 0.3s ease;
}
[data-bs-theme="dark"] .card:hover {
  transform: scale(1.05); /* Slight zoom */
  box-shadow: 0 8px 15px rgb(255, 254, 254); /* Shadow increase */
  background: linear-gradient(135deg, #1a0029, #2b0057, #3a0085);
  color: #f1f1f1;
}
</style>
