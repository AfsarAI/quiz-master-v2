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
          <option value="user">Student</option>
          <option value="admin">Admin</option>
        </select>
      </div>
    </div>

    <div class="row row-cols-1 row-cols-md-2 row-cols-lg-3 g-4">
      <div v-for="user in filteredUsers" :key="user.id" class="col">
        <div class="card h-100">
          <div class="card-body">
            <div class="d-flex justify-content-between align-items-center mb-3">
              <h5 class="card-title mb-0">{{ user.fullname }}</h5>
              <span :class="getRoleBadgeClass(user.roles[0]?.name)">{{
                user.roles[0]?.name
              }}</span>
            </div>
            <p class="card-text">
              <i class="bi bi-envelope me-2"></i>{{ user.email }}
            </p>
            <p class="card-text">
              <i class="bi bi-calendar-event me-2"></i>DOB: {{ user.dob }}
            </p>
            <p class="card-text">
              <i class="bi bi-telephone me-2"></i>{{ user.phone }}
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
  </div>

  <!-- User Details Modal -->
  <div
    class="modal fade"
    id="userDetailsModal"
    tabindex="-1"
    aria-hidden="true"
  >
    <div class="modal-dialog modal-lg">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title">User Details</h5>
          <button
            type="button"
            class="btn-close"
            data-bs-dismiss="modal"
          ></button>
        </div>
        <div class="modal-body" v-if="selectedUser">
          <div class="row">
            <!-- 🟢 Profile Image -->
            <div class="col-md-4 text-center">
              <img
                v-if="selectedUser.profileImage"
                :src="selectedUser.profileImage"
                class="rounded-circle img-fluid"
                alt="Profile Image"
              />
              <img
                v-else
                src="https://picsum.photos/300/200?random=1"
                class="rounded-circle img-fluid"
                alt="Default Avatar"
              />
            </div>

            <!-- 🟢 Personal Info -->
            <div class="col-md-8">
              <h6>Personal Information</h6>
              <p><strong>Name:</strong> {{ selectedUser.fullname }}</p>
              <p><strong>Email:</strong> {{ selectedUser.email }}</p>
              <p><strong>Role:</strong> {{ selectedUser.roles[0]?.name }}</p>
              <p><strong>Date of Birth:</strong> {{ selectedUser.dob }}</p>
            </div>
          </div>

          <!-- 🟢 Quiz Statistics -->
          <div class="mt-3">
            <h6>Quiz Statistics</h6>
            <p>
              <strong>Quizzes Taken:</strong>
              {{ selectedUser.quizzesTaken || "N/A" }}
            </p>
            <p>
              <strong>Average Score:</strong>
              {{ selectedUser.averageScore || "N/A" }}%
            </p>
            <p>
              <strong>Highest Score:</strong>
              {{ selectedUser.highestScore || "N/A" }}%
            </p>
          </div>

          <!-- 🟢 Recent Activity -->
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
</template>

<script setup>
import { ref, computed, onMounted } from "vue";
import { Modal } from "bootstrap";

const users = ref([]);
const searchQuery = ref("");
const roleFilter = ref("");
const selectedUser = ref(null);
let userDetailsModal;

// 🟢 API se data fetch karne ka function
const fetchUsers = async () => {
  try {
    const response = await fetch("http://localhost:5000/api/all/users/data");
    const data = await response.json();

    console.log("API Response:", data); // 🟢 Check if data is correct

    if (Array.isArray(data)) {
      users.value = data; // ✅ Assign users array properly
    } else {
      console.error("Unexpected API response format", data);
    }
  } catch (error) {
    console.error("Error fetching users:", error);
  }
};

// 🟢 Computed property jo search & filter apply kare
const filteredUsers = computed(() => {
  return (users.value || []).filter(
    (user) =>
      (user.fullname?.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
        user.email?.toLowerCase().includes(searchQuery.value.toLowerCase())) &&
      (roleFilter.value === "" ||
        user.roles?.some((role) => role.name === roleFilter.value))
  );
});

// 🟢 User details modal dikhane ka function
const viewUserDetails = (user) => {
  selectedUser.value = user;
  if (!userDetailsModal) {
    userDetailsModal = new Modal(document.getElementById("userDetailsModal"), {
      backdrop: "static",
    });
  }
  userDetailsModal.show();
};

// 🟢 User delete karne ka function
const deleteUser = (user) => {
  if (confirm(`Are you sure you want to delete ${user.fullname}?`)) {
    users.value = users.value.filter((u) => u.id !== user.id);
  }
};

// 🟢 Role ke hisaab se badge color dena
const getRoleBadgeClass = (role) => {
  switch (role) {
    case "user":
      return "badge bg-success";
    case "admin":
      return "badge bg-danger";
    default:
      return "badge bg-secondary";
  }
};

// 🟢 Jab component mount ho, tab API call kare
onMounted(fetchUsers);
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
