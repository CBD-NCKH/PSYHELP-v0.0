const chatbox = document.getElementById('chatbox');
const userInput = document.getElementById('userInput');
const sendBtn = document.getElementById('sendBtn');

sendBtn.addEventListener('click', async () => {
    const userMessage = userInput.value;
    if (!userMessage) return;

    // Hiển thị tin nhắn người dùng
    chatbox.innerHTML += `<p><strong>You:</strong> ${userMessage}</p>`;
    userInput.value = '';

    // Gửi yêu cầu đến backend
    const response = await fetch('/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: userMessage }),
    });
    const data = await response.json();

    // Hiển thị phản hồi từ AI
    chatbox.innerHTML += `<p><strong>AI:</strong> ${data.response}</p>`;
});
