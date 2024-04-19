import { createApp } from "vue";
import { FontAwesomeIcon } from "@fortawesome/vue-fontawesome";
import { library } from "@fortawesome/fontawesome-svg-core";
import { faCommentDots, faShareFromSquare, faClose, faPaperPlane, faWindowMaximize, faWindowMinimize } from "@fortawesome/free-solid-svg-icons";

library.add(faCommentDots, faShareFromSquare, faClose, faPaperPlane, faWindowMaximize, faWindowMinimize );

import { createPinia } from "pinia";
import App from "./App.vue";

import mitt from 'mitt';
const emitter = mitt();

const pinia = createPinia();
const app = createApp(App);
app.config.globalProperties.emitter = emitter;
app.use(pinia);
app.component("font-awesome-icon", FontAwesomeIcon)
app.mount("#app");
