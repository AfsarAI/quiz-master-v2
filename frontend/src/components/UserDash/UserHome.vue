<template>
  <div class="user-home container-fluid py-4">
    <h2 class="mb-4">User Home Page!</h2>

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
            <ul
              v-if="upcomingQuizzes.length"
              class="list-group list-group-flush"
            >
              <li
                v-for="quiz in upcomingQuizzes"
                :key="quiz.id"
                class="list-group-item d-flex justify-content-between align-items-center"
              >
                <div>
                  <h6 class="mb-0">{{ quiz.title }}</h6>
                  <small class="text-muted">{{ quiz.quiz_type }}</small>
                </div>
                <span class="badge bg-primary rounded-pill">{{
                  quiz.date_created
                }}</span>
              </li>
            </ul>
            <p v-else class="text-muted">No quizzes available at this time.</p>
          </div>
        </div>
      </div>

      <div class="col-md-6">
        <div class="card h-100">
          <div class="card-header bg-success text-white">
            <h5 class="mb-0">All Subjects</h5>
          </div>
          <div class="card-body">
            <ul v-if="subjectList.length" class="list-group list-group-flush">
              <li
                v-for="subject in subjectList"
                :key="subject.id"
                class="list-group-item d-flex justify-content-between align-items-center"
              >
                <div>
                  <!-- Constant book icon -->
                  <i class="bi bi-book me-2"></i>
                  <span>{{ subject.name }}</span>
                </div>

                <!-- Chapter count with badge -->
                <span class="badge bg-primary rounded-pill">
                  {{ subject.chapters.length }} Chapters
                </span>
              </li>
            </ul>
            <p v-else class="text-muted">No subjects available at this time.</p>
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
              <canvas
                v-if="quizScores.length"
                id="learningProgressChart"
              ></canvas>
              <p v-else class="text-muted">
                No data available for learning progress at this time.
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
<script setup>
import { ref, onMounted } from "vue";
import { useStore } from "vuex";
import Chart from "chart.js/auto";

const store = useStore();
const userId = store.state.user?.id;

if (!userId) {
  console.error("User ID not found. Please ensure the user is logged in.");
}

// Reactive variables to store fetched data
const userStats = ref([]);
const upcomingQuizzes = ref([]);
const subjectList = ref([]);
const quizScores = ref([]);

// Fetch User Stats
const fetchUserStats = async () => {
  try {
    const response = await fetch(
      `http://localhost:5000/api/user/dashboard/${userId}/user-stats`
    );
    if (!response.ok) throw new Error(`HTTP error! Status: ${response.status}`);
    const data = await response.json();
    userStats.value = data.user_stats_data || [];
  } catch (error) {
    console.error("Error fetching user stats:", error);
  }
};

// Fetch Upcoming Quizzes
const fetchUpcomingQuizzes = async () => {
  try {
    const response = await fetch(
      "http://localhost:5000/api/user/dashboard/upcoming-quizzes"
    );
    if (!response.ok) throw new Error(`HTTP error! Status: ${response.status}`);
    const data = await response.json();
    upcomingQuizzes.value = data || [];
  } catch (error) {
    console.error("Error fetching upcoming quizzes:", error);
  }
};

// Fetch Subjects
const fetchSubjects = async () => {
  try {
    const response = await fetch(
      `http://localhost:5000/api/user/dashboard/${userId}/subjects`
    );
    if (!response.ok) throw new Error(`HTTP error! Status: ${response.status}`);
    const data = await response.json();
    subjectList.value = data || [];
  } catch (error) {
    console.error("Error fetching subjects:", error);
  }
};

// Fetch Quiz Scores
const fetchQuizScores = async () => {
  try {
    const response = await fetch(
      `http://localhost:5000/api/user/dashboard/${userId}/quiz-scores`
    );
    if (!response.ok) throw new Error(`HTTP error! Status: ${response.status}`);
    const data = await response.json();
    quizScores.value = data || [];
    renderChart();
  } catch (error) {
    console.error("Error fetching quiz scores:", error);
  }
};

// Render Chart using fetched quiz scores
const renderChart = () => {
  if (!quizScores.value.length) {
    console.error("No data available for chart rendering.");
    return;
  }

  const ctx = document.getElementById("learningProgressChart");
  if (!ctx) {
    console.error("Chart element not found.");
    return;
  }

  new Chart(ctx, {
    type: "line",
    data: {
      labels: ["Jan", "Feb", "Mar", "Apr", "May", "Jun"],
      datasets: [
        {
          label: "Quiz Scores",
          data: quizScores.value,
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
};

onMounted(() => {
  fetchUserStats();
  fetchUpcomingQuizzes();
  fetchSubjects();
  fetchQuizScores();
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
