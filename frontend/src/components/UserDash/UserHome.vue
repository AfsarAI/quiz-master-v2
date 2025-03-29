<template>
  <div class="user-home container-fluid py-4">
    <h2 class="mb-4">User Home Page!</h2>
    <div v-if="!isLoading">
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
              <h5 class="mb-0">Recently Added Top 3 Quizzes</h5>
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
              <p v-else class="text-muted">
                No quizzes available at this time.
              </p>
            </div>
          </div>
        </div>

        <div class="col-md-6">
          <div class="card h-100">
            <div
              class="card-header bg-success text-white d-flex justify-content-between align-items-center"
            >
              <h5 class="mb-0">All Given Quizzes</h5>

              <!-- Download Button with Tooltip -->
              <button
                v-if="quizScores.length"
                type="button"
                class="btn btn-light btn-sm"
                @click="downloadCSV"
                data-bs-toggle="tooltip"
                data-bs-placement="right"
                title="Download ALL Data in CSV"
              >
                <i class="bi bi-download"></i>
              </button>
            </div>

            <div class="card-body">
              <ul v-if="quizScores.length" class="list-group list-group-flush">
                <li
                  v-for="score in quizScores"
                  :key="score.id"
                  class="list-group-item d-flex justify-content-between align-items-center"
                >
                  <div>
                    <i class="bi bi-book me-2"></i>
                    <span>{{ score.quiz_name }}</span>
                  </div>
                  <span class="badge bg-primary rounded-pill">
                    {{ score.score }} Points
                  </span>
                </li>
              </ul>
              <p v-else class="text-muted">No Quizzes given yet!</p>
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
    <div v-else>
      <div class="position-absolute top-50 start-50 translate-middle">
        <div class="spinner-border text-primary" role="status">
          <span class="visually-hidden">Loading...</span>
        </div>
      </div>
    </div>
  </div>
</template>
<script setup>
import { ref, onMounted, nextTick } from "vue";
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
const quizScores = ref([]);
const isLoading = ref(false);

// Fetch User Stats
const fetchUserStats = async () => {
  isLoading.value = true;
  try {
    const response = await fetch(
      `http://localhost:5000/api/user/dashboard/${userId}/user-stats`
    );
    if (!response.ok) throw new Error(`HTTP error! Status: ${response.status}`);
    const data = await response.json();
    userStats.value = data.user_stats_data || [];
  } catch (error) {
    console.error("Error fetching user stats:", error);
  } finally {
    isLoading.value = false;
  }
};

// Fetch Upcoming Quizzes
const fetchUpcomingQuizzes = async () => {
  isLoading.value = true;
  try {
    const response = await fetch(
      "http://localhost:5000/api/user/dashboard/upcoming-quizzes"
    );
    if (!response.ok) throw new Error(`HTTP error! Status: ${response.status}`);
    const data = await response.json();
    upcomingQuizzes.value = data || [];
  } catch (error) {
    console.error("Error fetching upcoming quizzes:", error);
  } finally {
    isLoading.value = false;
  }
};

// Fetch Quiz Scores
const fetchQuizScores = async () => {
  isLoading.value = true;
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
  } finally {
    isLoading.value = false;
  }
};

const downloadCSV = async () => {
  try {
    if (!userId) {
      console.error("User ID not found.");
      return;
    }

    // Step 1: Trigger CSV Generation
    const response = await fetch(
      `http://localhost:5000/api/user/dashboard/task/csv-export/${userId}`
    );
    if (!response.ok) {
      throw new Error("Failed to trigger CSV generation.");
    }

    const { task_id } = await response.json();
    console.log("CSV generation started. Task ID:", task_id);

    // Step 2: Polling to Check Task Status
    let isCompleted = false;
    while (!isCompleted) {
      const statusResponse = await fetch(
        `http://localhost:5000/api/user/dashboard/task/csv-download/${task_id}`
      );

      if (statusResponse.ok) {
        // Task completed, download the file
        window.location.href = `http://localhost:5000/api/user/dashboard/task/csv-download/${task_id}`;
        isCompleted = true;
      } else if (statusResponse.status === 404) {
        console.log(
          "CSV still processing... Waiting 3 seconds before retrying."
        );
        await new Promise((resolve) => setTimeout(resolve, 3000)); // 3-second delay
      } else {
        throw new Error("Error checking CSV generation status.");
      }
    }
  } catch (error) {
    console.error("Error during CSV download process:", error);
    alert("An error occurred. Please try again.");
  }
};

// Render Chart using fetched quiz scores
let chartInstance = null; // Chart instance ko track karne ke liye

// ✅ Render Chart using quizScores
const renderChart = async () => {
  if (!quizScores.value.length) {
    console.error("No data available for chart rendering.");
    return;
  }

  await nextTick(); // Ensure DOM is updated before accessing canvas

  const ctx = document.getElementById("learningProgressChart");
  if (!ctx) {
    console.error("Chart element not found.");
    return;
  }

  if (chartInstance) {
    chartInstance.destroy();
  }

  const dataLabels = quizScores.value.map((_, index) => `Attempt ${index + 1}`);
  const scoreData = quizScores.value.map((score) => score.percentage || 0);

  chartInstance = new Chart(ctx, {
    type: "line",
    data: {
      labels: dataLabels,
      datasets: [
        {
          label: "Quiz Scores (%)",
          data: scoreData,
          borderColor: "rgb(75, 192, 192)",
          backgroundColor: "rgba(75, 192, 192, 0.2)",
          fill: true,
          tension: 0.2,
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
        tooltip: {
          callbacks: {
            label: (context) => {
              const index = context.dataIndex;
              const score = quizScores.value[index];
              const quizName = score.quiz_name || `Quiz ID: ${score.id}`;
              return `${quizName} - ${score.percentage}%`;
            },
          },
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
  fetchQuizScores();
});
</script>

<style scoped>
.spinner-border {
  width: 3rem;
  height: 3rem;
}

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
