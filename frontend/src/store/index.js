import { createStore } from "vuex";

export default createStore({
  state: {
    isDarkMode: JSON.parse(localStorage.getItem("isDarkMode")) || false,
    user: {
      auth_token: null,
      roles: [],
      loggedIn: false,
      id: null,
      fullName: "",
    },
    toasts: [],
    activeSection: "overview",
  },
  mutations: {
    toggleDarkMode(state, value = null) {
      if (value !== null) {
        state.isDarkMode = value;
      } else {
        state.isDarkMode = !state.isDarkMode;
      }
      localStorage.setItem("isDarkMode", JSON.stringify(state.isDarkMode));
      const dark = localStorage.getItem("isDarkMode");
      console.log("darkmode!", dark);
    },
    setUser(state, user) {
      state.user = {
        auth_token: user.token,
        roles: user.roles || [],
        loggedIn: true,
        id: user.id,
        fullName: user.fullname || "Guest",
      };

      const data = localStorage.getItem("user");
      // If 'user' exists, print it; otherwise, print a message
      if (data) {
        console.log(
          "Don't need to store again!, User found in localStorage:",
          JSON.parse(data)
        );
      } else {
        localStorage.setItem("user", JSON.stringify(user));
        console.log("User Added Sussesfully!", data);
      }
    },
    removeUser(state) {
      state.user = {
        auth_token: null,
        roles: [],
        loggedIn: false,
        id: null,
        fullName: "",
      };
      localStorage.removeItem("user");
      console.log("User Removed!");
      // Check if 'user' key exists in localStorage
      const user = localStorage.getItem("user");

      // If 'user' exists, print it; otherwise, print a message
      if (user) {
        console.log("User found in localStorage:", JSON.parse(user));
      } else {
        console.log("No user found in localStorage.");
      }
      console.log(
        new Blob(Object.values(localStorage)).size / 1024 / 1024 + " MB"
      );
    },
    ADD_TOAST(state, toast) {
      state.toasts.push(toast);
    },
    REMOVE_TOAST(state, index) {
      state.toasts.splice(index, 1);
    },
    setActiveSection(state, section) {
      state.activeSection = section;
    },
  },
  actions: {
    login({ commit }, user) {
      if (user && user.token) {
        commit("setUser", user);
      } else {
        throw new Error("Invalid user data");
      }
    },
    logout({ commit }) {
      commit("removeUser");
    },
    initializeUser({ commit }) {
      const user = JSON.parse(localStorage.getItem("user"));
      console.log("userdata at init:", user);
      if (user && user.token) {
        commit("setUser", user);
      }
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
    updateActiveSection({ commit }, section) {
      commit("setActiveSection", section);
    },
  },
  getters: {
    toasts: (state) => state.toasts,
    user: (state) => state.user,
    isDarkMode: (state) => state.isDarkMode,
    activeSection: (state) => state.activeSection,
  },
});
