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
