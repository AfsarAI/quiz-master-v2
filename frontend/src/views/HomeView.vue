<template>
  <div class="home-page">
    <HeroSection />
    <FeaturesSection />

    <animated-section>
      <PopularQuizzesSection />
    </animated-section>

    <animated-section>
      <QualificationSection />
    </animated-section>

    <animated-section>
      <CtaSection />
    </animated-section>
  </div>
</template>

<script setup>
import AnimatedSection from "@/components/AnimatedSection.vue";
import HeroSection from "@/components/HomePage/HeroSection.vue";
import FeaturesSection from "@/components/HomePage/FeaturesSection.vue";
import PopularQuizzesSection from "@/components/HomePage/PopularQuizzesSection.vue";
import QualificationSection from "@/components/HomePage/QualificationSection.vue";
import CtaSection from "@/components/HomePage/CtaSection.vue";
</script>

<style scoped>
@import "@/styles/animations.css";

.home-page {
  font-family: "Arial", sans-serif;
  margin: 0;
  padding: 0;
}

/* Remove the background gradient from here */
/* Individual sections will handle their own backgrounds */
</style>
