<template>
  <div class="admin-overview container-fluid py-4">
    <h2 class="mb-4">Dashboard Overview</h2>

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
                    stat.trend === 'up' ? 'bi bi-arrow-up' : 'bi bi-arrow-down'
                  "
                ></i>
                {{ stat.change }}%
              </span>
              since last week
            </p>
          </div>
        </div>
      </div>

      <!-- Recent Activity Section -->
      <div class="row g-4">
        <div class="col-md-6">
          <div class="card h-100">
            <div class="card-header bg-primary text-white">
              <h5 class="mb-0">Recent Activity</h5>
            </div>
            <div class="card-body">
              <ul
                v-if="recentActivity && recentActivity.length > 0"
                class="list-group list-group-flush"
              >
                <li
                  v-for="activity in recentActivity"
                  :key="activity.id"
                  class="list-group-item"
                >
                  <div class="d-flex w-100 justify-content-between">
                    <h6 class="mb-1">{{ activity.action }}</h6>
                    <small>{{ activity.time }}</small>
                  </div>
                  <p class="mb-1">{{ activity.details }}</p>
                  <small>{{ activity.user }}</small>
                </li>
              </ul>
              <p v-else class="text-center">No activity this week.</p>
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
              <table class="table table-hover">
                <thead>
                  <tr>
                    <th>Quiz Title</th>
                    <th>Category</th>
                    <th>Avg. Score</th>
                    <th>Attempts</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="quiz in topQuizzes" :key="quiz.id">
                    <td>{{ quiz.title }}</td>
                    <td>{{ quiz.category }}</td>
                    <td>{{ quiz.avgScore }}%</td>
                    <td>{{ quiz.attempts }}</td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </div>

      <!-- User Engagement Chart -->
      <div class="row mt-4">
        <div class="col-12">
          <div class="card">
            <div class="card-header bg-info text-white">
              <h5 class="mb-0">User Engagement</h5>
            </div>
            <div class="card-body">
              <canvas id="userEngagementChart"></canvas>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
// Import dependencies
import { ref, onMounted } from "vue";
import Chart from "chart.js/auto";

// Reactive variables for dynamic data
const stats = ref([]);
const recentActivity = ref([]);
const topQuizzes = ref([]);

// Fetch Stats with Trend Calculation
const fetchStats = async () => {
  try {
    const response = await fetch("http://127.0.0.1:5000/api/dashboard/stats");
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
  }
};

// Fetch Recent Activity
const fetchRecentActivity = async () => {
  try {
    const response = await fetch(
      "http://127.0.0.1:5000/api/dashboard/get/recent-activity/data"
    );
    const data = await response.json();
    // Check if activities exist, otherwise set an empty array
    recentActivity.value = data.activities || [];
  } catch (error) {
    console.error("Error fetching recent activity:", error);
  }
};

// Fetch Top Performing Quizzes
const fetchTopQuizzes = async () => {
  try {
    const response = await fetch(
      "http://127.0.0.1:5000/api/dashboard/top-quizzes"
    );
    const data = await response.json();
    topQuizzes.value = data.quizzes;
  } catch (error) {
    console.error("Error fetching top quizzes:", error);
  }
};

// Initialize User Engagement Chart
const initUserEngagementChart = async () => {
  try {
    const response = await fetch(
      "http://127.0.0.1:5000/api/dashboard/user-engagement"
    );
    const engagementData = await response.json();

    const ctx = document.getElementById("userEngagementChart");
    new Chart(ctx, {
      type: "line",
      data: {
        labels: engagementData.labels,
        datasets: [
          {
            label: "Active Users",
            data: engagementData.activeUsers,
            borderColor: "rgb(75, 192, 192)",
            tension: 0.1,
          },
          {
            label: "Quizzes Taken",
            data: engagementData.quizzesTaken,
            borderColor: "rgb(255, 99, 132)",
            tension: 0.1,
          },
        ],
      },
      options: {
        responsive: true,
        plugins: {
          title: {
            display: true,
            text: "User Engagement Over Time",
          },
        },
        scales: {
          y: { beginAtZero: true },
        },
      },
    });
  } catch (error) {
    console.error("Error initializing user engagement chart:", error);
  }
};

// Fetch all data and initialize components on mount
onMounted(() => {
  fetchStats();
  fetchRecentActivity();
  fetchTopQuizzes();
  initUserEngagementChart();
});
</script>

<style scoped>
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
