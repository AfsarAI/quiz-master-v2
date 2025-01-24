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
                <th>Category</th>
                <th>Questions</th>
                <th>Date Created</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="quiz in filteredQuizzes" :key="quiz.id">
                <td>{{ quiz.title }}</td>
                <td>{{ quiz.category }}</td>
                <td>{{ quiz.questionCount }}</td>
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
                <label for="quizCategory" class="form-label">Category</label>
                <select
                  class="form-select"
                  id="quizCategory"
                  v-model="quizForm.category"
                  required
                >
                  <option value="">Select a category</option>
                  <option value="Mathematics">Mathematics</option>
                  <option value="Science">Science</option>
                  <option value="History">History</option>
                  <option value="Literature">Literature</option>
                  <option value="Geography">Geography</option>
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
import { ref, reactive, computed } from "vue";
import { Modal } from "bootstrap";

const quizzes = ref([
  {
    id: 1,
    title: "Math Quiz 101",
    category: "Mathematics",
    questionCount: 10,
    dateCreated: "2023-05-01",
  },
  {
    id: 2,
    title: "Science Trivia",
    category: "Science",
    questionCount: 15,
    dateCreated: "2023-05-02",
  },
  {
    id: 3,
    title: "History Challenge",
    category: "History",
    questionCount: 20,
    dateCreated: "2023-05-03",
  },
]);

const searchQuery = ref("");
const isEditing = ref(false);
const quizForm = reactive({
  id: null,
  title: "",
  category: "",
  questions: [
    {
      text: "",
      options: [{ text: "" }, { text: "" }, { text: "" }, { text: "" }],
      correctAnswer: null,
    },
  ],
});

const filteredQuizzes = computed(() => {
  return quizzes.value.filter(
    (quiz) =>
      quiz.title.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
      quiz.category.toLowerCase().includes(searchQuery.value.toLowerCase())
  );
});

let quizFormModal;

const openQuizForm = () => {
  isEditing.value = false;
  resetForm();
  if (!quizFormModal) {
    quizFormModal = new Modal(document.getElementById("quizFormModal"));
  }
  quizFormModal.show();
};

const editQuiz = (quiz) => {
  isEditing.value = true;
  Object.assign(quizForm, quiz);
  if (!quizFormModal) {
    quizFormModal = new Modal(document.getElementById("quizFormModal"));
  }
  quizFormModal.show();
};

const deleteQuiz = (quiz) => {
  if (confirm(`Are you sure you want to delete "${quiz.title}"?`)) {
    quizzes.value = quizzes.value.filter((q) => q.id !== quiz.id);
  }
};

const submitQuizForm = () => {
  if (isEditing.value) {
    const index = quizzes.value.findIndex((q) => q.id === quizForm.id);
    if (index !== -1) {
      quizzes.value[index] = {
        ...quizForm,
        questionCount: quizForm.questions.length,
      };
    }
  } else {
    quizzes.value.push({
      id: quizzes.value.length + 1,
      ...quizForm,
      questionCount: quizForm.questions.length,
      dateCreated: new Date().toISOString().split("T")[0],
    });
  }
  quizFormModal.hide();
  resetForm();
};

const resetForm = () => {
  quizForm.id = null;
  quizForm.title = "";
  quizForm.category = "";
  quizForm.questions = [
    {
      text: "",
      options: [{ text: "" }, { text: "" }, { text: "" }, { text: "" }],
      correctAnswer: null,
    },
  ];
};

const addQuestion = () => {
  quizForm.questions.push({
    text: "",
    options: [{ text: "" }, { text: "" }, { text: "" }, { text: "" }],
    correctAnswer: null,
  });
};

const removeQuestion = (index) => {
  quizForm.questions.splice(index, 1);
};
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
