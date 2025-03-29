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

    <div
      v-if="
        Qualifications.length > 0 && Subjects.length > 0 && Chapters.length > 0
      "
    >
      <div class="row g-4">
        <div class="col-md-4">
          <div class="card">
            <div
              class="card-header bg-primary text-white d-flex justify-content-between align-items-center"
            >
              <h5 class="mb-0">Classes / Qualifications</h5>
              <div class="search-box">
                <input
                  type="text"
                  class="form-control form-control-sm"
                  placeholder="Search..."
                  v-model="qualificationSearch"
                />
              </div>
            </div>
            <div class="card-body">
              <ul class="list-group list-group-flush">
                <li
                  v-for="qual in filteredQualifications"
                  :key="qual.id"
                  class="list-group-item d-flex justify-content-between align-items-center"
                >
                  {{ qual.name }}
                  <div>
                    <span class="badge bg-primary rounded-pill me-2">
                      {{ qual.subjects?.length || 0 }} subjects
                    </span>
                    <button
                      class="btn btn-sm btn-outline-primary me-1"
                      @click="editItem('qualification', qual)"
                    >
                      <i class="bi bi-pencil"></i>
                    </button>
                    <button
                      class="btn btn-sm btn-outline-danger"
                      @click="deleteItem('qualification', qual.id)"
                    >
                      <i class="bi bi-trash"></i>
                    </button>
                  </div>
                </li>
              </ul>
            </div>
          </div>
        </div>
        <div class="col-md-4">
          <div class="card">
            <div
              class="card-header bg-success text-white d-flex justify-content-between align-items-center"
            >
              <h5 class="mb-0">Subjects</h5>
              <div class="search-box">
                <input
                  type="text"
                  class="form-control form-control-sm"
                  placeholder="Search..."
                  v-model="subjectSearch"
                />
              </div>
            </div>
            <div class="card-body">
              <ul class="list-group list-group-flush">
                <li
                  v-for="sub in filteredSubjects"
                  :key="sub.id"
                  class="list-group-item d-flex justify-content-between align-items-center"
                >
                  {{ sub.name }}
                  <div>
                    <span class="badge bg-success rounded-pill me-2">
                      {{ sub.chapters?.length || 0 }} chapters
                    </span>
                    <button
                      class="btn btn-sm btn-outline-success me-1"
                      @click="editItem('subject', sub)"
                    >
                      <i class="bi bi-pencil"></i>
                    </button>
                    <button
                      class="btn btn-sm btn-outline-danger"
                      @click="deleteItem('subject', sub.id)"
                    >
                      <i class="bi bi-trash"></i>
                    </button>
                  </div>
                </li>
              </ul>
            </div>
          </div>
        </div>
        <div class="col-md-4">
          <div class="card">
            <div
              class="card-header bg-info text-white d-flex justify-content-between align-items-center"
            >
              <h5 class="mb-0">Chapters</h5>
              <div class="search-box">
                <input
                  type="text"
                  class="form-control form-control-sm"
                  placeholder="Search..."
                  v-model="chapterSearch"
                />
              </div>
            </div>
            <div class="card-body">
              <ul class="list-group list-group-flush">
                <li
                  v-for="chapter in filteredChapters"
                  :key="chapter.id"
                  class="list-group-item d-flex justify-content-between align-items-center"
                >
                  {{ chapter.name }}
                  <div>
                    <button
                      class="btn btn-sm btn-outline-info me-1"
                      @click="editItem('chapter', chapter)"
                    >
                      <i class="bi bi-pencil"></i>
                    </button>
                    <button
                      class="btn btn-sm btn-outline-danger"
                      @click="deleteItem('chapter', chapter.id)"
                    >
                      <i class="bi bi-trash"></i>
                    </button>
                  </div>
                </li>
              </ul>
            </div>
          </div>
        </div>
      </div>
    </div>
    <div v-else>
      <div class="position-absolute top-50 start-50 translate-middle">
        <div class="spinner-border text-primary" role="status">
          <span class="visually-hidden">Loading...</span>
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
                <select class="form-select" v-model="formData.qualId" required>
                  <option value="" disabled>Select a qualification</option>
                  <option
                    v-for="qual in Qualifications"
                    :key="qual.id"
                    :value="qual.id"
                  >
                    {{ qual.name }}
                  </option>
                </select>
                <label class="form-label mt-3">Subject Name</label>
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
                <select
                  class="form-select"
                  v-model="formData.subjectId"
                  required
                >
                  <option value="" disabled>Select a subject</option>
                  <option v-for="sub in Subjects" :key="sub.id" :value="sub.id">
                    {{ sub.name }}
                  </option>
                </select>
                <label class="form-label mt-3">Chapter Name</label>
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

    <!-- Confirmation Modal for Delete -->
    <div class="modal fade" id="deleteModal" tabindex="-1" aria-hidden="true">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">Confirm Delete</h5>
            <button
              type="button"
              class="btn-close"
              data-bs-dismiss="modal"
            ></button>
          </div>
          <div class="modal-body">
            <p>
              Are you sure you want to delete this item? This action cannot be
              undone.
            </p>
          </div>
          <div class="modal-footer">
            <button
              type="button"
              class="btn btn-secondary"
              data-bs-dismiss="modal"
            >
              Cancel
            </button>
            <button type="button" class="btn btn-danger" @click="confirmDelete">
              Delete
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, computed } from "vue";
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
  { type: "chapter", label: "Add Chapter", icon: "bi bi-file-text" },
  { type: "quiz", label: "Manage Quizzes", icon: "bi bi-question-circle" },
];

const Qualifications = ref([]);
const Subjects = ref([]);
const Chapters = ref([]);
const currentForm = reactive({
  type: "",
  title: "",
  isEditing: false,
  editId: null,
});
const formData = reactive({
  name: "",
  description: "",
  qualId: "",
  subjectId: "",
});

// Search functionality
const qualificationSearch = ref("");
const subjectSearch = ref("");
const chapterSearch = ref("");

// Filtered lists using computed properties
const filteredQualifications = computed(() => {
  if (!qualificationSearch.value) return Qualifications.value;
  return Qualifications.value.filter((qual) =>
    qual.name.toLowerCase().includes(qualificationSearch.value.toLowerCase())
  );
});

const filteredSubjects = computed(() => {
  if (!subjectSearch.value) return Subjects.value;
  return Subjects.value.filter((sub) =>
    sub.name.toLowerCase().includes(subjectSearch.value.toLowerCase())
  );
});

const filteredChapters = computed(() => {
  if (!chapterSearch.value) return Chapters.value;
  return Chapters.value.filter((chapter) =>
    chapter.name.toLowerCase().includes(chapterSearch.value.toLowerCase())
  );
});

let formModal;
let deleteModal;
let deleteItemInfo = { type: "", id: null };

const fetchData = async () => {
  try {
    const [qualRes, subjectRes, chapterRes] = await Promise.all([
      fetch(`${apiBase}/all/qualifications`).then((res) => res.json()),
      fetch(`${apiBase}/all/subjects`).then((res) => res.json()),
      fetch(`${apiBase}/all/chapters`).then((res) => res.json()),
    ]);
    Qualifications.value = qualRes;
    Subjects.value = subjectRes;
    Chapters.value = chapterRes;
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
  currentForm.isEditing = false;
  currentForm.editId = null;

  // Reset form data
  formData.name = "";
  formData.description = "";
  formData.qualId = "";
  formData.subjectId = "";

  if (!formModal) {
    formModal = new Modal(document.getElementById("formModal"));
  }
  formModal.show();
};

const editItem = (type, item) => {
  currentForm.type = type;
  currentForm.title = `Edit ${type.charAt(0).toUpperCase() + type.slice(1)}`;
  currentForm.isEditing = true;
  currentForm.editId = item.id;

  // Populate form data
  formData.name = item.name;
  formData.description = item.description || "";

  if (type === "subject") {
    // Use qualification_id from the item object
    formData.qualId = item.qualification_id;
    console.log("Setting qualId for edit:", item.qualification_id);
  } else if (type === "chapter") {
    // Use subject_id from the item object
    formData.subjectId = item.subject_id;
    console.log("Setting subjectId for edit:", item.subject_id);
  }

  if (!formModal) {
    formModal = new Modal(document.getElementById("formModal"));
  }
  formModal.show();
};

const deleteItem = (type, id) => {
  deleteItemInfo.type = type;
  deleteItemInfo.id = id;

  if (!deleteModal) {
    deleteModal = new Modal(document.getElementById("deleteModal"));
  }
  deleteModal.show();
};

const confirmDelete = async () => {
  try {
    let endpoint = "";

    if (deleteItemInfo.type === "qualification") {
      endpoint = `delete/qualification/${deleteItemInfo.id}`;
    } else if (deleteItemInfo.type === "subject") {
      endpoint = `delete/subject/${deleteItemInfo.id}`;
    } else if (deleteItemInfo.type === "chapter") {
      endpoint = `delete/chapter/${deleteItemInfo.id}`;
    }

    const response = await fetch(`${apiBase}/${endpoint}`, {
      method: "DELETE",
    });

    if (!response.ok) {
      throw new Error("Network response was not ok");
    }

    // Refresh data after deletion
    await fetchData();
    deleteModal.hide();
  } catch (error) {
    console.error("Error deleting item:", error);
  }
};

const submitForm = async () => {
  try {
    let endpoint = "";
    let payload = {};
    let method = currentForm.isEditing ? "PUT" : "POST";

    if (currentForm.type === "qualification") {
      endpoint = currentForm.isEditing
        ? `update/qualification/${currentForm.editId}`
        : "add/qualification";
      payload = {
        name: formData.name,
        description: formData.description,
      };
    } else if (currentForm.type === "subject") {
      endpoint = currentForm.isEditing
        ? `update/subject/${currentForm.editId}`
        : "add/subject";
      payload = {
        name: formData.name,
        description: formData.description,
        qualId: formData.qualId,
      };
      console.log("Subject payload:", payload);
    } else if (currentForm.type === "chapter") {
      endpoint = currentForm.isEditing
        ? `update/chapter/${currentForm.editId}`
        : "add/chapter";
      payload = {
        name: formData.name,
        description: formData.description,
        subjectId: formData.subjectId,
      };
      console.log("Chapter payload:", payload);
    }

    // API request
    const response = await fetch(`${apiBase}/${endpoint}`, {
      method: method,
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(payload),
    });

    if (!response.ok) {
      throw new Error("Network response was not ok");
    }

    // Refresh data
    await fetchData();
    formModal.hide();
  } catch (error) {
    console.error("Error submitting data:", error);
  }
};

onMounted(() => {
  fetchData();
});
</script>

<style scoped>
.spinner-border {
  width: 3rem;
  height: 3rem;
}

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

.search-box {
  width: 200px;
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
