<template>
  <div class="layout" :class="{ 'dark-mode': isDarkMode }">
    <app-navbar />
    <div class="about-page">
      <section class="about-section">
        <h1>Welcome to Quiz Master</h1>
        <p>
          Quiz Master is your go-to platform for creating, managing, and
          participating in engaging quizzes. Our aim is to enhance learning
          through fun and interactive quizzes.
        </p>
      </section>

      <section class="features-section">
        <h2>Why Choose Quiz Master?</h2>
        <ul>
          <li>🎯 Create and manage quizzes effortlessly</li>
          <li>📊 Real-time leaderboard and scoring</li>
          <li>💡 Multiple quiz formats available</li>
          <li>📱 Responsive and user-friendly design</li>
        </ul>
      </section>
    </div>
    <app-footer />
  </div>
</template>

<script>
import AppNavbar from "@/components/Navbar.vue";
import AppFooter from "@/components/Footer.vue";
import { useStore } from "vuex";
import { computed } from "vue";

export default {
  components: { AppNavbar, AppFooter },
  setup() {
    const store = useStore();
    const isDarkMode = computed(() => store.state.isDarkMode);
    return { isDarkMode };
  },
};
</script>

<style scoped>
.layout {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

.about-page {
  flex: 1;
  padding: 20px;
  background: linear-gradient(to right, #ffafbd, #ffc3a0);
  color: #333;
  font-family: "Arial", sans-serif;
}

.dark-mode .about-page {
  background: linear-gradient(to right, #2c3e50, #4ca1af);
  color: #ecf0f1;
}

/* About Section Styles */
.about-section h1 {
  font-size: 2.5rem;
  margin-bottom: 20px;
  text-align: center;
}

.about-section p {
  font-size: 1.2rem;
  line-height: 1.8;
  text-align: center;
}

/* Features Section Styles */
.features-section {
  margin-top: 40px;
}

.features-section h2 {
  font-size: 2rem;
  margin-bottom: 15px;
  text-align: center;
}

.features-section ul {
  list-style: none;
  padding: 0;
}

.features-section li {
  font-size: 1.2rem;
  margin-bottom: 10px;
  padding-left: 25px;
  position: relative;
}

.features-section li:before {
  content: "✔️";
  position: absolute;
  left: 0;
  color: #4caf50;
}

.dark-mode .features-section li:before {
  color: #27ae60;
}
</style>
