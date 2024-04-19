<script setup>

import {useChatStore} from "@/stores/chat";
import {socket} from "@/socket";
import VueMarkdown from 'vue-markdown-render'
const store = useChatStore();

function toggleChatWindow() {
  store.toggleChat();
}

function toggleExpanded() {
  store.toggleExpandedChat();
}

socket.off();
store.bindEvents();

let value = "";

// listne for enter button then trigger addMessage
document.addEventListener("keydown", function (event) {
  if (event.keyCode === 13) {
    addMessage();
  }
});


function addMessage() {
  const _value = value && value.trim();
  if (!_value) {
    return;
  }
  value = "";
  store.sendMessage(_value);
}

</script>

<template>
  <section class="todoapp" v-cloak>
    <header class="header"></header>
    <div id="body">
      <i class="fa-regular fa-comment-dots"></i>
      <section v-show="!store.showChat">
        <Transition :duration="550">
          <div id="chat-circle" class="btn btn-raised" @click="toggleChatWindow()">
            <div id="chat-overlay"></div>
            <font-awesome-icon :icon="['fas', 'comment-dots']" />
          </div>
        </Transition>
      </section>
      <section v-show="store.showChat">
        <Transition :duration="550">
          <div class="chat-box "  :class="store.expandedChat ? 'expanded' : 'compact'">
            <div class="chat-box-header">
              <span class="chat-box-toggle" @click="toggleChatWindow()"> <font-awesome-icon :icon="['fas', 'close']" /></span>
              <span class="chat-box-toggle" @click="toggleExpanded()" v-show="!store.expandedChat"> <font-awesome-icon :icon="['fas', 'window-maximize']" /></span>
              <span class="chat-box-toggle" @click="toggleExpanded()" v-show="store.expandedChat"> <font-awesome-icon :icon="['fas', 'window-minimize']" /></span>
            </div>
            <div class="chat-box-body">
              <div class="chat-box-overlay">
              </div>
                <div id="chat-logs" class="chat-logs">
                  <div
                      class="chat-msg"
                      v-for="chat in store.messages"
                      :key="chat.threadId"
                      :class="chat.role"
                  >
                    <span v-show="chat.role != 'user'" class="msg-avatar">
                      <img src="@/assets/X-1.png">
                    </span>
                   <vue-markdown class="cm-msg-text" :source="chat.output"></vue-markdown>

                  </div>
                  <div
                      class="chat-msg"
                      v-show="store.loading"
                  >
                    <span class="msg-avatar">
                      <img class="pulse" src="@/assets/logo.png">
                    </span>
                  </div>

                </div>
             <!--chat-log -->
            </div>
            <div class="chat-input">
                <input type="text" v-model="value"  id="chat-input"  :class="store.expandedChat ? 'expanded' : 'compact'" placeholder="Send a message..."/>
                <button  class="chat-submit" id="chat-submit" :class="store.expandedChat ? 'expanded' : 'compact'"  v-show="!store.loading"  @click="addMessage"> <font-awesome-icon :icon="['fas', 'paper-plane']" /></button>
                <button  class="chat-submit" id="chat-submit" :class="store.expandedChat ? 'expanded' : 'compact'"  v-show="store.loading" disabled style="opacity: 0.5"> <font-awesome-icon :icon="['fas', 'paper-plane']" /></button>
            </div>
          </div>
        </Transition>
      </section>
    </div>

  </section>
</template>

<style scoped></style>
