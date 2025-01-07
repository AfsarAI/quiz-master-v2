<template>
  <div class="page text-center">
    <div class="row justify-content-md-center">
      <div
        class="col d-flex align-items-center justify-content-center rounded mt-4 mb-5 mx-auto"
      >
        <h1 class="text-white">
          <span class="join-text">Join</span>
          <span class="quiz-master-text">Quiz Master</span>
          <span class="today-text">Today</span>
        </h1>
      </div>
      <div class="col bg-light rounded m-4 p-4">
        <h3
          class="text-center text-primary bg-light border-primary border rounded mb-4 p-3"
        >
          Your Profile Pic!
        </h3>
        <form @submit.prevent="register" class="mx-auto">
          <!-- Full Name and Email -->
          <div class="row mb-3">
            <div class="col-md-6">
              <label for="fullname" class="form-label">Full Name</label>
              <input
                v-model="fullname"
                type="text"
                id="fullname"
                class="form-control"
                placeholder="Enter your full name"
                required
              />
            </div>
            <div class="col-md-6">
              <label for="email" class="form-label">Email</label>
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

          <!-- Password and Confirm Password -->
          <div class="row mb-3">
            <div class="col-md-6">
              <label for="password" class="form-label">Password</label>
              <input
                v-model="password"
                type="password"
                id="password"
                class="form-control"
                placeholder="Enter your password"
                required
              />
            </div>
            <div class="col-md-6">
              <label for="confirmPassword" class="form-label"
                >Confirm Password</label
              >
              <input
                v-model="confirmPassword"
                type="password"
                id="confirmPassword"
                class="form-control"
                placeholder="Confirm your password"
                required
              />
              <!-- Live Feedback -->
              <small
                v-if="
                  password && confirmPassword && password !== confirmPassword
                "
                class="text-danger"
              >
                <ul>
                  Password do not match.
                </ul>
              </small>
              <small
                v-if="
                  password && confirmPassword && password === confirmPassword
                "
                class="text-success"
              >
                <ul>
                  Password matched.
                </ul>
              </small>
            </div>
          </div>

          <!-- Date of Birth and Gender -->
          <div class="row mb-3">
            <div class="col-md-6">
              <label for="dob" class="form-label">Date of Birth</label>
              <input
                v-model="dob"
                type="date"
                id="dob"
                class="form-control"
                required
              />
            </div>
            <div class="col-md-6">
              <label for="gender" class="form-label">Gender</label>
              <select v-model="gender" id="gender" class="form-select" required>
                <option value="" disabled hidden>Select your gender</option>
                <option value="male">Male</option>
                <option value="female">Female</option>
                <option value="other">Other</option>
              </select>
            </div>
          </div>

          <!-- Qualifications Dropdown -->
          <div class="mb-3">
            <label for="qualification" class="form-label">Qualification</label>
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

          <!-- Subjects (Checkboxes) -->
          <div class="mb-3">
            <label class="form-label"
              >Subjects
              <small class="text-small" v-if="qualification"
                >( Please select subjects by clicking on subjects buttons
                )</small
              ></label
            >
            <p class="text-center text-danger" v-if="!qualification">
              Please select a qualification before choosing subjects.
            </p>
            <div class="row">
              <div
                class="col-md-4 col-6 mb-2"
                v-for="subject in subjects"
                :key="subject.id"
              >
                <input
                  type="checkbox"
                  class="btn-check"
                  :id="'subject-' + subject.id"
                  v-model="selectedSubjects"
                  :value="subject.id"
                  autocomplete="off"
                />
                <label
                  class="btn btn-outline-primary"
                  :for="'subject-' + subject.id"
                >
                  {{ subject.name }}
                </label>
              </div>
            </div>
          </div>

          <!-- Address and Phone Number -->
          <div class="mb-3">
            <label for="address" class="form-label">Address</label>
            <textarea
              v-model="address"
              id="address"
              class="form-control"
              placeholder="Enter your address"
              required
            ></textarea>
          </div>
          <div class="mb-3">
            <label for="phone" class="form-label">Phone Number</label>
            <input
              v-model="phone"
              type="text"
              id="phone"
              class="form-control"
              placeholder="Enter your phone number"
              required
            />
          </div>

          <button type="submit" class="btn btn-primary btn-lg w-100 mt-3">
            Register
          </button>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "RegisterForm",
  data() {
    return {
      fullname: "",
      email: "",
      password: "",
      confirmPassword: "",
      dob: "",
      gender: "",
      qualification: "",
      address: "",
      phone: "",
      qualifications: [],
      subjects: [],
      selectedSubjects: [],
    };
  },
  methods: {
    async fetchData() {
      try {
        const qualRes = await fetch("http://127.0.0.1:5000/api/qualifications");
        this.qualifications = await qualRes.json();
      } catch (error) {
        console.error("Error fetching qualifications:", error);
      }
    },
    async fetchSubjects() {
      if (!this.qualification) return;
      try {
        const subjRes = await fetch(
          `http://127.0.0.1:5000/api/qualifications/${this.qualification}/subjects`
        );
        this.subjects = await subjRes.json();
      } catch (error) {
        console.error("Error fetching subjects:", error);
      }
    },
  },
  async register() {
    const userData = {
      fullname: this.fullname,
      email: this.email,
      password: this.password,
      confirmPassword: this.confirmPassword,
      dob: this.dob,
      gender: this.gender,
      qualification_id: this.qualification,
      subjects: this.selectedSubjects,
      address: this.address,
      phone: this.phone,
    };
    try {
      const response = await fetch("/api/register", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(userData),
      });
      const data = await response.json();
      console.log(data);
    } catch (error) {
      console.error("Error during registration:", error);
    }
  },
  created() {
    this.fetchData();
  },
};
</script>

<style scoped>
/* Add styles here if needed */
.page {
  background-image: url("https://picsum.photos/id/20/2000/1000/?blur=2");
  background-size: cover;
  background-position: center;
  background-attachment: fixed;
}

.container {
  margin: auto;
  background-color: rgba(255, 255, 255, 0.9);
}

/* General styling */
h1 {
  text-align: center;
  font-weight: bold;
  position: relative; /* To use absolute positioning for child elements */
  display: inline-block;
}

/* Styling for "Join" */
.join-text {
  font-size: 5cap;
  font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto,
    Oxygen, Ubuntu, Cantarell, "Open Sans", "Helvetica Neue", sans-serif;
  font-weight: normal;
  position: relative;
  top: -200px; /* Decrease this value to move it up */
  left: -10%;
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
  transform: translateX(-50%) translateY(-10px); /* Slightly adjust for upwards movement */
}

.quiz-master-text {
  font-size: 6rem;
  font-family: "Courier New", Courier, monospace;
  font-weight: bold;
  letter-spacing: 1px;
  color: #ff6347;
  position: absolute;
  top: -50px;
  left: 50%;
  transform: translateX(-50%) rotate(-5deg); /* Initial rotation */
  text-shadow: 3px 3px 6px rgba(0, 0, 0, 0.5); /* Stronger shadow */
  transition: transform 0.3s ease, color 0.2s ease; /* Smooth transition for transform and color */
}

.quiz-master-text:hover {
  transform: translateX(-50%) translateY(-5px) rotate(5deg); /* More rotation and slight upward movement */
  cursor: pointer;
  color: #ffa500; /* Change color on hover */
}

/* Styling for "Today" */
.today-text {
  font-size: 4rem;
  font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto,
    Oxygen, Ubuntu, Cantarell, "Open Sans", "Helvetica Neue", sans-serif;
  font-weight: normal;
  position: relative;
  top: 80px; /* Reduce this value to move it up */
  left: 10%;
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3); /* Same shadow as 'Join' */
  transform: translateX(-50%) translateY(5px); /* Slightly adjust position upwards */
}
</style>
