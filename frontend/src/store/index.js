// store/index.js
import { createStore } from "vuex";

export default createStore({
  state: {
    isDarkMode: JSON.parse(localStorage.getItem("isDarkMode")) || false,
    user: {
      token: null,
      roles: [],
      loggedIn: false,
      id: null,
      fullName: "",
    },
    toasts: [],
    quiz: {
      quizState: null, // Stores current quiz state during runtime
      quizResults: null, // Stores quiz results for the results page
    },
    activeSection: "overview",
  },

  mutations: {
    // Dark mode
    toggleDarkMode(state, value = null) {
      if (value !== null) {
        state.isDarkMode = value;
      } else {
        state.isDarkMode = !state.isDarkMode;
      }
      localStorage.setItem("isDarkMode", JSON.stringify(state.isDarkMode));
      console.log("Dark mode toggled:", state.isDarkMode);
    },

    // User state
    setUser(state, user) {
      state.user = {
        token: user.token,
        roles: user.roles || [],
        loggedIn: true,
        id: user.id,
        fullName: user.fullname || "Guest",
      };

      const data = localStorage.getItem("user");
      if (!data) {
        localStorage.setItem("user", JSON.stringify(user));
        console.log("User added successfully!");
      }
    },

    removeUser(state) {
      state.user = {
        token: null,
        roles: [],
        loggedIn: false,
        id: null,
        fullName: "",
      };
      localStorage.removeItem("user");
      console.log("User removed!");
    },

    // Toast notifications
    ADD_TOAST(state, toast) {
      state.toasts.push(toast);
    },

    REMOVE_TOAST(state, index) {
      state.toasts.splice(index, 1);
    },

    // Active section
    setActiveSection(state, section) {
      state.activeSection = section;
    },

    // Quiz state - only updates the runtime state in Vuex
    // The component handles localStorage persistence
    setQuizState(state, quizState) {
      console.log("Updating quiz state in Vuex store");
      state.quiz.quizState = quizState;
    },

    clearQuizState(state) {
      console.log("Clearing quiz state from Vuex store");
      state.quiz.quizState = null;
    },

    // Quiz results - used to pass data to the results page
    setQuizResults(state, results) {
      console.log("Saving quiz results to Vuex store");
      state.quiz.quizResults = results;
    },

    clearQuizResults(state) {
      console.log("Clearing quiz results from Vuex store");
      state.quiz.quizResults = null;
    },
  },

  actions: {
    // User authentication
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
      try {
        const user = JSON.parse(localStorage.getItem("user"));
        if (user && user.token) {
          commit("setUser", user);
        }
      } catch (error) {
        console.error("Error initializing user:", error);
      }
    },

    // Toast notifications
    addToast({ commit }, toast) {
      commit("ADD_TOAST", toast);
      setTimeout(() => {
        commit("REMOVE_TOAST", 0);
      }, 5000);
    },

    removeToast({ commit }, index) {
      commit("REMOVE_TOAST", index);
    },

    // Active section
    updateActiveSection({ commit }, section) {
      commit("setActiveSection", section);
    },

    // Quiz state management
    saveQuizState({ commit }, quizState) {
      commit("setQuizState", quizState);
    },

    saveQuizResults({ commit }, results) {
      commit("setQuizResults", results);
    },

    // Check if a quiz is in progress by looking at localStorage
    checkInProgressQuiz(_, { quizId, userId }) {
      const key = `quizState_${quizId}_${userId || "guest"}`;
      try {
        const savedState = JSON.parse(localStorage.getItem(key));
        if (!savedState) return false;

        // Check if the saved state is still valid (not expired)
        const currentTime = new Date().getTime();
        const savedTime = savedState.timestamp;
        const elapsedSeconds = Math.floor((currentTime - savedTime) / 1000);

        // If the elapsed time is less than the quiz duration, the quiz is still valid
        return elapsedSeconds < savedState.duration * 60;
      } catch (error) {
        console.error("Error checking in-progress quiz:", error);
        return false;
      }
    },

    // Load quiz state from localStorage
    loadQuizState({ commit }, { quizId, userId }) {
      const key = `quizState_${quizId}_${userId || "guest"}`;
      try {
        const savedState = JSON.parse(localStorage.getItem(key));
        if (savedState) {
          commit("setQuizState", savedState);
          return savedState;
        }
      } catch (error) {
        console.error("Error loading quiz state:", error);
      }
      return null;
    },

    // Clear quiz state from localStorage
    clearSavedQuizState(_, { quizId, userId }) {
      const key = `quizState_${quizId}_${userId || "guest"}`;
      try {
        localStorage.removeItem(key);
        console.log("Cleared saved quiz state from localStorage:", key);
      } catch (error) {
        console.error("Error clearing saved quiz state:", error);
      }
    },
  },

  getters: {
    toasts: (state) => state.toasts,
    user: (state) => state.user,
    isDarkMode: (state) => state.isDarkMode,
    activeSection: (state) => state.activeSection,
    getQuizState: (state) => state.quiz?.quizState || {},
    getQuizResults: (state) => state.quiz?.quizResults || {},
    // New getter to check if there are quiz results available
    hasQuizResults: (state) => !!state.quiz?.quizResults,
  },
});
