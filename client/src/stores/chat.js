import {defineStore} from "pinia";
import {socket} from "@/socket";

export const useChatStore = defineStore("chat", {
    state: () => ({
        messages: [],
        threadId: null,
        responseTo: null,
        loading: true,
        showChat: false,
        expandedChat: false
    }),

    getters: {},

    actions: {
        toggleChat() {
            this.showChat = !this.showChat;
        },
        toggleExpandedChat() {
            this.expandedChat = !this.expandedChat;
        },
        sendMessage(message) {
            this.loading = true;
            this.messages.push({
                output: message,
                role: "user"
            });

            socket.emit("message", {
                input: message,
                threadId: this.threadId,
                responseTo: this.responseTo
            });
            // wait one second before sending the message
            setTimeout(() => {
                // scroll to the bottom of the element .chat-logs
                var objDiv = document.getElementById("chat-logs");
                objDiv.scrollTop = objDiv.scrollHeight;

            }, 500);
        },
        bindEvents() {

            this.threadId = document.cookie
                .split("; ")
                .find((row) => row.startsWith("_tid="))
                ?.split("=")[1];
            if (this.threadId == undefined) this.threadId = "NONE";


            socket.on("load_messages", (data) => {
                this.threadId = data.threadId;
                // save the threadId in a cookie
                document.cookie = `_tid=${data.threadId}; path=/; max-age=31536000`;
                this.responseTo = data.query;
                if (data.output != "") this.messages.push(data);

                var objDiv = document.getElementById("chat-logs");
                objDiv.scrollTop = objDiv.scrollHeight;

                this.loading = false;
            });

            socket.on("new_message", (data) => {
                this.threadId = data.threadId;
                // save the threadId in a cookie
                document.cookie = `_tid=${data.threadId}; path=/; max-age=31536000`;

                this.responseTo = data.query;

                // get index of last message
                const index = this.messages.length;
                const output = data.output;

                if (data.role != 'user') {
                    data.output = "";
                    this.messages.push(data);

                    let i = 0;
                    const speed = 40; // speed in milliseconds
                    const type = () => {
                        if (i < output.length) {
                            this.messages[index].output += output.charAt(i);
                            i++;
                            setTimeout(type, speed);
                        }
                        var objDiv = document.getElementById("chat-logs");
                        objDiv.scrollTop = objDiv.scrollHeight;
                        objDiv.scrollTop = objDiv.scrollHeight;
                    }
                    type();
                }
                this.loading = false;
            });
        }
    }
});
