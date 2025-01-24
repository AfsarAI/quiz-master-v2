<template>
  <div class="user-profile container my-5">
    <div v-if="loading" class="text-center my-5">
      <div class="spinner-border text-primary" role="status">
        <span class="visually-hidden">Loading...</span>
      </div>
      <p>Loading profile data...</p>
    </div>
    <div v-else class="row justify-content-center">
      <div class="col-md-8">
        <div class="card shadow-lg border-0">
          <div class="card-body">
            <div class="d-flex align-items-center mb-4">
              <img
                :src="user.profile_url || 'https://via.placeholder.com/150'"
                alt="Profile Picture"
                class="rounded-circle me-4"
                style="width: 120px; height: 120px; object-fit: cover"
              />
              <div>
                <h3 class="card-title mb-1">{{ user.fullname }}</h3>
                <p class="text-muted mb-0">{{ user.email }}</p>
                <p class="mb-0">
                  <strong>Qualification:</strong> {{ user.qualification_id }}
                </p>
              </div>
            </div>
            <ul class="nav nav-tabs mb-4" id="profileTabs" role="tablist">
              <li class="nav-item" role="presentation">
                <button
                  class="nav-link active"
                  id="personal-tab"
                  data-bs-toggle="tab"
                  data-bs-target="#personal"
                  type="button"
                  role="tab"
                  aria-controls="personal"
                  aria-selected="true"
                >
                  Personal Info
                </button>
              </li>
              <li class="nav-item" role="presentation">
                <button
                  class="nav-link"
                  id="academic-tab"
                  data-bs-toggle="tab"
                  data-bs-target="#academic"
                  type="button"
                  role="tab"
                  aria-controls="academic"
                  aria-selected="false"
                >
                  Academic Info
                </button>
              </li>
            </ul>
            <div class="tab-content" id="profileTabsContent">
              <div
                class="tab-pane fade show active"
                id="personal"
                role="tabpanel"
                aria-labelledby="personal-tab"
              >
                <div class="row">
                  <div class="col-md-6 mb-3">
                    <h6>Date of Birth</h6>
                    <p>{{ user.dob }}</p>
                  </div>
                  <div class="col-md-6 mb-3">
                    <h6>Gender</h6>
                    <p>{{ user.gender }}</p>
                  </div>
                  <div class="col-md-6 mb-3">
                    <h6>Phone</h6>
                    <p>{{ user.phone }}</p>
                  </div>
                  <div class="col-md-6 mb-3">
                    <h6>Address</h6>
                    <p>{{ user.address }}</p>
                  </div>
                </div>
              </div>
              <div
                class="tab-pane fade"
                id="academic"
                role="tabpanel"
                aria-labelledby="academic-tab"
              >
                <div class="row">
                  <div class="col-md-6 mb-3">
                    <h6>Current Grade</h6>
                    <p>{{ user.current_grade || "Not specified" }}</p>
                  </div>
                  <div class="col-md-6 mb-3">
                    <h6>School/Institution</h6>
                    <p>{{ user.school || "Not specified" }}</p>
                  </div>
                  <div class="col-md-6 mb-3">
                    <h6>Favorite Subjects</h6>
                    <p>
                      {{
                        user.favorite_subjects
                          ? user.favorite_subjects.join(", ")
                          : "Not specified"
                      }}
                    </p>
                  </div>
                  <div class="col-md-6 mb-3">
                    <h6>Learning Goals</h6>
                    <p>{{ user.learning_goals || "Not specified" }}</p>
                  </div>
                </div>
              </div>
            </div>
            <div class="text-center mt-4">
              <button @click="editProfile" class="btn btn-primary">
                Edit Profile
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from "vue";
import { useStore } from "vuex";

const store = useStore();
const user = ref({
  fullname: "",
  email: "",
  dob: "",
  gender: "",
  phone: "",
  address: "",
  qualification_id: "",
  profile_url: "",
  current_grade: "",
  school: "",
  favorite_subjects: [],
  learning_goals: "",
});
const loading = ref(true);

const userId = computed(() => store.state.user.id);
const authToken = computed(() => store.state.user.auth_token);

const fetchUserData = async () => {
  try {
    if (!userId.value || !authToken.value) {
      throw new Error("User ID or authentication token is missing!");
    }
    const response = await fetch(
      `http://127.0.0.1:5000/api/user/${userId.value}/data`,
      {
        headers: {
          "Authentication-Token": authToken.value,
          "Content-Type": "application/json",
        },
      }
    );
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    const data = await response.json();
    user.value = { ...user.value, ...data };
  } catch (error) {
    console.error("Error fetching user data:", error);
    store.dispatch("addToast", {
      type: "error",
      message: "Failed to load user profile data.",
    });
  } finally {
    loading.value = false;
  }
};

const editProfile = () => {
  // Implement edit profile functionality
  console.log("Edit profile clicked");
};

onMounted(fetchUserData);
</script>

<style scoped>
.card {
  background: #ffffff;
  border-radius: 15px;
}
.card-body {
  padding: 2rem;
}
.card-title {
  font-size: 1.5rem;
  font-weight: bold;
}
.text-muted {
  font-size: 0.9rem;
}
.spinner-border {
  width: 3rem;
  height: 3rem;
}
.nav-tabs .nav-link {
  color: #495057;
}
.nav-tabs .nav-link.active {
  color: #007bff;
}

[data-bs-theme="dark"] .card {
  background-color: #2c3e50;
  color: #ecf0f1;
}
[data-bs-theme="dark"] .nav-tabs .nav-link {
  color: #ecf0f1;
}
[data-bs-theme="dark"] .nav-tabs .nav-link.active {
  color: #3498db;
  background-color: #34495e;
  border-color: #4a6278;
}
[data-bs-theme="dark"] .text-muted {
  color: #bdc3c7 !important;
}
</style>
