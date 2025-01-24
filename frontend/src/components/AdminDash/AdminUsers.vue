<template>
  <div class="admin-users container-fluid py-4">
    <h2 class="mb-4">Manage Users</h2>

    <div class="row mb-4">
      <div class="col-md-6">
        <input
          v-model="searchQuery"
          type="text"
          class="form-control"
          placeholder="Search users..."
        />
      </div>
      <div class="col-md-6">
        <select v-model="roleFilter" class="form-select">
          <option value="">All Roles</option>
          <option value="student">Student</option>
          <option value="teacher">Teacher</option>
          <option value="admin">Admin</option>
        </select>
      </div>
    </div>

    <div class="row row-cols-1 row-cols-md-2 row-cols-lg-3 g-4">
      <div v-for="user in filteredUsers" :key="user.id" class="col">
        <div class="card h-100">
          <div class="card-body">
            <div class="d-flex justify-content-between align-items-center mb-3">
              <h5 class="card-title mb-0">{{ user.name }}</h5>
              <span :class="getRoleBadgeClass(user.role)">{{ user.role }}</span>
            </div>
            <p class="card-text">
              <i class="bi bi-envelope me-2"></i>{{ user.email }}
            </p>
            <p class="card-text">
              <i class="bi bi-calendar-event me-2"></i>Joined:
              {{ user.joinDate }}
            </p>
            <p class="card-text">
              <i class="bi bi-trophy me-2"></i>Quizzes Taken:
              {{ user.quizzesTaken }}
            </p>
          </div>
          <div class="card-footer">
            <button class="btn btn-primary me-2" @click="viewUserDetails(user)">
              <i class="bi bi-eye me-1"></i>View Details
            </button>
            <button class="btn btn-outline-danger" @click="deleteUser(user)">
              <i class="bi bi-trash me-1"></i>Delete
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- User Details Modal -->
    <div
      class="modal fade"
      id="userDetailsModal"
      tabindex="-1"
      aria-labelledby="userDetailsModalLabel"
      aria-hidden="true"
    >
      <div class="modal-dialog modal-lg">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title" id="userDetailsModalLabel">User Details</h5>
            <button
              type="button"
              class="btn-close"
              data-bs-dismiss="modal"
              aria-label="Close"
            ></button>
          </div>
          <div class="modal-body" v-if="selectedUser">
            <div class="row">
              <div class="col-md-6">
                <h6>Personal Information</h6>
                <p><strong>Name:</strong> {{ selectedUser.name }}</p>
                <p><strong>Email:</strong> {{ selectedUser.email }}</p>
                <p><strong>Role:</strong> {{ selectedUser.role }}</p>
                <p><strong>Join Date:</strong> {{ selectedUser.joinDate }}</p>
              </div>
              <div class="col-md-6">
                <h6>Quiz Statistics</h6>
                <p>
                  <strong>Quizzes Taken:</strong>
                  {{ selectedUser.quizzesTaken }}
                </p>
                <p>
                  <strong>Average Score:</strong>
                  {{ selectedUser.averageScore }}%
                </p>
                <p>
                  <strong>Highest Score:</strong>
                  {{ selectedUser.highestScore }}%
                </p>
              </div>
            </div>
            <div class="mt-4">
              <h6>Recent Activity</h6>
              <ul class="list-group">
                <li
                  v-for="(activity, index) in selectedUser.recentActivity"
                  :key="index"
                  class="list-group-item"
                >
                  <strong>{{ activity.date }}:</strong> {{ activity.action }}
                </li>
              </ul>
            </div>
          </div>
          <div class="modal-footer">
            <button
              type="button"
              class="btn btn-secondary"
              data-bs-dismiss="modal"
            >
              Close
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from "vue";
import { Modal } from "bootstrap";

const users = ref([
  {
    id: 1,
    name: "John Doe",
    email: "john@example.com",
    role: "student",
    joinDate: "2023-01-15",
    quizzesTaken: 25,
    averageScore: 85,
    highestScore: 98,
    recentActivity: [
      { date: "2023-05-10", action: "Completed Math Quiz" },
      { date: "2023-05-08", action: "Started Science Course" },
      { date: "2023-05-05", action: "Achieved new high score in History Quiz" },
    ],
  },
  {
    id: 2,
    name: "Jane Smith",
    email: "jane@example.com",
    role: "teacher",
    joinDate: "2022-11-30",
    quizzesTaken: 15,
    averageScore: 92,
    highestScore: 100,
    recentActivity: [
      { date: "2023-05-09", action: "Created new Science Quiz" },
      { date: "2023-05-07", action: "Graded Math assignments" },
      { date: "2023-05-04", action: "Updated Literature course material" },
    ],
  },
  {
    id: 3,
    name: "Bob Johnson",
    email: "bob@example.com",
    role: "admin",
    joinDate: "2022-09-01",
    quizzesTaken: 5,
    averageScore: 88,
    highestScore: 95,
    recentActivity: [
      { date: "2023-05-10", action: "Added new user accounts" },
      { date: "2023-05-06", action: "Updated system settings" },
      { date: "2023-05-03", action: "Generated monthly report" },
    ],
  },
]);

const searchQuery = ref("");
const roleFilter = ref("");
const selectedUser = ref(null);

const filteredUsers = computed(() => {
  return users.value.filter(
    (user) =>
      (user.name.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
        user.email.toLowerCase().includes(searchQuery.value.toLowerCase())) &&
      (roleFilter.value === "" || user.role === roleFilter.value)
  );
});

let userDetailsModal;

const viewUserDetails = (user) => {
  selectedUser.value = user;
  if (!userDetailsModal) {
    userDetailsModal = new Modal(document.getElementById("userDetailsModal"));
  }
  userDetailsModal.show();
};

const deleteUser = (user) => {
  if (confirm(`Are you sure you want to delete ${user.name}?`)) {
    users.value = users.value.filter((u) => u.id !== user.id);
  }
};

const getRoleBadgeClass = (role) => {
  switch (role) {
    case "student":
      return "badge bg-primary";
    case "teacher":
      return "badge bg-success";
    case "admin":
      return "badge bg-danger";
    default:
      return "badge bg-secondary";
  }
};
</script>

<style scoped>
.admin-users {
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
[data-bs-theme="dark"] .modal-content,
[data-bs-theme="dark"] .list-group-item {
  background-color: #2c3e50;
  color: #ecf0f1;
}

[data-bs-theme="dark"] .card-footer,
[data-bs-theme="dark"] .modal-header,
[data-bs-theme="dark"] .modal-footer {
  background-color: #34495e;
  border-color: #4a6278;
}

[data-bs-theme="dark"] .btn-close {
  filter: invert(1) grayscale(100%) brightness(200%);
}

[data-bs-theme="dark"] .form-control,
[data-bs-theme="dark"] .form-select {
  background-color: #34495e;
  color: #ecf0f1;
  border-color: #4a6278;
}
</style>
