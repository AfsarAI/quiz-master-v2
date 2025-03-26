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
                  <small class="text-muted">{{ quiz.subject }}</small>
                </div>
                <span class="badge bg-primary rounded-pill">{{
                  quiz.date
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
                  <i :class="subject.icon + ' me-2'"></i>
                  <span>{{ subject.title }}</span>
                </div>
                <span class="badge bg-success rounded-pill">{{
                  subject.date
                }}</span>
              </li>
            </ul>
            <p v-else class="text-muted">No subjects available at this time.</p>
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
</template>

<script setup>
import { ref, onMounted } from "vue";
import { useStore } from "vuex";
import Chart from "chart.js/auto";

const store = useStore();
const userId = ref(null);

if (!store.state.user?.id) {
  console.error("User ID not found. Please ensure the user is logged in.");
} else {
  userId.value = store.state.user.id;
}

// Reactive variables to store fetched data
const userStats = ref([]);
const upcomingQuizzes = ref([]);
const subjectList = ref([]);
const quizScores = ref([]);

// Generic function to fetch data using Fetch API
const fetchData = async (url, targetRef) => {
  try {
    const response = await fetch(url);
    if (!response.ok) {
      throw new Error(`HTTP error! Status: ${response.status}`);
    }
    const data = await response.json();
    if (data?.user_stats_data) {
      targetRef.value = data.user_stats_data;
    } else {
      console.error("Invalid data format:", data);
    }
  } catch (error) {
    console.error(`Error fetching data from ${url}:`, error);
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

// Fetch all data and render chart on component mount
onMounted(async () => {
  await Promise.all([
    fetchData(
      `http://localhost:5000/api/user/dashboard/${userId.value}/user-stats`,
      userStats
    ),
    fetchData(
      "http://localhost:5000/api/user/dashboard/upcoming-quizzes",
      upcomingQuizzes
    ),
    fetchData(
      `http://localhost:5000/api/user/dashboard/${userId.value}/subjects`,
      subjectList
    ),
    fetchData(
      `http://localhost:5000/api/user/dashboard/${userId.value}/quiz-scores`,
      quizScores
    ),
  ]);
  console.log("User Stats Data:", userStats.value);
  renderChart();
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
