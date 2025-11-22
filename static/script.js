const chatMessages = document.getElementById('chatMessages');
const userInput = document.getElementById('userInput');
const sendButton = document.getElementById('sendButton');

// Auto-focus input on load
userInput.focus();

// Send message on Enter key
userInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        sendMessage();
    }
});

// Send message on button click
sendButton.addEventListener('click', sendMessage);

function sendExample(text) {
    userInput.value = text;
    sendMessage();
}

async function sendMessage() {
    const message = userInput.value.trim();

    if (!message) return;

    // Clear input and disable while processing
    userInput.value = '';
    userInput.disabled = true;
    sendButton.disabled = true;

    // Remove welcome message if it exists
    const welcomeMessage = document.querySelector('.welcome-message');
    if (welcomeMessage) {
        welcomeMessage.style.animation = 'fadeOut 0.3s ease-out';
        setTimeout(() => welcomeMessage.remove(), 300);
    }

    // Add user message
    addMessage(message, 'user');

    // Add typing indicator
    const typingIndicator = addTypingIndicator();

    try {
        const response = await fetch('/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ message }),
        });

        const data = await response.json();

        // Remove typing indicator
        typingIndicator.remove();

        if (response.ok) {
            addMessage(data.response, 'assistant');
        } else {
            addMessage(`Error: ${data.error || 'Something went wrong'}`, 'assistant');
        }
    } catch (error) {
        typingIndicator.remove();
        addMessage('Sorry, I encountered an error. Please try again.', 'assistant');
        console.error('Error:', error);
    } finally {
        // Re-enable input
        userInput.disabled = false;
        sendButton.disabled = false;
        userInput.focus();
    }
}

function addMessage(text, role) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${role}`;

    const avatar = document.createElement('div');
    avatar.className = 'message-avatar';
    avatar.textContent = role === 'user' ? '👤' : '🤖';

    const content = document.createElement('div');
    content.className = 'message-content';
    content.textContent = text;

    messageDiv.appendChild(avatar);
    messageDiv.appendChild(content);

    chatMessages.appendChild(messageDiv);

    // Scroll to bottom with smooth animation
    setTimeout(() => {
        chatMessages.scrollTo({
            top: chatMessages.scrollHeight,
            behavior: 'smooth'
        });
    }, 100);

    return messageDiv;
}

function addTypingIndicator() {
    const typingDiv = document.createElement('div');
    typingDiv.className = 'typing-indicator';

    const avatar = document.createElement('div');
    avatar.className = 'message-avatar';
    avatar.style.background = 'var(--primary-gradient)';
    avatar.style.boxShadow = '0 4px 12px rgba(102, 126, 234, 0.3)';
    avatar.textContent = '🤖';

    const content = document.createElement('div');
    content.className = 'message-content';

    for (let i = 0; i < 3; i++) {
        const dot = document.createElement('div');
        dot.className = 'typing-dot';
        content.appendChild(dot);
    }

    typingDiv.appendChild(avatar);
    typingDiv.appendChild(content);

    chatMessages.appendChild(typingDiv);

    // Scroll to bottom
    chatMessages.scrollTo({
        top: chatMessages.scrollHeight,
        behavior: 'smooth'
    });

    return typingDiv;
}

// Add fadeOut animation to CSS dynamically
const style = document.createElement('style');
style.textContent = `
    @keyframes fadeOut {
        from {
            opacity: 1;
            transform: scale(1);
        }
        to {
            opacity: 0;
            transform: scale(0.95);
        }
    }
`;
document.head.appendChild(style);
