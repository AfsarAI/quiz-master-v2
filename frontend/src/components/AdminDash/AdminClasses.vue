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
                v-for="qual in Qualifications"
                :key="qual.id"
                class="list-group-item d-flex justify-content-between align-items-center"
              >
                {{ qual.name }}
                <span class="badge bg-primary rounded-pill">
                  {{ qual.subjects?.length || 0 }} subjects
                </span>
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
                v-for="sub in Subjects"
                :key="sub.id"
                class="list-group-item d-flex justify-content-between align-items-center"
                index="subject.id"
              >
                {{ sub.name }}
                <span class="badge bg-success rounded-pill">
                  {{ sub.chapters?.length || 0 }} chapters
                </span>
              </li>
            </ul>
          </div>
        </div>
      </div>
    </div>

    <!-- Modal for Forms -->
    <div class="modal fade" id="formModal" tabindex="-1" aria-hidden="true">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">{{ currentForm.title }}</h5>
            <button
              type="button"
              class="btn-close"
              data-bs-dismiss="modal"
            ></button>
          </div>
          <div class="modal-body">
            <form @submit.prevent="submitForm">
              <div class="mb-3" v-if="currentForm.type === 'qualification'">
                <label class="form-label">Qualification Name</label>
                <input
                  type="text"
                  class="form-control"
                  v-model="formData.name"
                  required
                />
                <label class="form-label">Description</label>
                <textarea
                  type="text"
                  class="form-control"
                  v-model="formData.description"
                  required
                ></textarea>
              </div>
              <div class="mb-3" v-if="currentForm.type === 'subject'">
                <label class="form-label mt-2">Select Qualification</label>
                <select class="form-control" v-model="formData.qualId">
                  <option
                    v-for="qual in Qualifications"
                    :key="qual.id"
                    :value="qual.id"
                  >
                    {{ qual.name }}
                  </option>
                </select>
                <label class="form-label">Subject Name</label>
                <input
                  type="text"
                  class="form-control"
                  v-model="formData.name"
                  required
                />
                <label class="form-label">Description</label>
                <textarea
                  type="text"
                  class="form-control"
                  v-model="formData.description"
                  required
                ></textarea>
              </div>
              <div class="mb-3" v-if="currentForm.type === 'chapter'">
                <label class="form-label mt-2">Select Subject</label>
                <select class="form-control" v-model="formData.subjectId">
                  <option v-for="sub in Subjects" :key="sub.id" :value="sub.id">
                    {{ sub.name }}
                  </option>
                </select>
                <label class="form-label">Chapater Name</label>
                <input
                  type="text"
                  class="form-control"
                  v-model="formData.name"
                  required
                />
                <label class="form-label">Description</label>
                <textarea
                  type="text"
                  class="form-control"
                  v-model="formData.description"
                  required
                ></textarea>
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
import { ref, reactive, onMounted } from "vue";
import { useRouter } from "vue-router";
import { Modal } from "bootstrap";

const apiBase = "http://127.0.0.1:5000/api/admin/dashboard";
const router = useRouter();

const actions = [
  {
    type: "qualification",
    label: "Add Qualification",
    icon: "bi bi-mortarboard",
  },
  { type: "subject", label: "Add Subject", icon: "bi bi-book" },
  { type: "chapter", label: "Add Chapater", icon: "bi bi-file-text" },
  { type: "quiz", label: "Manage Quizzes", icon: "bi bi-question-circle" },
];

const Qualifications = ref([]);
const Subjects = ref([]);
const currentForm = reactive({ type: "", title: "" });
const formData = reactive({
  name: "",
  description: "",
  qualId: null,
  subjectId: null,
});
let formModal;
const fetchData = async () => {
  try {
    const [qualRes, subjectRes] = await Promise.all([
      fetch(`${apiBase}/all/qualifications`).then((res) => res.json()),
      fetch(`${apiBase}/all/subjects`).then((res) => res.json()),
    ]);
    Qualifications.value = qualRes;
    Subjects.value = subjectRes;
  } catch (error) {
    console.error("Error fetching data:", error);
  }
};

const openForm = (type) => {
  if (type === "quiz") {
    router.push("quizzes");
    console.log("Navigating to quiz page");
    return;
  }
  currentForm.type = type;
  currentForm.title = `Add New ${type.charAt(0).toUpperCase() + type.slice(1)}`;
  formData.name = "";
  formData.classId = null;
  if (!formModal) {
    formModal = new Modal(document.getElementById("formModal"));
  }
  formModal.show();
};
const submitForm = async () => {
  try {
    let endpoint = "";
    let payload = {};

    if (currentForm.type === "qualification") {
      endpoint = "add/qualification"; // API: /api/dashboard/classes
      payload = {
        name: formData.name,
        description: formData.description,
      };
    } else if (currentForm.type === "subject") {
      endpoint = "add/subject"; // API: /api/dashboard/subjects
      payload = {
        name: formData.name,
        description: formData.description,
        qualId: formData.qualId,
      };
    } else if (currentForm.type === "chapter") {
      endpoint = "add/chapter"; // API: /api/dashboard/chapters
      payload = {
        name: formData.name,
        description: formData.description,
        subjectId: formData.subjectId, // yeh 'classId' nahi 'subjectId' hoga
      };
    }

    // API request send karna
    const response = await fetch(`${apiBase}/${endpoint}`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(payload),
    });

    if (!response.ok) {
      throw new Error("Network response was not ok");
    }
    // Data refresh karna
    await fetchData();
    formModal.hide();
  } catch (error) {
    console.error("Error adding data:", error);
  }
};

onMounted(fetchData);
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
