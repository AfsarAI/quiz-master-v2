<template>
  <div class="user-progress container-fluid py-4">
    <h2 class="mb-4">Your Progress</h2>

    <div v-if="!isLoading">
      <!-- Learning Progress Chart - Full Width -->
      <div class="row mb-4">
        <div class="col-12">
          <div class="card">
            <div class="card-header bg-primary text-white">
              <h5 class="mb-0">Your Learning Progress</h5>
            </div>
            <div class="card-body">
              <canvas
                v-if="quizScores.length"
                ref="learningProgressChartRef"
                id="learningProgressChart"
              ></canvas>
              <p v-else class="text-muted">
                No data available for learning progress at this time.
              </p>
            </div>
          </div>
        </div>
      </div>

      <!-- Recent Quiz Results Table -->
      <div class="row mb-4">
        <div class="col-12">
          <div class="card">
            <div
              class="card-header bg-info text-white d-flex justify-content-between align-items-center"
            >
              <h5 class="mb-0">Recent Quiz Results</h5>
              <!-- Download Button with Icon and Text -->
              <button
                v-if="quizScores.length"
                type="button"
                class="btn btn-light btn-sm"
                @click="downloadCSV"
              >
                <i class="bi bi-download me-1"></i>
                Download
              </button>
            </div>
            <div class="card-body">
              <div class="table-responsive">
                <table class="table table-hover">
                  <thead>
                    <tr>
                      <th>Quiz Name</th>
                      <th>Date Taken</th>
                      <th>Score</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-for="score in quizScores" :key="score.id">
                      <td>{{ score.quiz_name }}</td>
                      <td>{{ score.attempt_date }}</td>
                      <td>
                        <div class="progress" style="height: 20px">
                          <div
                            class="progress-bar"
                            role="progressbar"
                            :style="{ width: score.percentage + '%' }"
                            :aria-valuenow="score.percentage"
                            aria-valuemin="0"
                            aria-valuemax="100"
                          >
                            {{ score.percentage.toFixed(1) }}%
                          </div>
                        </div>
                      </td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Quiz Performance by Subject (Pie Chart) -->
      <div class="row">
        <div class="col-12">
          <div class="card">
            <div class="card-header bg-warning text-white">
              <h5 class="mb-0">Quiz Performance by Quiz</h5>
            </div>
            <div class="card-body">
              <canvas
                v-if="quizScores.length"
                ref="quizPerformanceChartRef"
                id="quizPerformanceChart"
              ></canvas>
              <p v-else class="text-muted">
                No data available for quiz performance at this time.
              </p>
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
import { ref, onMounted, nextTick, watch } from "vue";
import { useStore } from "vuex";
import Chart from "chart.js/auto";

const store = useStore();
const userId = store.state.user?.id;

if (!userId) {
  console.error("User ID not found. Please ensure the user is logged in.");
}

// Reactive variables to store fetched data
const quizScores = ref([]);
const isLoading = ref(false);
let learningProgressChart = null;
let quizPerformanceChart = null;

// Refs for chart elements
const learningProgressChartRef = ref(null);
const quizPerformanceChartRef = ref(null);

// Fetch Quiz Scores
const fetchQuizScores = async () => {
  isLoading.value = true;
  try {
    const response = await fetch(
      `http://localhost:5000/api/user/dashboard/${userId}/quiz-scores`,
      {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
          "Authentication-Token": store.state.user?.token,
        },
      }
    );
    if (!response.ok) throw new Error(`HTTP error! Status: ${response.status}`);
    const data = await response.json();
    quizScores.value = data || [];
  } catch (error) {
    console.error("Error fetching quiz scores:", error);
  } finally {
    isLoading.value = false;
  }
};

// Download CSV function - enhanced with toasts
const downloadCSV = async () => {
  try {
    if (!userId) {
      console.error("User ID not found.");
      store.dispatch("addToast", {
        message: "User ID not found.",
        type: "error",
      });
      return;
    }

    // Step 1: Trigger CSV Generation
    const response = await fetch(
      `http://localhost:5000/api/user/dashboard/task/csv-export/${userId}`,
      {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
          "Authentication-Token": store.state.user?.token,
        },
      }
    );
    if (!response.ok) {
      throw new Error("Failed to trigger CSV generation.");
    }

    const { task_id } = await response.json();
    console.log("CSV generation started. Task ID:", task_id);
    store.dispatch("addToast", {
      message: "CSV generation started. Processing, please wait...",
      type: "info",
    });

    // Step 2: Polling to Check Task Status
    let isCompleted = false;
    while (!isCompleted) {
      const statusResponse = await fetch(
        `http://localhost:5000/api/user/dashboard/task/csv-download/${task_id}`,
        {
          method: "GET",
          headers: {
            "Content-Type": "application/json",
            "Authentication-Token": store.state.user?.token,
          },
        }
      );

      if (statusResponse.status === 202) {
        console.log("CSV still processing...");
        await new Promise((resolve) => setTimeout(resolve, 5000)); // 5-second delay
      } else if (statusResponse.status === 200) {
        window.location.href = `http://localhost:5000/api/user/dashboard/task/csv-download/${task_id}`;
        store.dispatch("addToast", {
          message: "CSV download successful!",
          type: "success",
        });
        isCompleted = true;
      } else {
        const statusData = await statusResponse.json();
        console.error("Unexpected error during CSV download:", statusData);
      }
    }
  } catch (error) {
    console.error("Error during CSV download process:", error);
    store.dispatch("addToast", {
      message: "An error occurred. Please try again.",
      type: "error",
    });
  }
};

// Watch for changes in quizScores and render charts when data is available
watch(
  quizScores,
  async (newScores) => {
    if (newScores.length > 0) {
      // Wait for DOM to update
      await nextTick();
      // Render charts with a small delay to ensure DOM is ready
      setTimeout(() => {
        renderLearningProgressChart();
        renderQuizPerformanceChart();
      }, 100);
    }
  },
  { deep: true }
);

// Render Learning Progress Chart
const renderLearningProgressChart = () => {
  if (!quizScores.value.length) {
    console.error("No data available for chart rendering.");
    return;
  }

  const canvas = document.getElementById("learningProgressChart");
  if (!canvas) {
    console.error("Learning progress chart element not found.");
    return;
  }

  // Get the 2D context from the canvas
  const ctx = canvas.getContext("2d");
  if (!ctx) {
    console.error("Could not get 2D context from canvas.");
    return;
  }

  // Destroy existing chart if it exists
  if (learningProgressChart) {
    learningProgressChart.destroy();
  }

  const dataLabels = quizScores.value.map((_, index) => `Attempt ${index + 1}`);
  const scoreData = quizScores.value.map((score) => score.percentage || 0);

  learningProgressChart = new Chart(ctx, {
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
              const quizName = score.quiz_name || `Quiz ID: ${score.quiz_id}`;
              return `${quizName} - ${score.percentage.toFixed(1)}%`;
            },
          },
        },
      },
      scales: {
        y: {
          beginAtZero: true,
          max: 100,
          title: {
            display: true,
            text: "Score (%)",
          },
        },
        x: {
          title: {
            display: true,
            text: "Quiz Attempts",
          },
        },
      },
    },
  });
};

// Render Quiz Performance Chart (Pie Chart)
const renderQuizPerformanceChart = () => {
  if (!quizScores.value.length) {
    console.error("No data available for quiz performance chart rendering.");
    return;
  }

  const canvas = document.getElementById("quizPerformanceChart");
  if (!canvas) {
    console.error("Quiz performance chart element not found.");
    return;
  }

  // Get the 2D context from the canvas
  const ctx = canvas.getContext("2d");
  if (!ctx) {
    console.error("Could not get 2D context from canvas.");
    return;
  }

  // Destroy existing chart if it exists
  if (quizPerformanceChart) {
    quizPerformanceChart.destroy();
  }

  // Group scores by quiz_id and calculate average score for each quiz
  const quizMap = new Map();

  quizScores.value.forEach((score) => {
    if (!quizMap.has(score.quiz_id)) {
      quizMap.set(score.quiz_id, {
        quiz_name: score.quiz_name,
        scores: [],
        total: 0,
        count: 0,
      });
    }

    const quizData = quizMap.get(score.quiz_id);
    quizData.scores.push(score.percentage);
    quizData.total += score.percentage;
    quizData.count += 1;
  });

  // Calculate averages and prepare chart data
  const quizNames = [];
  const averageScores = [];
  const backgroundColors = [
    "rgba(255, 99, 132, 0.8)",
    "rgba(54, 162, 235, 0.8)",
    "rgba(255, 206, 86, 0.8)",
    "rgba(75, 192, 192, 0.8)",
    "rgba(153, 102, 255, 0.8)",
    "rgba(255, 159, 64, 0.8)",
    "rgba(199, 199, 199, 0.8)",
    "rgba(83, 102, 255, 0.8)",
    "rgba(78, 205, 196, 0.8)",
    "rgba(255, 99, 71, 0.8)",
  ];

  quizMap.forEach((data) => {
    quizNames.push(data.quiz_name);
    averageScores.push((data.total / data.count).toFixed(1));
  });

  quizPerformanceChart = new Chart(ctx, {
    type: "pie",
    data: {
      labels: quizNames,
      datasets: [
        {
          data: averageScores,
          backgroundColor: backgroundColors.slice(0, quizNames.length),
          borderWidth: 1,
        },
      ],
    },
    options: {
      responsive: true,
      plugins: {
        title: {
          display: true,
          text: "Average Score by Quiz (%)",
        },
        tooltip: {
          callbacks: {
            label: (context) => {
              const label = context.label || "";
              const value = context.raw || 0;
              return `${label}: ${value}%`;
            },
          },
        },
        legend: {
          position: "right",
        },
      },
    },
  });
};

onMounted(async () => {
  await fetchQuizScores();
});
</script>

<style scoped>
.user-progress {
  max-width: 1200px;
  margin: 0 auto;
}

.card {
  border: none;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
  margin-bottom: 20px;
}

.card:hover {
  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15);
}

.progress {
  height: 20px;
  background-color: #e9ecef;
}

.progress-bar {
  background-color: #007bff;
}

.spinner-border {
  width: 3rem;
  height: 3rem;
}

[data-bs-theme="dark"] .card {
  background-color: #2c3e50;
  color: #ecf0f1;
}

[data-bs-theme="dark"] .card-header {
  background-color: #34495e;
}

[data-bs-theme="dark"] .table {
  color: #ecf0f1;
}

[data-bs-theme="dark"] .table-hover tbody tr:hover {
  background-color: #34495e;
}

[data-bs-theme="dark"] .progress {
  background-color: #4a6278;
}

[data-bs-theme="dark"] .text-muted {
  color: #bdc3c7 !important;
}
</style>
