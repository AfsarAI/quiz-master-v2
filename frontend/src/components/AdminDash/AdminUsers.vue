<template>
  <div class="admin-users container-fluid py-4">
    <h2 class="mb-4">Manage Users</h2>
    <div v-if="!isLoading">
      <div v-if="users.length > 0">
        <div class="row mb-4">
          <div class="col-md-4">
            <input
              v-model="searchQuery"
              type="text"
              class="form-control"
              placeholder="Search users..."
            />
          </div>
          <div class="col-md-4">
            <select v-model="roleFilter" class="form-select">
              <option value="">All Roles</option>
              <option value="user">Student</option>
              <option value="admin">Admin</option>
            </select>
          </div>
          <div class="col-md-4">
            <select v-model="statusFilter" class="form-select">
              <option value="">All Status</option>
              <option value="active">Active</option>
              <option value="blocked">Blocked</option>
            </select>
          </div>
        </div>

        <div class="row row-cols-1 row-cols-md-2 row-cols-lg-3 g-4">
          <div v-for="user in filteredUsers" :key="user.id" class="col">
            <div class="card h-100" :class="{ 'border-danger': !user.active }">
              <div class="card-body">
                <div
                  class="d-flex justify-content-between align-items-center mb-3"
                >
                  <h5 class="card-title mb-0">{{ user.fullname }}</h5>
                  <div>
                    <span
                      :class="getRoleBadgeClass(user.roles[0]?.name)"
                      class="me-2"
                    >
                      {{
                        user.roles[0]?.name === "user"
                          ? "Student"
                          : user.roles[0]?.name
                      }}
                    </span>
                    <span v-if="!user.active" class="badge bg-danger"
                      >Blocked</span
                    >
                  </div>
                </div>
                <div class="user-avatar mb-3">
                  <img
                    :src="
                      user.profile_url ||
                      'https://picsum.photos/300/300?random=' + user.id
                    "
                    alt="User Avatar"
                    class="rounded-circle"
                  />
                </div>
                <p class="card-text">
                  <i class="bi bi-envelope me-2"></i>{{ user.email }}
                </p>
                <p class="card-text">
                  <i class="bi bi-calendar-event me-2"></i>DOB: {{ user.dob }}
                </p>
                <p class="card-text">
                  <i class="bi bi-telephone me-2"></i>{{ user.phone || "N/A" }}
                </p>
              </div>
              <div class="card-footer">
                <button
                  class="btn btn-primary me-2"
                  @click="viewUserDetails(user)"
                >
                  <i class="bi bi-eye me-1"></i>View Details
                </button>
                <button
                  v-if="user.active"
                  class="btn btn-outline-danger"
                  @click="toggleUserStatus(user, false)"
                >
                  <i class="bi bi-ban me-1"></i>Block
                </button>
                <button
                  v-else
                  class="btn btn-outline-success"
                  @click="toggleUserStatus(user, true)"
                >
                  <i class="bi bi-check-circle me-1"></i>Unblock
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
      <div v-else>
        <p>No user data found</p>
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
            <!-- Profile Image -->
            <div class="col-md-4 text-center">
              <div class="profile-image-container">
                <img
                  :src="
                    selectedUser.profile_url ||
                    'https://picsum.photos/300/300?random=' + selectedUser.id
                  "
                  class="profile-image"
                  alt="Profile Image"
                />
              </div>
              <div class="mt-3">
                <span
                  :class="getStatusBadgeClass(selectedUser.active)"
                  class="d-block mt-2"
                >
                  {{ selectedUser.active ? "Active" : "Blocked" }}
                </span>
              </div>
            </div>

            <!-- Personal Info -->
            <div class="col-md-8">
              <h6>Personal Information</h6>
              <div class="info-grid">
                <div class="info-item">
                  <strong>Name:</strong> {{ selectedUser.fullname }}
                </div>
                <div class="info-item">
                  <strong>Email:</strong> {{ selectedUser.email }}
                </div>
                <div class="info-item">
                  <strong>Role:</strong>
                  {{
                    selectedUser.roles[0]?.name === "user"
                      ? "Student"
                      : selectedUser.roles[0]?.name
                  }}
                </div>
                <div class="info-item">
                  <strong>Date of Birth:</strong> {{ selectedUser.dob }}
                </div>
                <div class="info-item">
                  <strong>Gender:</strong> {{ selectedUser.gender || "N/A" }}
                </div>
                <div class="info-item">
                  <strong>Phone:</strong> {{ selectedUser.phone || "N/A" }}
                </div>
                <div class="info-item">
                  <strong>Address:</strong> {{ selectedUser.address || "N/A" }}
                </div>
                <div class="info-item">
                  <strong>Qualification:</strong>
                  {{
                    selectedUser.qualification
                      ? selectedUser.qualification.name
                      : "N/A"
                  }}
                </div>
              </div>
            </div>
          </div>

          <!-- Subjects -->
          <div class="mt-4">
            <h6>Enrolled Subjects</h6>
            <div
              v-if="selectedUser.subjects && selectedUser.subjects.length > 0"
            >
              <div class="row">
                <div
                  v-for="(subject, index) in selectedUser.subjects"
                  :key="index"
                  class="col-md-6 mb-2"
                >
                  <div class="card">
                    <div class="card-body py-2">
                      <h6 class="mb-1">{{ subject.name }}</h6>
                      <p class="small text-muted mb-0">
                        {{ subject.description || "No description" }}
                      </p>
                    </div>
                  </div>
                </div>
              </div>
            </div>
            <p v-else class="text-muted">No subjects enrolled</p>
          </div>

          <!-- Quiz Statistics -->
          <div class="mt-4">
            <h6>Quiz Statistics</h6>
            <div v-if="selectedUser.scores && selectedUser.scores.length > 0">
              <div class="table-responsive">
                <table class="table table-striped">
                  <thead>
                    <tr>
                      <th>Quiz Name</th>
                      <th>Score</th>
                      <th>Percentage</th>
                      <th>Date</th>
                      <th>Status</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr
                      v-for="(score, index) in selectedUser.scores"
                      :key="index"
                    >
                      <td>{{ score.quiz_name }}</td>
                      <td>{{ score.score }} / {{ score.total_marks }}</td>
                      <td>{{ score.percentage.toFixed(2) }}%</td>
                      <td>{{ score.attempt_date }}</td>
                      <td>
                        <span
                          :class="
                            score.active
                              ? 'badge bg-success'
                              : 'badge bg-danger'
                          "
                        >
                          {{ score.active ? "Active" : "Inactive" }}
                        </span>
                      </td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>
            <p v-else class="text-muted">No quiz attempts found</p>
          </div>

          <!-- Action Buttons -->
          <div class="mt-4 d-flex justify-content-end">
            <button
              v-if="selectedUser.active"
              class="btn btn-danger me-2"
              @click="toggleUserStatus(selectedUser, false)"
            >
              <i class="bi bi-ban me-1"></i>Block User
            </button>
            <button
              v-else
              class="btn btn-success me-2"
              @click="toggleUserStatus(selectedUser, true)"
            >
              <i class="bi bi-check-circle me-1"></i>Unblock User
            </button>
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
import { useStore } from "vuex";

const store = useStore();

const users = ref([]);
const searchQuery = ref("");
const roleFilter = ref("");
const statusFilter = ref("");
const selectedUser = ref(null);
const isLoading = ref(false);
let userDetailsModal;

// Fetch users from API
const fetchUsers = async () => {
  try {
    isLoading.value = true;
    const response = await fetch("http://localhost:5000/api/all/users/data", {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
        "Authentication-Token": store.state.user?.token,
      },
    });
    const data = await response.json();

    console.log("API Response:", data);

    if (Array.isArray(data)) {
      users.value = data;
    } else {
      console.error("Unexpected API response format", data);
    }
  } catch (error) {
    console.error("Error fetching users:", error);
  } finally {
    isLoading.value = false;
  }
};

// Toggle user active status (block/unblock)
const toggleUserStatus = async (user, status) => {
  const action = status ? "unblock" : "block";
  const confirmMessage = `Are you sure you want to ${action} ${user.fullname}?`;

  if (confirm(confirmMessage)) {
    try {
      const response = await fetch(
        `http://localhost:5000/api/user/${user.id}/status`,
        {
          method: "PUT",
          headers: {
            "Content-Type": "application/json",
            "Authentication-Token": store.state.user?.token,
          },
          body: JSON.stringify({ active: status }),
        }
      );

      if (response.ok) {
        // Update in the users array
        const index = users.value.findIndex((u) => u.id === user.id);
        if (index !== -1) {
          users.value[index].active = status;
        }

        // Update selected user if in modal
        if (selectedUser.value && selectedUser.value.id === user.id) {
          selectedUser.value.active = status;
        }

        store.dispatch("addToast", {
          message: `User ${action}ed successfully!`,
          type: "success",
        });
      } else {
        alert(`Failed to ${action} user. Please try again.`);
      }
    } catch (error) {
      console.error(`Error ${action}ing user:`, error);
      alert(`Error ${action}ing user. Please check console for details.`);
    }
  }
};

// Computed property for filtered users
const filteredUsers = computed(() => {
  return (users.value || []).filter((user) => {
    // Search filter
    const matchesSearch =
      user.fullname?.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
      user.email?.toLowerCase().includes(searchQuery.value.toLowerCase());

    // Role filter
    const matchesRole =
      roleFilter.value === "" ||
      user.roles?.some((role) => role.name === roleFilter.value);

    // Status filter
    const matchesStatus =
      statusFilter.value === "" ||
      (statusFilter.value === "active" && user.active) ||
      (statusFilter.value === "blocked" && !user.active);

    return matchesSearch && matchesRole && matchesStatus;
  });
});

// Show user details modal
const viewUserDetails = (user) => {
  selectedUser.value = user;
  if (!userDetailsModal) {
    userDetailsModal = new Modal(document.getElementById("userDetailsModal"), {
      backdrop: "static",
    });
  }
  userDetailsModal.show();
};

// Get badge class for role
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

// Get badge class for status
const getStatusBadgeClass = (active) => {
  return active ? "badge bg-success" : "badge bg-danger";
};

// Mount component and fetch data
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

.user-avatar {
  text-align: center;
}

.user-avatar img {
  width: 100px;
  height: 100px;
  object-fit: cover;
  border: 3px solid #f8f9fa;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
}

.profile-image-container {
  width: 150px;
  height: 150px;
  margin: 0 auto;
  border-radius: 50%;
  overflow: hidden;
  border: 4px solid #f8f9fa;
  box-shadow: 0 3px 10px rgba(0, 0, 0, 0.2);
}

.profile-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.info-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 10px;
}

.info-item {
  padding: 8px;
  border-bottom: 1px solid #eee;
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

[data-bs-theme="dark"] .info-item {
  border-color: #4a6278;
}

[data-bs-theme="dark"] .profile-image-container {
  border-color: #34495e;
}
</style>
