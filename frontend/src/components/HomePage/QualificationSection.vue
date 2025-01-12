<template>
  <section class="qualification-section section py-5">
    <div class="container">
      <h2 class="text-center mb-5">Who Can Benefit?</h2>
      <div class="row g-4">
        <div class="col-md-3" v-for="level in educationLevels" :key="level.id">
          <div class="card h-100 border-0 shadow-sm">
            <div class="card-body text-center">
              <i :class="level.icon + ' fs-1 text-primary mb-3'"></i>
              <h3 class="card-title h5">{{ level.title }}</h3>
              <p class="card-text">{{ level.description }}</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script>
export default {
  name: "QualificationSection",
  setup() {
    const educationLevels = [
      {
        id: 1,
        title: "School Students",
        description: "From elementary to high school",
        icon: "bi bi-mortarboard",
      },
      {
        id: 2,
        title: "College Students",
        description: "Undergraduate and postgraduate",
        icon: "bi bi-book",
      },
      {
        id: 3,
        title: "Professionals",
        description: "Skill enhancement and certifications",
        icon: "bi bi-briefcase",
      },
      {
        id: 4,
        title: "Lifelong Learners",
        description: "For curious minds of all ages",
        icon: "bi bi-lightbulb",
      },
    ];

    return {
      educationLevels,
    };
  },
};
</script>

<style scoped>
h2 {
  color: #4361ee;
}

[data-bs-theme="light"] .card {
  padding: 20px;
  border-radius: 8px;
  background-color: #f4f4f4;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  text-align: center;
  transition: transform 0.3s ease, box-shadow 0.3s ease,
    background-color 0.3s ease, color 0.3s ease;
}
[data-bs-theme="light"] .card:hover {
  transform: scale(1.05); /* Slight zoom */
  box-shadow: 0 8px 15px rgba(0, 0, 0, 0.2); /* Shadow increase */
  background: linear-gradient(135deg, #3a0ca3, #4361ee, #4cc9f0);
  color: white; /* Text color change */
}

[data-bs-theme="dark"] .card {
  padding: 20px;
  border-radius: 8px;
  background-color: #34495e;
  box-shadow: 0 4px 6px rgb(255, 254, 254);
  text-align: center;
  transition: transform 0.3s ease, box-shadow 0.3s ease,
    background-color 0.3s ease, color 0.3s ease;
}
[data-bs-theme="dark"] .card:hover {
  transform: scale(1.05); /* Slight zoom */
  box-shadow: 0 8px 15px rgb(255, 254, 254); /* Shadow increase */
  background: linear-gradient(135deg, #1a0029, #2b0057, #3a0085);
  color: white; /* Text color change */
}
</style>
