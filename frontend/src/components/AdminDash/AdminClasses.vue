<template>
  <div class="admin-classes container-fluid py-4">
    <h2 class="mb-4">Manage Classes</h2>

    <div class="row g-4 mb-4">
      <div class="col-md-3" v-for="(action, index) in actions" :key="index">
        <button
          class="btn btn-primary w-100 h-100 py-3"
          @click="openForm(action.type)"
        >
          <i :class="action.icon" class="fs-2 mb-2"></i>
          <br />
          {{ action.label }}
        </button>
      </div>
    </div>

    <div class="row g-4">
      <div class="col-md-6">
        <div class="card">
          <div class="card-header bg-primary text-white">
            <h5 class="mb-0">Classes / Qualifications</h5>
          </div>
          <div class="card-body">
            <ul class="list-group list-group-flush">
              <li
                v-for="cls in classes"
                :key="cls.id"
                class="list-group-item d-flex justify-content-between align-items-center"
              >
                {{ cls.name }}
                <span class="badge bg-primary rounded-pill"
                  >{{ cls.subjectsCount }} subjects</span
                >
              </li>
            </ul>
          </div>
        </div>
      </div>
      <div class="col-md-6">
        <div class="card">
          <div class="card-header bg-success text-white">
            <h5 class="mb-0">Subjects</h5>
          </div>
          <div class="card-body">
            <ul class="list-group list-group-flush">
              <li
                v-for="subject in subjects"
                :key="subject.id"
                class="list-group-item d-flex justify-content-between align-items-center"
              >
                {{ subject.name }}
                <span class="badge bg-success rounded-pill"
                  >{{ subject.chaptersCount }} chapters</span
                >
              </li>
            </ul>
          </div>
        </div>
      </div>
    </div>

    <!-- Modal for forms -->
    <div
      class="modal fade"
      id="formModal"
      tabindex="-1"
      aria-labelledby="formModalLabel"
      aria-hidden="true"
    >
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title" id="formModalLabel">
              {{ currentForm.title }}
            </h5>
            <button
              type="button"
              class="btn-close"
              data-bs-dismiss="modal"
              aria-label="Close"
            ></button>
          </div>
          <div class="modal-body">
            <form @submit.prevent="submitForm">
              <div class="mb-3">
                <label :for="currentForm.type" class="form-label">{{
                  currentForm.label
                }}</label>
                <input
                  :type="currentForm.inputType"
                  class="form-control"
                  :id="currentForm.type"
                  v-model="formData[currentForm.type]"
                  required
                />
              </div>
              <button type="submit" class="btn btn-primary">Submit</button>
            </form>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from "vue";
import { Modal } from "bootstrap";

const actions = [
  {
    type: "class",
    label: "Add Class / Qualification",
    icon: "bi bi-mortarboard",
  },
  { type: "subject", label: "Add Subject", icon: "bi bi-book" },
  { type: "chapter", label: "Add Chapter", icon: "bi bi-file-text" },
  { type: "quiz", label: "Manage Quizzes", icon: "bi bi-question-circle" },
];

const classes = ref([
  { id: 1, name: "Class 10", subjectsCount: 5 },
  { id: 2, name: "Class 11", subjectsCount: 6 },
  { id: 3, name: "Class 12", subjectsCount: 6 },
]);

const subjects = ref([
  { id: 1, name: "Mathematics", chaptersCount: 10 },
  { id: 2, name: "Physics", chaptersCount: 8 },
  { id: 3, name: "Chemistry", chaptersCount: 9 },
]);

const currentForm = reactive({
  type: "",
  title: "",
  label: "",
  inputType: "text",
});

const formData = reactive({
  class: "",
  subject: "",
  chapter: "",
});

let formModal;

const openForm = (type) => {
  if (type === "quiz") {
    // Navigate to quiz management page
    console.log("Navigating to quiz management page");
    return;
  }

  currentForm.type = type;
  currentForm.title = `Add New ${type.charAt(0).toUpperCase() + type.slice(1)}`;
  currentForm.label = `${type.charAt(0).toUpperCase() + type.slice(1)} Name`;

  if (!formModal) {
    formModal = new Modal(document.getElementById("formModal"));
  }
  formModal.show();
};

const submitForm = () => {
  console.log(`Submitting ${currentForm.type}:`, formData[currentForm.type]);
  // Here you would typically make an API call to save the data
  // For demonstration, we'll just add it to the local array
  if (currentForm.type === "class") {
    classes.value.push({
      id: classes.value.length + 1,
      name: formData[currentForm.type],
      subjectsCount: 0,
    });
  } else if (currentForm.type === "subject") {
    subjects.value.push({
      id: subjects.value.length + 1,
      name: formData[currentForm.type],
      chaptersCount: 0,
    });
  }

  formData[currentForm.type] = ""; // Clear the form
  formModal.hide();
};
</script>

<style scoped>
.admin-classes {
  max-width: 1200px;
  margin: 0 auto;
}

.card {
  transition: all 0.3s ease;
}

.card:hover {
  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15);
}

[data-bs-theme="dark"] .card {
  background-color: #2c3e50;
  color: #ecf0f1;
}

[data-bs-theme="dark"] .card-header {
  background-color: #34495e;
}

[data-bs-theme="dark"] .list-group-item {
  background-color: #2c3e50;
  color: #ecf0f1;
  border-color: #34495e;
}

[data-bs-theme="dark"] .modal-content {
  background-color: #2c3e50;
  color: #ecf0f1;
}

[data-bs-theme="dark"] .btn-close {
  filter: invert(1) grayscale(100%) brightness(200%);
}
</style>
