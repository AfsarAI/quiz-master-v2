<template>
  <div class="admin-overview container-fluid py-4">
    <h2 class="mb-4">Dashboard Overview</h2>

    <div v-if="!loading">
      <!-- Stats Section -->
      <div class="row g-4 mb-4">
        <div v-for="stat in stats" :key="stat.title" class="col-md-3 col-sm-6">
          <div class="card h-100">
            <div class="card-body">
              <h5 class="card-title">{{ stat.title }}</h5>
              <p class="card-text display-4">{{ stat.value }}</p>
              <p class="card-text text-muted">
                <span
                  :class="stat.trend === 'up' ? 'text-success' : 'text-danger'"
                >
                  <i
                    :class="
                      stat.trend === 'up'
                        ? 'bi bi-arrow-up'
                        : 'bi bi-arrow-down'
                    "
                  ></i>
                  {{ stat.change }}%
                </span>
                since last week
              </p>
            </div>
          </div>
        </div>
      </div>

      <!-- Recent Activity & Top Quizzes -->
      <div class="row g-4">
        <!-- Recent Activity Section -->
        <div class="col-md-6">
          <div class="card h-100">
            <div class="card-header bg-primary text-white">
              <h5 class="mb-0">Recent Activity</h5>
            </div>
            <div class="card-body">
              <ul
                v-if="recentActivity.length > 0"
                class="list-group list-group-flush"
              >
                <li
                  v-for="activity in recentActivity"
                  :key="activity.id"
                  class="list-group-item"
                >
                  <div class="d-flex w-100 justify-content-between">
                    <h6 class="mb-1">{{ activity.action }}</h6>
                    <small>{{ activity.timestamp }}</small>
                  </div>
                  <p class="mb-1">{{ activity.details }}</p>
                  <small>{{ activity.user }}</small>
                </li>
              </ul>
              <p v-else class="text-center text-muted">
                No activity this week.
              </p>
            </div>
          </div>
        </div>

        <!-- Top Performing Quizzes Section -->
        <div class="col-md-6">
          <div class="card h-100">
            <div class="card-header bg-success text-white">
              <h5 class="mb-0">Top Performing Quizzes</h5>
            </div>
            <div class="card-body">
              <p v-if="topScorers.length === 0" class="text-center text-muted">
                No quizzes taken yet.
              </p>
              <table v-else class="table table-hover">
                <thead>
                  <tr>
                    <th>User Name</th>
                    <th>Quiz Name</th>
                    <th>Score</th>
                    <th>Attempt Date</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="scorer in topScorers" :key="scorer.user_id">
                    <td>{{ scorer.user }}</td>
                    <td>{{ scorer.quiz_name }}</td>
                    <td>{{ scorer.score }}%</td>
                    <td>{{ scorer.attempt_date }}</td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </div>

      <!-- User Engagement Chart -->
      <!-- Score Distribution Chart -->
      <div class="row mt-4">
        <div class="col-md-6">
          <div class="card">
            <div class="card-header bg-warning text-white">
              <h5 class="mb-0">Score Distribution</h5>
            </div>
            <div class="card-body">
              <canvas id="scoreDistributionChart"></canvas>
            </div>
          </div>
        </div>

        <!-- Quiz Participation Chart -->
        <div class="col-md-6">
          <div class="card">
            <div class="card-header bg-info text-white">
              <h5 class="mb-0">Quiz Participation Overview</h5>
            </div>
            <div class="card-body">
              <canvas id="quizParticipationChart"></canvas>
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
// Import dependencies
import { ref, onMounted } from "vue";
import { useStore } from "vuex";
import Chart from "chart.js/auto";

const store = useStore();

// Reactive variables for dynamic data
const stats = ref([]);
const recentActivity = ref([]);
const topScorers = ref([]);
const loading = ref(false);

// Fetch Stats with Trend Calculation
const fetchStats = async () => {
  try {
    loading.value = true;
    const response = await fetch(
      "http://127.0.0.1:5000/api/admin/dashboard/stats",
      {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
          "Authentication-Token": store.state.user?.token,
        },
      }
    );
    const data = await response.json();

    // Calculate trends dynamically based on last week's data
    stats.value = data.stats.map((stat) => {
      const change = ((stat.current - stat.previous) / stat.previous) * 100;
      return {
        ...stat,
        trend: change > 0 ? "up" : "down",
        change: Math.abs(change.toFixed(2)),
      };
    });
  } catch (error) {
    console.error("Error fetching stats:", error);
  } finally {
    loading.value = false;
  }
};

// Fetch Recent Activity
const fetchRecentActivity = async () => {
  try {
    loading.value = true;
    const response = await fetch(
      "http://127.0.0.1:5000/api/admin/dashboard/recent-activity/data",
      {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
          "Authentication-Token": store.state.user?.token,
        },
      }
    );
    const data = await response.json();
    // Check if activities exist, otherwise set an empty array
    recentActivity.value = data || [];
  } catch (error) {
    console.error("Error fetching recent activity:", error);
  } finally {
    loading.value = false;
  }
};

// Fetch Top Performing Quizzes
const fetchTopScorers = async () => {
  try {
    loading.value = true;
    const response = await fetch(
      "http://127.0.0.1:5000/api/admin/dashboard/top-scorers",
      {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
          "Authentication-Token": store.state.user?.token,
        },
      }
    );
    const data = await response.json();
    topScorers.value = data || [];
  } catch (error) {
    console.error("Error fetching top quizzes:", error);
  } finally {
    loading.value = false;
  }
};

// Initialize User Engagement Charts
const initUserEngagementCharts = async () => {
  try {
    loading.value = true;
    const response = await fetch(
      "http://127.0.0.1:5000/api/admin/dashboard/user-engagement",
      {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
          "Authentication-Token": store.state.user?.token,
        },
      }
    );
    const engagementData = await response.json();

    // Histogram for Score Distribution
    const ctx1 = document.getElementById("scoreDistributionChart");
    new Chart(ctx1, {
      type: "bar",
      data: {
        labels: engagementData.scoreRanges,
        datasets: [
          {
            label: "Users in Score Range",
            data: engagementData.scoreCounts,
            backgroundColor: "rgba(75, 192, 192, 0.6)",
            borderColor: "rgba(75, 192, 192, 1)",
            borderWidth: 1,
          },
        ],
      },
      options: {
        responsive: true,
        plugins: {
          title: {
            display: true,
            text: "Score Distribution of Users",
          },
        },
        scales: {
          y: { beginAtZero: true },
        },
      },
    });

    // Pie Chart for Quiz Participation
    const ctx2 = document.getElementById("quizParticipationChart");
    new Chart(ctx2, {
      type: "pie",
      data: {
        labels: ["1-5 Quizzes", "6-10 Quizzes", "11-20 Quizzes", "21+ Quizzes"],
        datasets: [
          {
            label: "Users by Quiz Participation",
            data: engagementData.quizParticipation,
            backgroundColor: [
              "rgba(255, 99, 132, 0.6)",
              "rgba(54, 162, 235, 0.6)",
              "rgba(255, 206, 86, 0.6)",
              "rgba(75, 192, 192, 0.6)",
            ],
            borderWidth: 1,
          },
        ],
      },
      options: {
        responsive: true,
        plugins: {
          title: {
            display: true,
            text: "Quiz Participation Overview",
          },
        },
      },
    });
  } catch (error) {
    console.error("Error initializing charts:", error);
  } finally {
    loading.value = false;
  }
};

// Fetch all data and initialize components on mount
onMounted(() => {
  fetchStats();
  fetchRecentActivity();
  fetchTopScorers();
  initUserEngagementCharts();
});
</script>

<style scoped>
.spinner-border {
  width: 3rem;
  height: 3rem;
}

.admin-overview {
  max-width: 1200px;
  margin: 0 auto;
}

.card {
  transition: all 0.3s ease;
}

.card:hover {
  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15);
}

[data-bs-theme="dark"] .card,
[data-bs-theme="dark"] .list-group-item {
  background-color: #2c3e50;
  color: #ecf0f1;
}

[data-bs-theme="dark"] .card-header {
  border-bottom: 1px solid #4a6278;
}

[data-bs-theme="dark"] .table {
  color: #ecf0f1;
}

[data-bs-theme="dark"] .table-hover tbody tr:hover {
  background-color: #34495e;
}

[data-bs-theme="dark"] .text-muted {
  color: #bdc3c7 !important;
}
</style>
