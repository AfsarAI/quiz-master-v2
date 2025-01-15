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
    },
    setUser(state, user) {
      if (user) {
        state.user = {
          auth_token: user.token,
          roles: user.roles || [],
          loggedIn: true,
          id: user.id,
          fullName: user.fullname || "Guest",
        };
        localStorage.setItem("user", JSON.stringify(user));
      } else {
        state.user = {
          auth_token: null,
          roles: [],
          loggedIn: false,
          id: null,
          fullName: "",
        };
        localStorage.removeItem("user");
      }
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
      commit("setUser", null);
    },
    initializeUser({ commit }) {
      const user = JSON.parse(localStorage.getItem("user"));
      commit("setUser", user);
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
