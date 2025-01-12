<template>
  <div
    v-for="(toast, index) in toasts"
    :key="index"
    class="toast-container position-fixed bottom-0 end-0 p-3"
    style="z-index: 1055"
  >
    <div
      v-for="(toast, index) in toasts"
      :key="index"
      class="toast align-items-center text-bg-{{ toast.type }} border-0 show"
      role="alert"
      aria-live="assertive"
      aria-atomic="true"
    >
      <div class="d-flex">
        <div class="toast-body">
          {{ toast.message }}
        </div>
        <button
          type="button"
          class="btn-close me-2 m-auto"
          data-bs-dismiss="toast"
          aria-label="Close"
          @click="removeToast(index)"
        ></button>
      </div>
    </div>
  </div>
</template>

<script>
import { computed } from "vue";
import { useStore } from "vuex";

export default {
  name: "ToastNotifications",
  setup() {
    const store = useStore();

    const toasts = computed(() => store.getters.toasts);

    const addToast = (message, type = "success") => {
      store.dispatch("addToast", { message, type });
    };

    const removeToast = (index) => {
      store.dispatch("removeToast", index);
    };

    return { toasts, addToast, removeToast };
  },
};
</script>

<style scoped>
.toast-container {
  position: fixed;
  bottom: 20px;
  right: 20px;
  background-color: #333;
  color: #fff;
  padding: 10px 20px;
  border-radius: 5px;
  z-index: 1055; /* Ensure this is above other elements */
}
</style>
