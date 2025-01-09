<template>
  <footer
    :class="[
      'text-white',
      'text-center',
      'text-lg-start',
      { 'bg-dark': isDarkMode, 'bg-primary': !isDarkMode },
    ]"
  >
    <div class="container p-4">
      <div class="row">
        <!-- Column 1 -->
        <div class="col-lg-3 col-md-6 mb-4 mb-lg-0">
          <h5 class="text-uppercase">About Quiz Master</h5>
          <p>
            We are dedicated to providing high-quality quizzes and learning
            experiences for students of all levels.
          </p>
        </div>

        <!-- Column 2 -->
        <div class="col-lg-3 col-md-6 mb-4 mb-lg-0">
          <h5 class="text-uppercase">Quiz Categories</h5>
          <ul class="list-unstyled">
            <li><a href="#" class="text-white">General Knowledge</a></li>
            <li><a href="#" class="text-white">Science</a></li>
            <li><a href="#" class="text-white">Mathematics</a></li>
            <li><a href="#" class="text-white">History</a></li>
          </ul>
        </div>

        <!-- Column 3 -->
        <div class="col-lg-3 col-md-6 mb-4 mb-lg-0">
          <h5 class="text-uppercase">Contact</h5>
          <ul class="list-unstyled">
            <li>
              <a href="mailto:contact@quizmaster.com" class="text-white"
                >contact@quizmaster.com</a
              >
            </li>
            <li>
              <a href="tel:+1234567890" class="text-white">+123 456 7890</a>
            </li>
            <li>
              <a href="#" class="text-white">123 Quiz Street, Knowledge City</a>
            </li>
          </ul>
        </div>

        <!-- Column 4 -->
        <div class="col-lg-3 col-md-6 mb-4 mb-lg-0">
          <h5 class="text-uppercase">Follow Us</h5>
          <ul
            class="list-unstyled d-flex justify-content-center justify-content-lg-start"
          >
            <li>
              <a href="#" class="text-white me-3"
                ><i class="fab fa-facebook fa-2x"></i
              ></a>
            </li>
            <li>
              <a href="#" class="text-white me-3"
                ><i class="fab fa-twitter fa-2x"></i
              ></a>
            </li>
            <li>
              <a href="#" class="text-white me-3"
                ><i class="fab fa-instagram fa-2x"></i
              ></a>
            </li>
            <li>
              <a href="#" class="text-white me-3"
                ><i class="fab fa-linkedin fa-2x"></i
              ></a>
            </li>
          </ul>
        </div>
      </div>
    </div>

    <!-- Footer Bottom -->
    <div
      :class="[
        'text-center p-3',
        { 'bg-dark': isDarkMode, 'bg-primary': !isDarkMode },
      ]"
    >
      <p class="m-0">© {{ currentYear }} Quiz Master. All Rights Reserved.</p>
    </div>
  </footer>
</template>

<script>
import { computed } from "vue";
import { useStore } from "vuex";

export default {
  name: "AppFooter",
  setup() {
    const store = useStore();
    const isDarkMode = computed(() => store.state.isDarkMode);
    const currentYear = new Date().getFullYear();

    return {
      isDarkMode,
      currentYear,
    };
  },
};
</script>

<style scoped>
footer {
  margin-top: auto;
}

footer a:hover {
  text-decoration: underline;
}

.dark-mode footer {
  background-color: #2c3e50 !important;
}

.dark-mode footer a:hover {
  color: #5dade2 !important;
}
</style>
