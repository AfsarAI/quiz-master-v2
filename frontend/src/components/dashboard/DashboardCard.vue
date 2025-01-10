<template>
  <div class="card h-100 border-0 shadow-sm">
    <div class="card-body text-center">
      <i :class="`bi ${icon} fs-1 text-primary mb-3`"></i>
      <h3 class="card-title h5">{{ title }}</h3>
      <p class="card-text display-4">{{ value }}</p>
    </div>
  </div>
</template>

<script>
export default {
  name: "DashboardCard",
  props: {
    title: {
      type: String,
      required: true,
    },
    value: {
      type: [String, Number],
      required: true,
    },
    icon: {
      type: String,
      required: true,
    },
  },
};
</script>

<style scoped>
.card {
  transition: all 0.3s ease;
}

.card:hover {
  transform: translateY(-5px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1) !important;
}
</style>
