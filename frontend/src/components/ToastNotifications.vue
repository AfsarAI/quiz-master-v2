<template>
  <div
    v-for="(toast, index) in toasts"
    :key="index"
    class="toast-container position-fixed top-0 start-50 translate-middle-x p-3"
    style="z-index: 1055"
  >
    <div
      :class="[
        'toast',
        'align-items-center',
        'text-white',
        'border-0',
        'show',
        toastClasses(toast.type),
      ]"
      role="alert"
      aria-live="assertive"
      aria-atomic="true"
    >
      <div class="d-flex align-items-center w-100">
        <div class="toast-icon me-3">
          <i :class="iconClass(toast.type)"></i>
        </div>
        <div class="toast-body flex-grow-1 text-center">
          {{ toast.message }}
        </div>
        <button
          type="button"
          class="btn-close ms-3"
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

    const removeToast = (index) => {
      store.dispatch("removeToast", index);
    };

    const toastClasses = (type) => {
      const colors = {
        success: "glass-success",
        error: "glass-error",
        danger: "glass-danger",
        warning: "glass-warning",
        info: "glass-info",
      };
      return colors[type] || "glass-default";
    };

    const iconClass = (type) => {
      const icons = {
        success: "bi bi-check-circle-fill",
        error: "bi bi-exclamation-circle-fill",
        danger: "bi bi-x-circle-fill",
        warning: "bi bi-exclamation-triangle-fill",
        info: "bi bi-info-circle-fill",
      };
      return icons[type] || "bi bi-bell-fill";
    };

    return { toasts, removeToast, toastClasses, iconClass };
  },
};
</script>

<style scoped>
.toast-container {
  animation: slideInPop 0.8s cubic-bezier(0.68, -0.55, 0.27, 1.55),
    fadeOut 0.5s ease-in-out 4s forwards;
}

.toast {
  display: flex;
  align-items: center;
  padding: 8px 16px;
  border-radius: 12px;
  backdrop-filter: blur(16px);
  background-color: rgba(0, 0, 0, 0.7);
  border: 1px solid rgba(255, 255, 255, 0.3);
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);
  min-width: 220px;
  max-width: 300px;
}

.glass-success {
  background-color: rgba(40, 167, 69, 0.7);
}
.glass-error {
  background-color: rgba(220, 53, 69, 0.7);
}
.glass-danger {
  background-color: rgba(220, 53, 69, 0.7);
}
.glass-warning {
  background-color: rgba(255, 193, 7, 0.7);
}
.glass-info {
  background-color: rgba(23, 162, 184, 0.7);
}
.glass-default {
  background-color: rgba(108, 117, 125, 0.7);
}

.toast-icon i {
  font-size: 20px;
}

.toast-body {
  font-size: 12px;
}

.btn-close {
  opacity: 0.8;
}

@keyframes slideInPop {
  0% {
    transform: translateY(-100px) translateX(-50%) scale(0.8);
    opacity: 0;
  }
  60% {
    transform: translateY(10px) translateX(-50%) scale(1.1);
    opacity: 1;
  }
  100% {
    transform: translateY(0) translateX(-50%) scale(1);
    opacity: 1;
  }
}

@keyframes fadeOut {
  to {
    transform: translateY(40px) translateX(-50%);
    opacity: 0;
  }
}
</style>
