document.addEventListener('DOMContentLoaded', function() {
    const chatIcon = document.getElementById('chat-icon');
    const chatBox = document.getElementById('chat-box');
    const closeMsg = document.getElementById('close-msg');
    const initialMessage = document.getElementById('initial-message');
    const sendBtn = document.getElementById('send-btn');
    const chatInput = document.getElementById('chat-input');
    const chatHistory = document.getElementById('chat-history');
    let firstMessageShown = false;

    // Toggle chat box visibility
    chatIcon.addEventListener('click', function() {
        if (chatBox.style.display === 'none' || chatBox.style.display === '') {
            chatBox.style.display = 'flex';
            initialMessage.style.display = 'none'; // Hide initial message if chat is opened
            
            // Show the first message only once
            if (!firstMessageShown) {
                let adminMessage = document.createElement('div');
                adminMessage.classList.add('admin-message');
                adminMessage.textContent = 'Thank you for reaching out! How can I assist you?';
                chatHistory.appendChild(adminMessage);
                chatHistory.scrollTop = chatHistory.scrollHeight;
                firstMessageShown = true;
            }
        } else {
            chatBox.style.display = 'none';
        }
    });

    // Close initial message
    closeMsg.addEventListener('click', function() {
        initialMessage.style.display = 'none';
    });

    // Send message function
    sendBtn.addEventListener('click', function() {
        sendMessage();
    });

    // Send message on Enter key press
    chatInput.addEventListener('keypress', function(event) {
        if (event.key === 'Enter') {
            sendMessage();
        }
    });

    function sendMessage() {
        let messageText = chatInput.value.trim();
        if (messageText !== '') {
            // Append message to chat history
            let messageElement = document.createElement('div');
            messageElement.classList.add('user-message');
            messageElement.textContent = messageText;
            chatHistory.appendChild(messageElement);

            // Clear input field after sending
            chatInput.value = '';

            // Scroll to the latest message
            chatHistory.scrollTop = chatHistory.scrollHeight;
        }
    }
});
