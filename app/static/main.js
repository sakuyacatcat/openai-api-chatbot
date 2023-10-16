let conversationHistory = [
  { role: "system", content: "You are a helpful assistant." },
  { role: "system", content: "Think step-by-step to solve the problem." },
];

async function sendMessage() {
  const userInput = document.getElementById("user-input").value;
  document.getElementById("user-input").value = "";

  conversationHistory.push({ role: "user", content: userInput });

  const response = await fetch("/chat", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ conversation: conversationHistory }),
  });

  const data = await response.json();
  conversationHistory.push({ role: "assistant", content: data.response });

  const chatBox = document.getElementById("chat-box");
  chatBox.innerHTML += `<div>User: ${userInput}</div>`;
  chatBox.innerHTML += `<div>Bot: ${data.response}</div>`;
}
