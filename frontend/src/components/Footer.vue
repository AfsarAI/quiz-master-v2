<template>
  <footer class="text-center text-lg-start">
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
            <li><a href="#" class="footer-link">General Knowledge</a></li>
            <li><a href="#" class="footer-link">Science</a></li>
            <li><a href="#" class="footer-link">Mathematics</a></li>
            <li><a href="#" class="footer-link">History</a></li>
          </ul>
        </div>

        <!-- Column 3 -->
        <div class="col-lg-3 col-md-6 mb-4 mb-lg-0">
          <h5 class="text-uppercase">Contact</h5>
          <ul class="list-unstyled">
            <li>
              <a href="mailto:contact@quizmaster.com" class="footer-link"
                >contact@quizmaster.com</a
              >
            </li>
            <li>
              <a href="tel:+1234567890" class="footer-link">+123 456 7890</a>
            </li>
            <li>
              <a href="#" class="footer-link"
                >123 Quiz Street, Knowledge City</a
              >
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
              <a href="#" class="footer-link me-3"
                ><i class="fab fa-facebook fa-2x"></i
              ></a>
            </li>
            <li>
              <a href="#" class="footer-link me-3"
                ><i class="fab fa-twitter fa-2x"></i
              ></a>
            </li>
            <li>
              <a href="#" class="footer-link me-3"
                ><i class="fab fa-instagram fa-2x"></i
              ></a>
            </li>
            <li>
              <a href="#" class="footer-link me-3"
                ><i class="fab fa-linkedin fa-2x"></i
              ></a>
            </li>
          </ul>
        </div>
      </div>
    </div>

    <!-- Footer Bottom -->
    <div class="text-center p-3">
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
  background: light;
  margin-top: auto;
}

footer h5 {
  font-weight: bold;
}

.footer-link {
  color: black;
  text-decoration: none;
  transition: color 0.3s ease;
}

.footer-link:hover {
  color: #f72585;
  text-decoration: underline;
}

[data-bs-theme="dark"] footer {
  background: dark;
}

[data-bs-theme="dark"] .footer-link {
  color: rgba(255, 255, 255, 0.8) !important;
  /* color: black; */
  text-decoration: none;
  transition: color 0.3s ease;
}
[data-bs-theme="dark"] .footer-link:hover {
  color: #4cc9f0 !important;
}
</style>
