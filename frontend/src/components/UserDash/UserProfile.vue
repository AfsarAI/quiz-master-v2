<template>
  <div class="container my-5">
    <div v-if="loading" class="text-center my-5">
      <div class="spinner-border text-primary" role="status">
        <span class="visually-hidden">Loading...</span>
      </div>
      <p>Loading profile data...</p>
    </div>
    <div v-else class="row justify-content-center">
      <div class="col-md-8">
        <div class="card shadow-lg border-0">
          <div class="card-body">
            <div class="d-flex align-items-center">
              <img
                :src="user.profile_url || 'https://via.placeholder.com/150'"
                alt="Profile Picture"
                class="rounded-circle me-3"
                style="width: 120px; height: 120px; object-fit: cover"
              />
              <div>
                <h4 class="card-title">{{ user.fullname }}</h4>
                <p class="text-muted">{{ user.email }}</p>
              </div>
            </div>
            <hr />
            <div class="row">
              <div class="col-6">
                <p><strong>Date of Birth:</strong> {{ user.dob }}</p>
                <p><strong>Gender:</strong> {{ user.gender }}</p>
              </div>
              <div class="col-6">
                <p><strong>Phone:</strong> {{ user.phone }}</p>
                <p><strong>Address:</strong> {{ user.address }}</p>
              </div>
            </div>
            <hr />
            <div>
              <p><strong>Qualification:</strong> {{ user.qualification_id }}</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted } from "vue";
import { useStore } from "vuex";

export default {
  name: "UserProfile",
  setup() {
    const store = useStore();
    const user = ref({
      fullname: "",
      email: "",
      dob: "",
      gender: "",
      phone: "",
      address: "",
      qualification_id: "",
      profile_url: "",
    });
    const loading = ref(true);

    const userId = computed(() => store.state.user.id);
    const authToken = computed(() => store.state.user.auth_token);

    const fetchUserData = async () => {
      try {
        if (!userId.value || !authToken.value) {
          throw new Error("User ID or authentication token is missing!");
        }
        const response = await fetch(
          `http://127.0.0.1:5000/api/user/${userId.value}/data`,
          {
            headers: {
              "Authentication-Token": authToken.value,
              "Content-Type": "application/json",
            },
          }
        );
        console.log("saved!");
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();
        user.value = data;
        console.log("hiiiiii...");
        console.log(data);
      } catch (error) {
        console.error("Error fetching user data:", error);
        store.dispatch("addToast", {
          type: "error",
          message: "Failed to load user profile data.",
        });
      } finally {
        loading.value = false;
      }
    };

    onMounted(fetchUserData);

    return {
      user,
      loading,
    };
  },
};
</script>

<style scoped>
.card {
  background: #ffffff;
  border-radius: 15px;
}
.card-body {
  padding: 2rem;
}
.card-title {
  font-size: 1.5rem;
  font-weight: bold;
}
.text-muted {
  font-size: 0.9rem;
}
.spinner-border {
  width: 3rem;
  height: 3rem;
}
</style>
