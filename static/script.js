async function sendMessage() {
    console.log("script loaded");
    const input = document.getElementById("user-input");
    const message = input.value;

    if(message.trim() === "") return;

    const messagesDiv = document.getElementById("messages");

    messagesDiv.innerHTML += `<div class="user">You: ${message}</div>`;

    input.value = "";

    const response = await fetch("/api/chat", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            sessionId: "demo-session",
            message: message
        })
    });

    const data = await response.json();

    messagesDiv.innerHTML += `<div class="bot">Assistant: ${data.reply}</div>`;

    messagesDiv.scrollTop = messagesDiv.scrollHeight;
}