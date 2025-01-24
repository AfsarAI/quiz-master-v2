<template>
  <div class="user-progress container-fluid py-4">
    <h2 class="mb-4">Your Progress</h2>

    <div class="row g-4">
      <div class="col-md-6">
        <div class="card h-100">
          <div class="card-header bg-primary text-white">
            <h5 class="mb-0">Overall Progress</h5>
          </div>
          <div class="card-body">
            <canvas id="overallProgressChart"></canvas>
          </div>
        </div>
      </div>
      <div class="col-md-6">
        <div class="card h-100">
          <div class="card-header bg-success text-white">
            <h5 class="mb-0">Subject Mastery</h5>
          </div>
          <div class="card-body">
            <canvas id="subjectMasteryChart"></canvas>
          </div>
        </div>
      </div>
    </div>

    <div class="row mt-4">
      <div class="col-12">
        <div class="card">
          <div class="card-header bg-info text-white">
            <h5 class="mb-0">Recent Quiz Results</h5>
          </div>
          <div class="card-body">
            <div class="table-responsive">
              <table class="table table-hover">
                <thead>
                  <tr>
                    <th>Quiz Name</th>
                    <th>Subject</th>
                    <th>Date Taken</th>
                    <th>Score</th>
                    <th>Actions</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="quiz in recentQuizzes" :key="quiz.id">
                    <td>{{ quiz.name }}</td>
                    <td>{{ quiz.subject }}</td>
                    <td>{{ quiz.dateTaken }}</td>
                    <td>
                      <div class="progress" style="height: 20px">
                        <div
                          class="progress-bar"
                          role="progressbar"
                          :style="{ width: quiz.score + '%' }"
                          :aria-valuenow="quiz.score"
                          aria-valuemin="0"
                          aria-valuemax="100"
                        >
                          {{ quiz.score }}%
                        </div>
                      </div>
                    </td>
                    <td>
                      <button
                        class="btn btn-sm btn-outline-primary"
                        @click="reviewQuiz(quiz.id)"
                      >
                        Review
                      </button>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div class="row mt-4">
      <div class="col-md-6">
        <div class="card">
          <div class="card-header bg-warning text-white">
            <h5 class="mb-0">Study Time Distribution</h5>
          </div>
          <div class="card-body">
            <canvas id="studyTimeChart"></canvas>
          </div>
        </div>
      </div>
      <div class="col-md-6">
        <div class="card">
          <div class="card-header bg-secondary text-white">
            <h5 class="mb-0">Learning Streak</h5>
          </div>
          <div class="card-body">
            <div class="d-flex justify-content-between align-items-center">
              <h3 class="mb-0">{{ learningStreak }} days</h3>
              <i class="bi bi-fire text-danger" style="font-size: 2rem"></i>
            </div>
            <p class="text-muted mb-0">Keep up the great work!</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import Chart from "chart.js/auto";

const recentQuizzes = ref([
  {
    id: 1,
    name: "Math Quiz 101",
    subject: "Mathematics",
    dateTaken: "2023-05-01",
    score: 85,
  },
  {
    id: 2,
    name: "Science Trivia",
    subject: "Science",
    dateTaken: "2023-05-03",
    score: 92,
  },
  {
    id: 3,
    name: "History Challenge",
    subject: "History",
    dateTaken: "2023-05-05",
    score: 78,
  },
  {
    id: 4,
    name: "Literature Quiz",
    subject: "Literature",
    dateTaken: "2023-05-07",
    score: 88,
  },
  {
    id: 5,
    name: "Geography Explorer",
    subject: "Geography",
    dateTaken: "2023-05-09",
    score: 95,
  },
]);

const learningStreak = ref(7);

const reviewQuiz = (quizId) => {
  console.log(`Reviewing quiz with id: ${quizId}`);
  // Implement quiz review functionality
};

onMounted(() => {
  // Overall Progress Chart
  new Chart(document.getElementById("overallProgressChart"), {
    type: "line",
    data: {
      labels: ["Jan", "Feb", "Mar", "Apr", "May", "Jun"],
      datasets: [
        {
          label: "Average Score",
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
          text: "Your Progress Over Time",
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

  // Subject Mastery Chart
  new Chart(document.getElementById("subjectMasteryChart"), {
    type: "radar",
    data: {
      labels: ["Mathematics", "Science", "History", "Literature", "Geography"],
      datasets: [
        {
          label: "Your Mastery",
          data: [85, 92, 78, 88, 95],
          fill: true,
          backgroundColor: "rgba(54, 162, 235, 0.2)",
          borderColor: "rgb(54, 162, 235)",
          pointBackgroundColor: "rgb(54, 162, 235)",
          pointBorderColor: "#fff",
          pointHoverBackgroundColor: "#fff",
          pointHoverBorderColor: "rgb(54, 162, 235)",
        },
      ],
    },
    options: {
      responsive: true,
      plugins: {
        title: {
          display: true,
          text: "Subject Mastery",
        },
      },
      scales: {
        r: {
          angleLines: {
            display: false,
          },
          suggestedMin: 0,
          suggestedMax: 100,
        },
      },
    },
  });

  // Study Time Chart
  new Chart(document.getElementById("studyTimeChart"), {
    type: "doughnut",
    data: {
      labels: ["Mathematics", "Science", "History", "Literature", "Geography"],
      datasets: [
        {
          data: [30, 25, 20, 15, 10],
          backgroundColor: [
            "rgba(255, 99, 132, 0.8)",
            "rgba(54, 162, 235, 0.8)",
            "rgba(255, 206, 86, 0.8)",
            "rgba(75, 192, 192, 0.8)",
            "rgba(153, 102, 255, 0.8)",
          ],
        },
      ],
    },
    options: {
      responsive: true,
      plugins: {
        title: {
          display: true,
          text: "Study Time Distribution",
        },
      },
    },
  });
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
