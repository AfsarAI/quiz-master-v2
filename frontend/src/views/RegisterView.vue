<template>
  <div>
    <app-navbar />
    <div class="register-container">
      <div class="container mt-4 mb-4">
        <div class="row justify-content-center align-items-center min-vh-100">
          <div class="col-md-10">
            <div class="card shadow-lg border-0">
              <div class="card-body p-5">
                <h2 class="text-center text-primary mb-4">
                  <span class="join-text">Join</span>
                  <router-link to="/" class="text-decoration-none">
                    <span class="quiz-master-text">Quiz Master</span>
                  </router-link>
                  <span class="today-text">Today</span>
                </h2>
                <div class="row">
                  <div class="col-md-4">
                    <div
                      class="profile-pic-container mb-3"
                      @click="triggerFileInput"
                    >
                      <img
                        :src="profilePicUrl"
                        alt="Profile Picture"
                        class="profile-pic"
                      />
                      <div class="overlay">
                        <i class="bi bi-plus-circle-fill fs-1"></i>
                      </div>
                    </div>
                    <input
                      type="file"
                      ref="fileInput"
                      @change="handleFileUpload"
                      style="display: none"
                      accept="image/*"
                    />
                    <h3 class="text-center">{{ displayName }}</h3>
                    <p class="text-muted small text-center" v-if="!fullname">
                      When you enter your name, it will appear here!
                    </p>
                    <div v-if="hasEnteredData" class="mt-4">
                      <h5 class="text-start">Your Entered Data:</h5>
                      <ul class="list-group list-group-flush">
                        <li class="list-group-item text-start" v-if="email">
                          <strong>Email ID:</strong> {{ email }}
                        </li>
                        <li class="list-group-item text-start" v-if="dob">
                          <strong>Date of Birth:</strong> {{ dob }}
                        </li>
                        <li class="list-group-item text-start" v-if="gender">
                          <strong>Gender:</strong> {{ gender }}
                        </li>
                        <li
                          class="list-group-item text-start"
                          v-if="qualification"
                        >
                          <strong>Qualification:</strong>
                          {{
                            qualifications.find(
                              (qual) => qual.id === qualification
                            )?.name
                          }}
                        </li>
                        <li
                          class="list-group-item text-start"
                          v-if="selectedSubjects.length > 0"
                        >
                          <strong>Subjects:</strong>
                          <ul>
                            <li
                              v-for="(id, index) in selectedSubjects"
                              :key="index"
                            >
                              {{
                                subjects.find((subj) => subj.id === id)?.name ||
                                "Unknown Subject"
                              }}
                            </li>
                          </ul>
                        </li>
                        <li class="list-group-item text-start" v-if="address">
                          <strong>Address:</strong> {{ address }}
                        </li>
                        <li class="list-group-item text-start" v-if="phone">
                          <strong>Phone Number:</strong> {{ phone }}
                        </li>
                      </ul>
                    </div>
                  </div>
                  <div class="col-md-8">
                    <form @submit.prevent="register">
                      <div class="row">
                        <div class="col-md-6 mb-3">
                          <label for="fullname" class="form-label"
                            >Full Name</label
                          >
                          <div class="input-group">
                            <span class="input-group-text"
                              ><i class="bi bi-person"></i
                            ></span>
                            <input
                              v-model="fullname"
                              type="text"
                              id="fullname"
                              class="form-control"
                              placeholder="Enter your full name"
                              required
                            />
                          </div>
                        </div>
                        <div class="col-md-6 mb-3">
                          <label for="email" class="form-label">Email</label>
                          <div class="input-group">
                            <span class="input-group-text"
                              ><i class="bi bi-envelope"></i
                            ></span>
                            <input
                              v-model="email"
                              type="email"
                              id="email"
                              class="form-control"
                              placeholder="Enter your email"
                              required
                            />
                          </div>
                        </div>
                      </div>
                      <div class="row">
                        <div class="col-md-6 mb-3">
                          <label for="password" class="form-label"
                            >Password</label
                          >
                          <div class="input-group">
                            <span class="input-group-text"
                              ><i class="bi bi-lock"></i
                            ></span>
                            <input
                              v-model="password"
                              :type="showPassword ? 'text' : 'password'"
                              id="password"
                              class="form-control"
                              placeholder="Enter your password"
                              required
                            />
                            <button
                              class="btn btn-outline-secondary"
                              type="button"
                              @click="togglePassword"
                            >
                              <i
                                :class="
                                  showPassword ? 'bi bi-eye-slash' : 'bi bi-eye'
                                "
                              ></i>
                            </button>
                          </div>
                        </div>
                        <div class="col-md-6 mb-3">
                          <label for="confirmPassword" class="form-label"
                            >Confirm Password</label
                          >
                          <div class="input-group">
                            <span class="input-group-text"
                              ><i class="bi bi-lock"></i
                            ></span>
                            <input
                              v-model="confirmPassword"
                              :type="showConfirmPassword ? 'text' : 'password'"
                              id="confirmPassword"
                              class="form-control"
                              placeholder="Confirm your password"
                              required
                            />
                            <button
                              class="btn btn-outline-secondary"
                              type="button"
                              @click="toggleConfirmPassword"
                            >
                              <i
                                :class="
                                  showConfirmPassword
                                    ? 'bi bi-eye-slash'
                                    : 'bi bi-eye'
                                "
                              ></i>
                            </button>
                          </div>
                          <small
                            v-if="
                              password &&
                              confirmPassword &&
                              password !== confirmPassword
                            "
                            class="text-danger"
                            >Passwords do not match.</small
                          >
                          <small
                            v-if="
                              password &&
                              confirmPassword &&
                              password === confirmPassword
                            "
                            class="text-success"
                            >Passwords match.</small
                          >
                        </div>
                      </div>
                      <div class="row">
                        <div class="col-md-4 mb-3">
                          <label for="dob" class="form-label"
                            >Date of Birth</label
                          >
                          <div class="input-group">
                            <span class="input-group-text"
                              ><i class="bi bi-calendar"></i
                            ></span>
                            <input
                              v-model="dob"
                              type="date"
                              id="dob"
                              class="form-control"
                              required
                            />
                          </div>
                        </div>
                        <div class="col-md-4 mb-3">
                          <label for="gender" class="form-label">Gender</label>
                          <div class="input-group">
                            <span class="input-group-text"
                              ><i class="bi bi-gender-ambiguous"></i
                            ></span>
                            <select
                              v-model="gender"
                              id="gender"
                              class="form-select"
                              required
                            >
                              <option value="" disabled hidden>
                                Select your gender
                              </option>
                              <option value="male">Male</option>
                              <option value="female">Female</option>
                              <option value="other">Other</option>
                            </select>
                          </div>
                        </div>
                        <div class="col-md-4 mb-3">
                          <label for="qualification" class="form-label"
                            >Qualification</label
                          >
                          <div class="input-group">
                            <span class="input-group-text"
                              ><i class="bi bi-mortarboard"></i
                            ></span>
                            <select
                              v-model="qualification"
                              id="qualification"
                              class="form-select"
                              @change="fetchSubjects"
                              required
                            >
                              <option value="" disabled hidden>
                                Select your qualification
                              </option>
                              <option
                                v-for="qual in qualifications"
                                :key="qual.id"
                                :value="qual.id"
                              >
                                {{ qual.name }}
                              </option>
                            </select>
                          </div>
                        </div>
                      </div>
                      <div class="mb-3">
                        <label class="form-label">Subjects</label>
                        <p class="text-muted small" v-if="qualification">
                          Please select subjects by clicking on the buttons
                          below
                        </p>
                        <p class="text-danger small" v-if="!qualification">
                          Please select a qualification before choosing
                          subjects.
                        </p>
                        <div class="subject-grid">
                          <button
                            v-for="subject in subjects"
                            :key="subject.id"
                            @click.prevent="toggleSubject(subject.id)"
                            :class="[
                              'btn',
                              'btn-outline-primary',
                              'btn-sm',
                              'mb-2',
                              { active: selectedSubjects.includes(subject.id) },
                            ]"
                          >
                            {{ subject.name }}
                          </button>
                        </div>
                      </div>
                      <div class="row">
                        <div class="col-md-6 mb-3">
                          <label for="address" class="form-label"
                            >Address</label
                          >
                          <div class="input-group">
                            <span class="input-group-text"
                              ><i class="bi bi-geo-alt"></i
                            ></span>
                            <textarea
                              v-model="address"
                              id="address"
                              class="form-control"
                              placeholder="Enter your address"
                              required
                            ></textarea>
                          </div>
                        </div>
                        <div class="col-md-6 mb-3">
                          <label for="phone" class="form-label"
                            >Phone Number</label
                          >
                          <div class="input-group">
                            <span class="input-group-text"
                              ><i class="bi bi-telephone"></i
                            ></span>
                            <input
                              v-model="phone"
                              type="tel"
                              id="phone"
                              class="form-control"
                              placeholder="Enter your phone number"
                              required
                            />
                          </div>
                        </div>
                      </div>
                      <div class="text-center">
                        <button
                          type="submit"
                          class="btn btn-primary btn-register"
                        >
                          Register
                        </button>
                      </div>
                    </form>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    <app-footer />
  </div>
</template>

<script setup>
import AppNavbar from "@/components/Navbar.vue";
import AppFooter from "@/components/Footer.vue";

import { ref, computed, onMounted } from "vue";
import { useRouter } from "vue-router";

const router = useRouter();
const fullname = ref("");
const email = ref("");
const password = ref("");
const confirmPassword = ref("");
const dob = ref("");
const gender = ref("");
const qualification = ref("");
const address = ref("");
const phone = ref("");
const qualifications = ref([]);
const subjects = ref([]);
const selectedSubjects = ref([]);
const profilePicUrl = ref("https://via.placeholder.com/150");
const fileInput = ref(null);
const showPassword = ref(false);
const showConfirmPassword = ref(false);

const displayName = computed(() => fullname.value || "Quiz Master");

const hasEnteredData = computed(() => {
  return (
    email.value ||
    dob.value ||
    gender.value ||
    qualification.value ||
    selectedSubjects.value.length > 0 ||
    address.value ||
    phone.value
  );
});

const fetchData = async () => {
  try {
    const qualRes = await fetch("http://127.0.0.1:5000/api/qualifications");
    qualifications.value = await qualRes.json();
  } catch (error) {
    console.error("Error fetching qualifications:", error);
  }
};

const fetchSubjects = async () => {
  if (!qualification.value) return;
  try {
    const subjRes = await fetch(
      `http://127.0.0.1:5000/api/qualifications/${qualification.value}/subjects`
    );
    subjects.value = await subjRes.json();
  } catch (error) {
    console.error("Error fetching subjects:", error);
  }
};

const toggleSubject = (subjectId) => {
  const index = selectedSubjects.value.indexOf(subjectId);
  if (index === -1) {
    selectedSubjects.value.push(subjectId);
  } else {
    selectedSubjects.value.splice(index, 1);
  }
};

const triggerFileInput = () => {
  fileInput.value.click();
};

const handleFileUpload = (event) => {
  const file = event.target.files[0];
  if (file) {
    const reader = new FileReader();
    reader.onload = (e) => {
      profilePicUrl.value = e.target.result;
    };
    reader.readAsDataURL(file);
  }
};

const togglePassword = () => {
  showPassword.value = !showPassword.value;
};

const toggleConfirmPassword = () => {
  showConfirmPassword.value = !showConfirmPassword.value;
};

const register = async () => {
  if (password.value !== confirmPassword.value) {
    alert("Passwords do not match!");
    return;
  }

  const userData = {
    fullname: fullname.value,
    email: email.value,
    password: password.value,
    dob: dob.value,
    gender: gender.value,
    address: address.value,
    phone: phone.value,
    profilePicUrl: profilePicUrl.value,
    qualification_id: qualification.value,
    subjects: selectedSubjects.value,
  };
  console.log(userData);
  try {
    const response = await fetch("http://127.0.0.1:5000/api/user/register", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(userData),
    });
    const data = await response.json();
    console.log(data);
    // Handle successful registration (e.g., show success message, redirect)
    alert("Registration successful!"); // Replace with a more user-friendly notification
    router.push("/login"); // Redirect to login page after successful registration
  } catch (error) {
    console.error("Error during registration:", error);
    alert("Registration failed. Please try again."); // Replace with a more user-friendly error handling
  }
};

onMounted(() => {
  fetchData();
});
</script>

<style scoped>
.register-container {
  background: linear-gradient(135deg, #3a0ca3, #4361ee, #8e44ad);
  min-height: 100vh;
  position: relative;
  overflow: hidden;
}

.register-container::before {
  content: "";
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: url('data:image/svg+xml;charset=utf8,%3Csvg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1440 320"%3E%3Cpath fill="%23ffffff" fill-opacity="0.05" d="M0,96L48,112C96,128,192,160,288,186.7C384,213,480,235,576,213.3C672,192,768,128,864,128C960,128,1056,192,1152,208C1248,224,1344,192,1392,176L1440,160L1440,320L1392,320C1344,320,1248,320,1152,320C1056,320,960,320,864,320C768,320,672,320,576,320C480,320,384,320,288,320C192,320,96,320,48,320L0,320Z"%3E%3C/path%3E%3C/svg%3E')
    no-repeat bottom;
  background-size: cover;
}
[data-bs-theme="dark"] .register-container {
  background: #34495e;
}
.card {
  /* background-color: rgba(255, 255, 255, 0.9); */
  backdrop-filter: blur(10px);
}

.form-control:focus,
.btn:focus {
  box-shadow: 0 0 0 0.25rem rgba(13, 110, 253, 0.25);
}

.btn-primary {
  background-color: #3498db;
  border-color: #3498db;
  transition: all 0.3s ease;
}

.btn-primary:hover {
  background-color: #2980b9;
  border-color: #2980b9;
}

.text-primary {
  color: #3498db !important;
}

[data-bs-theme="light"] .input-group-text {
  background-color: #f8f9fa;
}

.join-text,
.today-text {
  font-size: 1.5rem;
  font-weight: 300;
  color: #3498db;
  text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.1);
}

.quiz-master-text {
  font-size: 2rem;
  font-weight: 700;
  color: #3498db;
  margin: 0 0.5rem;
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.2);
  transition: transform 0.3s ease, color 0.2s ease;
}

.quiz-master-text:hover {
  transform: translateY(-2px) rotate(2deg);
  color: #2980b9;
}

.profile-pic-container {
  position: relative;
  width: 150px;
  height: 150px;
  margin: 0 auto;
  cursor: pointer;
  overflow: hidden;
  border-radius: 50%;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.profile-pic {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  opacity: 0;
  transition: opacity 0.3s ease;
}

.profile-pic-container:hover .overlay {
  opacity: 1;
}

.subject-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(100px, 1fr));
  gap: 0.5rem;
}

.btn-register {
  background: linear-gradient(to right, #3498db, #2980b9);
  border: none;
  padding: 10px 30px;
  font-size: 1.1rem;
  font-weight: bold;
  text-transform: uppercase;
  letter-spacing: 1px;
  transition: all 0.3s ease;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.btn-register:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 8px rgba(0, 0, 0, 0.15);
}

.btn-register:active {
  transform: translateY(1px);
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

@media (max-width: 768px) {
  .join-text,
  .today-text {
    font-size: 1.2rem;
  }

  .quiz-master-text {
    font-size: 1.5rem;
  }
}
</style>
