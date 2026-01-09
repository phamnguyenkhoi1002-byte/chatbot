const API_URL = "http://127.0.0.1:8000/chat";

let sessionId = localStorage.getItem("chat_session_id");
if (!sessionId) {
    sessionId = "user_" + Date.now() + "_" + Math.random().toString(36).substr(2, 9);
    localStorage.setItem("chat_session_id", sessionId);
}

async function sendMessage() {
    const inputField = document.getElementById("userInput");
    const userText = inputField.value.trim();
    if (userText === "") return;

    addMessage(userText, "user-message");
    inputField.value = "";
    inputField.disabled = true;

    const loadingId = addMessage("🤔 Đang suy nghĩ...", "bot-message", true);

    try {
        const response = await fetch(API_URL, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                message: userText,
                session_id: sessionId
            })
        });

        const data = await response.json();
        removeMessage(loadingId);
        addMessage(data.answer, "bot-message");

    } catch (error) {
        removeMessage(loadingId);
        addMessage("⚠️ Server đang lỗi hoặc chưa bật!", "bot-message");
    } finally {
        inputField.disabled = false;
        inputField.focus();
    }
}

function addMessage(text, className, isTemp = false) {
    const chatBox = document.getElementById("chatBox");
    const msgDiv = document.createElement("div");
    msgDiv.className = className;
    msgDiv.innerText = text;

    const id = "msg-" + Date.now() + Math.random();
    msgDiv.id = id;

    if (isTemp) {
        msgDiv.style.fontStyle = "italic";
        msgDiv.style.opacity = "0.7";
    }

    chatBox.appendChild(msgDiv);
    chatBox.scrollTo({
        top: chatBox.scrollHeight,
        behavior: "smooth"
    });

    return id;
}

function removeMessage(id) {
    const el = document.getElementById(id);
    if (el) el.remove();
}

document.getElementById("userInput").addEventListener("keypress", e => {
    if (e.key === "Enter") sendMessage();
});