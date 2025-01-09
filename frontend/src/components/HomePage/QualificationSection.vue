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
