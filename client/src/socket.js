import {io} from "socket.io-client";

let threadId = null;
try {
    threadId = document.cookie
        .split("; ")
        .find((row) => row.startsWith("_tid="))
        ?.split("=")[1];
    if(threadId == undefined) threadId = "NONE";

} catch (e) {
    console.log(e);
}

// "undefined" means the URL will be computed from the `window.location` object
const URL =
    process.env.NODE_ENV === "production" ? undefined : "https://pixelleassistant.go2partners.com/";

export const socket = io(URL, {
    auth: {
        token: "AuthToken",
        threadId: threadId,
    },
});
