<template>
  <div class="home-page">
    <!-- Hero Section -->
    <div class="hero-section bg-primary text-white py-5">
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
            <img
              src="https://picsum.photos/500/300"
              alt="Quiz Illustration"
              class="img-fluid rounded shadow-lg"
            />
          </div>
        </div>
      </div>
    </div>

    <!-- Features Section -->
    <div class="features-section py-5">
      <div class="container">
        <h2 class="text-center mb-5">Why Choose Quiz Master?</h2>
        <div class="row g-4">
          <div class="col-md-4">
            <div class="card h-100 border-0 shadow-sm">
              <div class="card-body text-center">
                <i class="bi bi-book fs-1 text-primary mb-3"></i>
                <h3 class="card-title h4">Comprehensive Coverage</h3>
                <p class="card-text">
                  Access quizzes from various subjects and difficulty levels.
                </p>
              </div>
            </div>
          </div>
          <div class="col-md-4">
            <div class="card h-100 border-0 shadow-sm">
              <div class="card-body text-center">
                <i class="bi bi-graph-up fs-1 text-primary mb-3"></i>
                <h3 class="card-title h4">Track Your Progress</h3>
                <p class="card-text">
                  Monitor your performance and see your improvement over time.
                </p>
              </div>
            </div>
          </div>
          <div class="col-md-4">
            <div class="card h-100 border-0 shadow-sm">
              <div class="card-body text-center">
                <i class="bi bi-people fs-1 text-primary mb-3"></i>
                <h3 class="card-title h4">Community Learning</h3>
                <p class="card-text">
                  Engage with peers and compete on leaderboards.
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Popular Quizzes Section -->
    <div class="popular-quizzes-section py-5 bg-light">
      <div class="container">
        <h2 class="text-center mb-5">Popular Quizzes</h2>
        <div class="row g-4">
          <div class="col-md-4" v-for="quiz in popularQuizzes" :key="quiz.id">
            <div class="card h-100 border-0 shadow-sm">
              <img :src="quiz.image" class="card-img-top" :alt="quiz.title" />
              <div class="card-body">
                <h3 class="card-title h5">{{ quiz.title }}</h3>
                <p class="card-text">{{ quiz.description }}</p>
                <router-link
                  :to="'/quiz/' + quiz.id"
                  class="btn btn-outline-primary"
                  >Start Quiz</router-link
                >
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Qualification Section -->
    <div class="qualification-section py-5">
      <div class="container">
        <h2 class="text-center mb-5">Who Can Benefit?</h2>
        <div class="row g-4">
          <div
            class="col-md-3"
            v-for="level in educationLevels"
            :key="level.id"
          >
            <div class="card h-100 border-0 shadow-sm">
              <div class="card-body text-center">
                <i :class="level.icon + ' fs-1 text-primary mb-3'"></i>
                <h3 class="card-title h5">{{ level.title }}</h3>
                <p class="card-text">{{ level.description }}</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Call to Action Section -->
    <div class="cta-section py-5 bg-primary text-white text-center">
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
    </div>
  </div>
</template>

<script>
export default {
  name: "HomePage",
  data() {
    return {
      popularQuizzes: [
        {
          id: 1,
          title: "General Knowledge",
          description: "Test your knowledge on various topics.",
          image: "https://picsum.photos/300/200?random=1",
        },
        {
          id: 2,
          title: "Mathematics",
          description: "Challenge yourself with math problems.",
          image: "https://picsum.photos/300/200?random=2",
        },
        {
          id: 3,
          title: "Science",
          description: "Explore the wonders of science.",
          image: "https://picsum.photos/300/200?random=3",
        },
      ],
      educationLevels: [
        {
          id: 1,
          title: "School Students",
          description: "From elementary to high school",
          icon: "bi bi-mortarboard",
        },
        {
          id: 2,
          title: "College Students",
          description: "Undergraduate and postgraduate",
          icon: "bi bi-book",
        },
        {
          id: 3,
          title: "Professionals",
          description: "Skill enhancement and certifications",
          icon: "bi bi-briefcase",
        },
        {
          id: 4,
          title: "Lifelong Learners",
          description: "For curious minds of all ages",
          icon: "bi bi-lightbulb",
        },
      ],
    };
  },
};
</script>

<style scoped>
.home-page {
  font-family: "Arial", sans-serif;
}

.hero-section {
  background: linear-gradient(45deg, #007bff, #6610f2);
}

.card {
  transition: transform 0.3s ease-in-out;
}

.card:hover {
  transform: translateY(-5px);
}

.cta-section {
  background: linear-gradient(45deg, #6610f2, #007bff);
}
</style>
