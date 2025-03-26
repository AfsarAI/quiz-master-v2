<template>
  <div class="admin-quizzes container-fluid py-4">
    <h2 class="mb-4">Manage Quizzes</h2>

    <div class="row mb-4">
      <div class="col-md-6">
        <button class="btn btn-primary w-100" @click="openQuizForm">
          <i class="bi bi-plus-circle me-2"></i>Add New Quiz
        </button>
      </div>
      <div class="col-md-6">
        <input
          v-model="searchQuery"
          type="text"
          class="form-control"
          placeholder="Search quizzes..."
        />
      </div>
    </div>

    <div class="card">
      <div class="card-header bg-primary text-white">
        <h5 class="mb-0">Quiz List</h5>
      </div>
      <div class="card-body">
        <div class="table-responsive">
          <table class="table table-hover">
            <thead>
              <tr>
                <th>Title</th>
                <th>Quiz Type</th>
                <th>Questions</th>
                <th>Date Created</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="quiz in filteredQuizzes" :key="quiz.id">
                <td>{{ quiz.title }}</td>
                <td>{{ quiz.quiz_type }}</td>
                <td>{{ quiz.questions?.length || 0 }}</td>
                <td>{{ quiz.dateCreated }}</td>
                <td>
                  <button
                    class="btn btn-sm btn-outline-primary me-2"
                    @click="editQuiz(quiz)"
                  >
                    <i class="bi bi-pencil"></i> Edit
                  </button>
                  <button
                    class="btn btn-sm btn-outline-danger"
                    @click="deleteQuiz(quiz)"
                  >
                    <i class="bi bi-trash"></i> Delete
                  </button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>

    <!-- Quiz Form Modal -->
    <div
      class="modal fade"
      id="quizFormModal"
      tabindex="-1"
      aria-labelledby="quizFormModalLabel"
      aria-hidden="true"
    >
      <div class="modal-dialog modal-lg">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title" id="quizFormModalLabel">
              {{ isEditing ? "Edit Quiz" : "Add New Quiz" }}
            </h5>
            <button
              type="button"
              class="btn-close"
              data-bs-dismiss="modal"
              aria-label="Close"
            ></button>
          </div>
          <div class="modal-body">
            <form @submit.prevent="submitQuizForm">
              <div class="mb-3">
                <label for="quizTitle" class="form-label">Quiz Title</label>
                <input
                  type="text"
                  class="form-control"
                  id="quizTitle"
                  v-model="quizForm.title"
                  required
                />
              </div>
              <div class="mb-3">
                <label for="quizType" class="form-label">Quiz Type</label>
                <select
                  class="form-select"
                  id="quizType"
                  v-model="quizForm.quizType"
                  required
                >
                  <option value="" disabled hidden>Select a Quiz Type</option>
                  <option value="whole">Whole Syllabus</option>
                  <option value="subject">Subject Wise</option>
                  <option value="chapter">Chapter Wise</option>
                </select>
              </div>

              <!-- Subject & Chapter Select -->
              <div
                class="mb-3"
                v-if="
                  quizForm.quizType === 'subject' ||
                  quizForm.quizType === 'chapter'
                "
              >
                <label class="form-label mt-2">Subject</label>
                <select
                  class="form-select"
                  id="subjectId"
                  v-model="quizForm.subjectId"
                  required
                >
                  <option :value="null" disabled hidden>
                    Select a Subject
                  </option>
                  <option v-for="sub in Subjects" :key="sub.id" :value="sub.id">
                    {{ sub.name }}
                  </option>
                </select>
              </div>
              <div class="mb-3" v-if="quizForm.quizType === 'chapter'">
                <label class="form-label mt-2">Chapter</label>
                <select
                  class="form-control"
                  v-model="quizForm.chapterId"
                  required
                >
                  <option :value="null" disabled hidden>
                    Select a Chapter
                  </option>
                  <option
                    v-for="chap in filteredChapters"
                    :key="chap.id"
                    :value="chap.id"
                  >
                    {{ chap.name }}
                  </option>
                </select>
              </div>
              <div class="mb-3">
                <label class="form-label">Questions</label>
                <div
                  v-for="(question, index) in quizForm.questions"
                  :key="index"
                  class="card mb-3"
                >
                  <div class="card-body">
                    <div class="mb-3">
                      <label :for="'question' + index" class="form-label"
                        >Question {{ index + 1 }}</label
                      >
                      <input
                        type="text"
                        class="form-control"
                        :id="'question' + index"
                        v-model="question.text"
                        required
                      />
                    </div>
                    <div
                      class="mb-3"
                      v-for="(option, optionIndex) in question.options"
                      :key="optionIndex"
                    >
                      <div class="input-group">
                        <div class="input-group-text">
                          <input
                            type="radio"
                            :name="'correctAnswer' + index"
                            :id="'option' + index + optionIndex"
                            :value="optionIndex"
                            v-model="question.correctAnswer"
                            required
                          />
                        </div>
                        <input
                          type="text"
                          class="form-control"
                          :id="'optionText' + index + optionIndex"
                          v-model="option.text"
                          :placeholder="'Option ' + (optionIndex + 1)"
                          required
                        />
                      </div>
                    </div>
                    <button
                      type="button"
                      class="btn btn-danger btn-sm"
                      @click="removeQuestion(index)"
                    >
                      Remove Question
                    </button>
                  </div>
                </div>
                <button
                  type="button"
                  class="btn btn-secondary"
                  @click="addQuestion"
                >
                  Add Question
                </button>
              </div>
              <button type="submit" class="btn btn-primary">
                {{ isEditing ? "Update Quiz" : "Create Quiz" }}
              </button>
            </form>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
<script setup>
import { ref, reactive, computed, onMounted, watch } from "vue";
import { Modal } from "bootstrap";

const apiBaseUrl = "http://localhost:5000/api/admin/dashboard"; // Backend API ka URL

const quizzes = ref([]);
const Subjects = ref([]);
const Chapters = ref([]);
const searchQuery = ref("");
const isEditing = ref(false);
const quizForm = reactive({
  id: null,
  title: "",
  quizType: "",
  subjectId: null,
  chapterId: null,
  questions: [
    {
      text: "",
      options: [{ text: "" }, { text: "" }, { text: "" }, { text: "" }],
      correctAnswer: null,
    },
  ],
});

let quizFormModal;

// API se quizzes fetch karna
const fetchQuizzes = async () => {
  try {
    const response = await fetch(`${apiBaseUrl}/all/quizzes`);
    if (!response.ok) throw new Error("Failed to fetch quizzes");
    quizzes.value = await response.json();
  } catch (error) {
    console.error("Error fetching quizzes:", error);
  }
};

const fetchSubjectsAndChapters = async () => {
  try {
    const subjectsRes = await fetch(`${apiBaseUrl}/all/subjects`);
    Subjects.value = await subjectsRes.json();
    console.log("Subjects fetched:", Subjects.value);

    const chaptersRes = await fetch(`${apiBaseUrl}/all/chapters`);
    Chapters.value = await chaptersRes.json();
    console.log("Chapters fetched:", Chapters.value);
  } catch (error) {
    console.error("Error fetching subjects and chapters:", error);
  }
};

const filteredChapters = computed(() => {
  if (!quizForm.subjectId) return Chapters.value; // Agar subject select nahi hai, sabhi chapters dikhao
  return Chapters.value.filter(
    (chap) => chap.subject_id === quizForm.subjectId
  );
});

watch(
  () => quizForm.chapterId,
  (newChapterId) => {
    const selectedChapter = Chapters.value.find(
      (chap) => chap.id === newChapterId
    );
    if (selectedChapter) {
      quizForm.subjectId = selectedChapter.subject_id;
    }
  }
);

// Quiz add/edit modal open karna
const openQuizForm = () => {
  isEditing.value = false;
  resetForm();
  if (!quizFormModal) {
    quizFormModal = new Modal(document.getElementById("quizFormModal"));
  }
  quizFormModal.show();
};

// Quiz edit karna
const editQuiz = (quiz) => {
  isEditing.value = true;
  Object.assign(quizForm, JSON.parse(JSON.stringify(quiz))); // Deep copy to avoid mutation
  if (!quizFormModal) {
    quizFormModal = new Modal(document.getElementById("quizFormModal"));
  }
  quizFormModal.show();
};

// Quiz delete karna
const deleteQuiz = async (quizId) => {
  if (confirm("Are you sure you want to delete this quiz?")) {
    try {
      const response = await fetch(`${apiBaseUrl}/${quizId}`, {
        method: "DELETE",
      });
      if (!response.ok) throw new Error("Failed to delete quiz");
      quizzes.value = quizzes.value.filter((q) => q.id !== quizId);
    } catch (error) {
      console.error("Error deleting quiz:", error);
    }
  }
};

// Quiz submit karna (Add/Edit)
const submitQuizForm = async () => {
  const method = isEditing.value ? "PUT" : "POST";
  const url = isEditing.value
    ? `${apiBaseUrl}/${quizForm.id}`
    : `${apiBaseUrl}/add/quiz`;

  try {
    const response = await fetch(url, {
      method: method,
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        title: quizForm.title,
        quizType: quizForm.quizType,
        questions: quizForm.questions,
      }),
    });

    if (!response.ok) throw new Error("Failed to save quiz");

    const savedQuiz = await response.json();
    if (isEditing.value) {
      const index = quizzes.value.findIndex((q) => q.id === savedQuiz.id);
      quizzes.value[index] = savedQuiz;
    } else {
      quizzes.value.push(savedQuiz);
    }

    quizFormModal.hide();
    resetForm();
  } catch (error) {
    console.error("Error saving quiz:", error);
  }
};

// Form reset karna
const resetForm = () => {
  quizForm.id = null;
  quizForm.title = "";
  quizForm.quizType = "";
  quizForm.questions = [
    {
      text: "",
      options: [{ text: "" }, { text: "" }, { text: "" }, { text: "" }],
      correctAnswer: null,
    },
  ];
};

// Naya question add karna
const addQuestion = () => {
  quizForm.questions.push({
    text: "",
    options: [{ text: "" }, { text: "" }, { text: "" }, { text: "" }],
    correctAnswer: null,
  });
};

// Question remove karna
const removeQuestion = (index) => {
  quizForm.questions.splice(index, 1);
};

// #fetching api during page load
onMounted(async () => {
  await fetchQuizzes();
  await fetchSubjectsAndChapters();
});

// Search filter
const filteredQuizzes = computed(() => {
  return quizzes.value.filter(
    (quiz) =>
      quiz.title
        ?.toLowerCase()
        .includes(searchQuery.value?.toLowerCase() || "") ||
      quiz.quiz_type
        ?.toLowerCase()
        .includes(searchQuery.value?.toLowerCase() || "")
  );
});
</script>

<style scoped>
.admin-quizzes {
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
[data-bs-theme="dark"] .modal-content {
  background-color: #2c3e50;
  color: #ecf0f1;
}

[data-bs-theme="dark"] .card-header {
  background-color: #34495e;
}

[data-bs-theme="dark"] .table {
  color: #ecf0f1;
}

[data-bs-theme="dark"] .table-hover tbody tr:hover {
  background-color: #34495e;
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

[data-bs-theme="dark"] .input-group-text {
  background-color: #4a6278;
  color: #ecf0f1;
  border-color: #4a6278;
}
</style>
