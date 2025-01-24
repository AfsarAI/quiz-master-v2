<template>
  <div class="layout">
    <app-navbar />
    <div class="about-page">
      <!-- About Section -->
      <section class="about-section">
        <h1>Welcome to Quiz Master</h1>
        <p>
          Quiz Master is your ultimate platform for organizing and participating
          in engaging quizzes. Whether you're a student, teacher, or quiz
          enthusiast, this platform is designed to make quizzing fun, efficient,
          and interactive. Our goal is to bring the joy of learning through
          quizzes to everyone!
        </p>
      </section>

      <!-- Features Section -->
      <section class="features-section">
        <h2>Why Choose Quiz Master?</h2>
        <ul>
          <li>🎯 Seamless quiz creation and management for admins</li>
          <li>📊 Real-time leaderboard for participants</li>
          <li>
            💡 Multiple quiz formats (MCQs, True/False, Fill in the blanks)
          </li>
          <li>🔐 Secure platform with advanced anti-cheating mechanisms</li>
          <li>📱 Responsive design for desktop and mobile users</li>
        </ul>
      </section>

      <!-- Admin Details Section -->
      <section class="admin-details-section">
        <h2>Admin Contact</h2>
        <div class="admin-card">
          <h3>Quiz Master Admin</h3>
          <p>Name: <strong>John Doe</strong></p>
          <p>Email: <strong>admin@quizmaster.com</strong></p>
          <p>Phone: <strong>+91 9876543210</strong></p>
          <p>Role: <strong>Quiz Creator & Organizer</strong></p>
        </div>
      </section>

      <!-- Contact Us Section -->
      <section class="contact-section">
        <h2>Contact Us</h2>
        <p>
          If you have any questions, feedback, or suggestions, feel free to
          reach out to us. We value your input and strive to make Quiz Master
          better for you.
        </p>
        <div class="contact-info">
          <p>Email: <strong>support@quizmaster.com</strong></p>
          <p>Phone: <strong>+91 1234567890</strong></p>
          <p>Address: <strong>123 Quiz Lane, Knowledge City, India</strong></p>
        </div>
      </section>
    </div>
    <app-footer />
  </div>
</template>

<script>
import AppNavbar from "@/components/Navbar.vue";
import AppFooter from "@/components/Footer.vue";

export default {
  components: {
    AppNavbar,
    AppFooter,
  },
};
</script>

<style scoped>
/* Layout Styles */
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

/* About Section Styles */
.about-section h1 {
  font-size: 2.5rem;
  margin-bottom: 10px;
  text-align: center;
  color: #4a4a4a;
}

.about-section p {
  font-size: 1.2rem;
  line-height: 1.8;
  text-align: center;
}

/* Features Section Styles */
.features-section {
  margin-top: 30px;
}

.features-section h2 {
  font-size: 2rem;
  margin-bottom: 15px;
  color: #333;
  text-align: center;
}

.features-section ul {
  list-style: none;
  padding: 0;
  font-size: 1.2rem;
  color: #333;
}

.features-section li {
  margin: 10px 0;
  padding-left: 25px;
  position: relative;
}

.features-section li:before {
  content: "✔️";
  position: absolute;
  left: 0;
  color: #4caf50;
}

/* Admin Section Styles */
.admin-details-section {
  margin-top: 30px;
  background: #ffffff;
  border-radius: 10px;
  padding: 20px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  text-align: center;
}

.admin-details-section h2 {
  font-size: 2rem;
  margin-bottom: 10px;
  color: #333;
}

.admin-card {
  background: #f7f9fc;
  padding: 20px;
  border-radius: 10px;
  border: 1px solid #ddd;
}

.admin-card h3 {
  font-size: 1.5rem;
  margin-bottom: 10px;
  color: #4a4a4a;
}

/* Contact Section Styles */
.contact-section {
  margin-top: 30px;
  background: #ffffff;
  padding: 20px;
  border-radius: 10px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.contact-section h2 {
  font-size: 2rem;
  margin-bottom: 10px;
  color: #333;
}

.contact-info p {
  font-size: 1.2rem;
  margin: 5px 0;
}
</style>
