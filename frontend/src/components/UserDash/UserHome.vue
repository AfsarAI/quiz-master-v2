<template>
  <div class="user-home container-fluid py-4">
    <h2 class="mb-4">Welcome, {{ user.fullname }}!</h2>

    <div class="row g-4 mb-4">
      <div
        class="col-md-3 col-sm-6"
        v-for="(stat, index) in userStats"
        :key="index"
      >
        <div class="card stat-card h-100">
          <div class="card-body">
            <h5 class="card-title">{{ stat.title }}</h5>
            <p class="card-text display-4">{{ stat.value }}</p>
            <div class="stat-icon">
              <i :class="stat.icon"></i>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div class="row g-4">
      <div class="col-md-6">
        <div class="card h-100">
          <div class="card-header bg-primary text-white">
            <h5 class="mb-0">Upcoming Quizzes</h5>
          </div>
          <div class="card-body">
            <ul class="list-group list-group-flush">
              <li
                v-for="quiz in upcomingQuizzes"
                :key="quiz.id"
                class="list-group-item d-flex justify-content-between align-items-center"
              >
                <div>
                  <h6 class="mb-0">{{ quiz.title }}</h6>
                  <small class="text-muted">{{ quiz.subject }}</small>
                </div>
                <span class="badge bg-primary rounded-pill">{{
                  quiz.date
                }}</span>
              </li>
            </ul>
          </div>
        </div>
      </div>
      <div class="col-md-6">
        <div class="card h-100">
          <div class="card-header bg-success text-white">
            <h5 class="mb-0">Recent Achievements</h5>
          </div>
          <div class="card-body">
            <ul class="list-group list-group-flush">
              <li
                v-for="achievement in recentAchievements"
                :key="achievement.id"
                class="list-group-item d-flex justify-content-between align-items-center"
              >
                <div>
                  <i :class="achievement.icon + ' me-2'"></i>
                  <span>{{ achievement.title }}</span>
                </div>
                <span class="badge bg-success rounded-pill">{{
                  achievement.date
                }}</span>
              </li>
            </ul>
          </div>
        </div>
      </div>
    </div>

    <div class="row mt-4">
      <div class="col-12">
        <div class="card">
          <div class="card-header bg-info text-white">
            <h5 class="mb-0">Your Learning Progress</h5>
          </div>
          <div class="card-body">
            <canvas id="learningProgressChart"></canvas>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import Chart from "chart.js/auto";

const user = ref({
  fullname: "John Doe",
  // Add other user details as needed
});

const userStats = ref([
  { title: "Quizzes Taken", value: 25, icon: "bi bi-journal-check" },
  { title: "Average Score", value: "85%", icon: "bi bi-graph-up" },
  { title: "Study Streak", value: 7, icon: "bi bi-calendar-check" },
  { title: "Achievements", value: 12, icon: "bi bi-trophy" },
]);

const upcomingQuizzes = ref([
  {
    id: 1,
    title: "Advanced Mathematics",
    subject: "Mathematics",
    date: "Tomorrow",
  },
  { id: 2, title: "World History", subject: "History", date: "In 2 days" },
  {
    id: 3,
    title: "Physics Fundamentals",
    subject: "Science",
    date: "Next week",
  },
]);

const recentAchievements = ref([
  { id: 1, title: "Quiz Master", icon: "bi bi-star-fill", date: "Today" },
  {
    id: 2,
    title: "Fast Learner",
    icon: "bi bi-lightning-charge-fill",
    date: "2 days ago",
  },
  {
    id: 3,
    title: "Consistent Performer",
    icon: "bi bi-graph-up-arrow",
    date: "1 week ago",
  },
]);

onMounted(() => {
  new Chart(document.getElementById("learningProgressChart"), {
    type: "line",
    data: {
      labels: ["Jan", "Feb", "Mar", "Apr", "May", "Jun"],
      datasets: [
        {
          label: "Quiz Scores",
          data: [65, 70, 75, 80, 85, 90],
          borderColor: "rgb(75, 192, 192)",
          tension: 0.1,
        },
      ],
    },
    options: {
      responsive: true,
      plugins: {
        title: {
          display: true,
          text: "Your Quiz Score Progress",
        },
      },
      scales: {
        y: {
          beginAtZero: true,
          max: 100,
        },
      },
    },
  });
});
</script>

<style scoped>
.user-home {
  max-width: 1200px;
  margin: 0 auto;
}

.stat-card {
  position: relative;
  overflow: hidden;
  transition: all 0.3s ease;
}

.stat-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
}

.stat-icon {
  position: absolute;
  top: 1rem;
  right: 1rem;
  font-size: 2.5rem;
  opacity: 0.2;
}

.card {
  border: none;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
}

.card:hover {
  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15);
}

.display-4 {
  font-size: 2.5rem;
  font-weight: bold;
  color: var(--bs-primary);
}

[data-bs-theme="dark"] .card {
  background-color: #2c3e50;
  color: #ecf0f1;
}

[data-bs-theme="dark"] .card-header {
  background-color: #34495e;
}

[data-bs-theme="dark"] .list-group-item {
  background-color: #2c3e50;
  color: #ecf0f1;
  border-color: #34495e;
}

[data-bs-theme="dark"] .text-muted {
  color: #bdc3c7 !important;
}
</style>
