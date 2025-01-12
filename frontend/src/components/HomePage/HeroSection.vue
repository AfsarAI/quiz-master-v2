<template>
  <section class="hero-section section text-white py-5">
    <div class="container">
      <div class="row align-items-center">
        <div class="col-lg-6 hero-content" :class="{ animate: animate }">
          <h1 class="display-4 fw-bold mb-4">Welcome to Quiz Master!</h1>
          <p class="lead mb-4 typewriter" ref="typewriter"></p>
          <div class="d-flex gap-3">
            <router-link to="/register" class="btn btn-primary btn-lg">
              Get Started
            </router-link>
            <router-link to="/about" class="btn btn-secondary btn-lg">
              Learn More
            </router-link>
          </div>
        </div>
        <div class="col-lg-6 d-none d-lg-block">
          <div class="clock-container">
            <analog-clock></analog-clock>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script>
import { ref, onMounted, nextTick } from "vue";
import AnalogClock from "../AnalogClock.vue";

export default {
  name: "HeroSection",
  components: {
    AnalogClock,
  },
  setup() {
    const animate = ref(false);
    const typewriter = ref(null);

    onMounted(() => {
      setTimeout(() => {
        animate.value = true;
      }, 100);

      nextTick(() => {
        startTypewriter();
      });
    });

    const startTypewriter = () => {
      const text =
        "Your ultimate platform to practice mock quizzes and exams for any subject, at any level.";
      let i = 0;
      const typingSpeed = 50; // Typing speed in milliseconds
      const pauseDuration = 3000; // Pause duration in milliseconds

      function typeWriter() {
        if (typewriter.value && i < text.length) {
          typewriter.value.textContent += text.charAt(i);
          i++;
          setTimeout(typeWriter, typingSpeed);
        } else if (typewriter.value && i >= text.length) {
          // Remove the cursor when typing is complete
          typewriter.value.classList.remove("typing");

          // Reset and restart after pause
          setTimeout(() => {
            i = 0;
            if (typewriter.value) {
              typewriter.value.textContent = "";
              typewriter.value.classList.add("typing");
              typeWriter();
            }
          }, pauseDuration);
        }
      }

      if (typewriter.value) {
        typewriter.value.classList.add("typing");
        typeWriter();
      }
    };

    return { animate, typewriter };
  },
};
</script>

<style scoped>
.hero-section {
  background: linear-gradient(135deg, #3a0ca3, #4361ee, #8e44ad);
  min-height: 100vh;
  display: flex;
  align-items: center;
  position: relative;
  overflow: hidden;
}

[data-bs-theme="dark"] .hero-section {
  background: #34495e;
}

.hero-section::before {
  content: "";
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: url('data:image/svg+xml;charset=utf8,%3Csvg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1440 320"%3E%3Cpath fill="%23ffffff" fill-opacity="0.05" d="M0,96L48,112C96,128,192,160,288,186.7C384,213,480,235,576,213.3C672,192,768,128,864,128C960,128,1056,192,1152,208C1248,224,1344,192,1392,176L1440,160L1440,320L1392,320C1344,320,1248,320,1152,320C1056,320,960,320,864,320C768,320,672,320,576,320C480,320,384,320,288,320C192,320,96,320,48,320L0,320Z"%3E%3C/path%3E%3C/svg%3E')
    no-repeat bottom;
  background-size: cover;
}

.container {
  position: relative;
  z-index: 2;
}

.hero-content {
  padding-top: 50px;
  padding-right: 30px;
}

h1 {
  color: #ffffff;
  font-size: 3.5rem;
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.1);
}

.lead {
  font-size: 1.25rem;
  max-width: 600px;
}

.typewriter {
  position: relative;
  overflow: hidden;
  white-space: pre-wrap;
  word-break: break-word;
  margin: 0;
  letter-spacing: 0.05em;
  display: inline-block;
}

.typewriter.typing::after {
  content: "";
  position: absolute;
  right: -4px;
  animation: blink 0.7s step-end infinite;
}

@keyframes blink {
  from,
  to {
    opacity: 0;
  }
  50% {
    opacity: 1;
  }
}

.btn {
  padding: 12px 24px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 1px;
  transition: all 0.3s ease;
  border: none;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  border-radius: 30px;
}

.btn-primary {
  background-color: #f72585;
  color: #ffffff;
}

.btn-primary:hover {
  background-color: #b5179e;
  transform: translateY(-2px);
  box-shadow: 0 6px 8px rgba(0, 0, 0, 0.15);
}

.btn-secondary {
  background-color: #4cc9f0;
  color: #ffffff;
}

.btn-secondary:hover {
  background-color: #4361ee;
  transform: translateY(-2px);
  box-shadow: 0 6px 8px rgba(0, 0, 0, 0.15);
}

.clock-container {
  position: relative;
  width: 300px;
  height: 300px;
  margin: 0 auto;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 50%;
  padding: 20px;
  box-shadow: 0 0 5px rgba(255, 255, 255, 0.05);
}

.hero-content {
  opacity: 0;
  transform: translateY(20px);
  transition: all 1s ease;
}

.hero-content.animate {
  opacity: 1;
  transform: translateY(0);
}

@media (max-width: 991px) {
  .hero-section {
    text-align: center;
  }

  .lead {
    margin-left: auto;
    margin-right: auto;
  }

  .d-flex {
    justify-content: center;
  }

  .hero-content {
    padding-top: 0;
    padding-right: 0;
  }
}
</style>
