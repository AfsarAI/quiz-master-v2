<template>
  <div>
    <AppNavbar />
    <div class="home-page">
      <HeroSection />

      <AnimatedSection>
        <FeaturesSection />
      </AnimatedSection>

      <AnimatedSection>
        <PopularQuizzesSection />
      </AnimatedSection>

      <AnimatedSection>
        <QualificationSection />
      </AnimatedSection>

      <AnimatedSection>
        <CtaSection />
      </AnimatedSection>
    </div>
    <Footer />
  </div>
</template>

<script setup>
import AppNavbar from "@/components/Navbar.vue";
import AnimatedSection from "@/components/AnimatedSection.vue";
import HeroSection from "@/components/HomePage/HeroSection.vue";
import FeaturesSection from "@/components/HomePage/FeaturesSection.vue";
import PopularQuizzesSection from "@/components/HomePage/PopularQuizzesSection.vue";
import QualificationSection from "@/components/HomePage/QualificationSection.vue";
import CtaSection from "@/components/HomePage/CtaSection.vue";
import Footer from "@/components/Footer.vue";
</script>

<style scoped>
@import "@/styles/animations.css";

.home-page {
  font-family: "Arial", sans-serif;
  margin: 0;
  padding: 0;
  color: #212529;
}
</style>
