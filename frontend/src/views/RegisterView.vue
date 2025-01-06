<template>
  <div
    class="container bg-light p-5 rounded shadow-lg mt-4 mb-5"
    style="max-width: 700px"
  >
    <h3
      class="text-center text-primary bg-light border-primary border rounded mb-4 p-3"
    >
      Join Quiz Master Today
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
          required
        >
          <option value="" disabled hidden>Select your qualification</option>
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
        <label class="form-label">Subjects</label>
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
        const [qualRes, subjRes] = await Promise.all([
          fetch("/api/qualifications"),
          fetch("/api/subjects"),
        ]);
        this.qualifications = await qualRes.json();
        this.subjects = await subjRes.json();
      } catch (error) {
        console.error("Error fetching data:", error);
      }
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
  },
  created() {
    this.fetchData();
  },
};
</script>

<style scoped>
/* Add styles here if needed */
</style>
