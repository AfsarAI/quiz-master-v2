import { createStore } from "vuex";

export default createStore({
  state: {
    // Correctly initialize dark mode with 'isDarkMode' key
    isDarkMode: JSON.parse(localStorage.getItem("isDarkMode")) || false,
    user: {
      auth_token: null,
      roles: [],
      loggedIn: false,
      id: null,
      fullName: "",
    },
    toasts: [],
  },
  mutations: {
    toggleDarkMode(state, value = null) {
      if (value !== null) {
        state.isDarkMode = value;
      } else {
        state.isDarkMode = !state.isDarkMode;
      }
      localStorage.setItem("isDarkMode", JSON.stringify(state.isDarkMode)); // Use correct key
    },

    setUser(state) {
      try {
        const user = JSON.parse(localStorage.getItem("user"));
        if (user) {
          state.user = {
            auth_token: user["token"],
            roles: user["roles"] || [],
            loggedIn: true,
            id: user["id"],
            fullName: user["fullname"] || "Guest",
          };
        }
      } catch {
        console.warn("User not logged in or data is invalid.");
      }
    },

    logout(state) {
      state.user = {
        auth_token: null,
        roles: [],
        loggedIn: false,
        id: null,
        fullName: "",
      };
      localStorage.removeItem("user");
    },

    ADD_TOAST(state, toast) {
      state.toasts.push(toast);
    },

    REMOVE_TOAST(state, index) {
      state.toasts.splice(index, 1);
    },
  },
  actions: {
    initializeUser({ commit }) {
      commit("setUser");
    },

    addToast({ commit }, toast) {
      commit("ADD_TOAST", toast);
      setTimeout(() => {
        commit("REMOVE_TOAST", 0);
      }, 5000);
    },

    removeToast({ commit }, index) {
      commit("REMOVE_TOAST", index);
    },
  },
  getters: {
    toasts: (state) => state.toasts,
    user: (state) => state.user,
    isDarkMode: (state) => state.isDarkMode,
  },
});
