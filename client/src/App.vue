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
              <!-- Loading
              <div class="chat-logs" v-show="!store.messages.length" style="text-align: center">
                <label>
                  <img src="@/assets/X-1.png" class="pulse" style="width: 65px;"><br>
                  Connecting...</label>
              </div>
               v-show="store.messages.length"
              -->
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

    <!--
        <transition name="fade" mode="out-in">
          <section class="main" v-show="store.messages.length">
            <ul class="chat-list">
              <li
                  class="chat"
                  v-for="chat in store.messages"
                  :key="chat.threadId"
                  :class="chat.role"
              >
                <div class="view ">
                  <div style="display: inline-block; vertical-align: top; text-align: right; width: 6%;">
                    <img v-show="chat.role != 'user'" src="@/assets/X-1.png" style="width: 25px; background-color: #fff; padding: 6px; border-radius: 180px; filter: drop-shadow(1px 2px 3px rgb(221, 221, 221)); vertical-align: top;">
                  </div>
                  <div style="display: inline-block; width: 85%; padding: 0 10px;">
                    <label>
                      <strong style="font-size: 14px; font-weight: bold;" v-show="chat.role != 'user'">Assistant</strong>
                      <strong style="font-size: 14px; font-weight: bold;"
                              v-show="chat.role === 'user'">You</strong><br>{{ chat.output }}</label>
                  </div>
                </div>
              </li>
              <li
                  class="chat"
                  v-show="store.loading"
              >
                <div style="display: inline-block; vertical-align: top; text-align: right; width: 6%;">
                  <img src="@/assets/X-1.png" class="pulse" style="width: 25px; background-color: #fff; padding: 6px; border-radius: 180px; filter: drop-shadow(1px 2px 3px rgb(221, 221, 221)); vertical-align: top;">
                </div>
                <div style="display: inline-block; width: 85%; padding: 0 10px;">
                  <strong style="font-size: 14px; font-weight: bold; opacity: .25;">Assistant</strong><br/>
                </div>
              </li>
            </ul>

          </section>
        </transition>
        <transition name="fade" mode="out-in">
          <section class="footer">
            <div style="text-align: right;width: 75%; display: inline-block">
              <input v-model="value" style=""/>

            </div>
            <div style=" width: 25%; display: inline-block; text-align: left;">
              <button type="submit" v-show="!store.loading" style="margin-left: 10px" @click="addMessage">Submit</button>
              <button type="submit" v-show="store.loading" style="opacity: 0.7;margin-left: 10px" disabled="true">Submit
              </button>
            </div>
          </section>
        </transition>
        <transition name="fade" mode="out-in">
          <section class="main" v-show="!store.messages.length">

            <ul class="chat-loading">
              <li>
                <div class="view">
                  <label>
                    <img src="@/assets/X-1.png" style="width: 65px;"><br>
                    Connecting...</label>
                </div>
              </li>
            </ul>
          </section>
        </transition>
        !-->
  </section>
</template>

<style scoped></style>
