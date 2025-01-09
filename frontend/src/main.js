import "bootstrap";
import "bootstrap/dist/css/bootstrap.min.css";
import "bootstrap-icons/font/bootstrap-icons.css";
import "@fortawesome/fontawesome-free/css/all.css";

import { createApp } from "vue";

import App from "./App.vue";
import router from "./router";
import store from "./store";
import ObserveDirective from "./directives/objerve";

const app = createApp(App);

app.directive("observe", ObserveDirective);

// Use router and store
app.use(store).use(router);

// Mount the app
app.mount("#app");
