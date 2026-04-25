// AI对话模块

async function callDeepSeek(question) {
    const apiKey = localStorage.getItem('deepseek_api_key') || 'sk-8413f72a3f084fb08c84389555a76d37';
    
    try {
        const response = await fetch('https://api.deepseek.com/v1/chat/completions', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': 'Bearer ' + apiKey
            },
            body: JSON.stringify({
                model: 'deepseek-chat',
                messages: [
                    { role: 'system', content: '你是专业的学习助手。' },
                    { role: 'user', content: question }
                ]
            })
        });
        const data = await response.json();
        return data.choices[0].message.content;
    } catch(e) {
        return 'AI服务暂时不可用';
    }
}

async function sendDeepSeekChat() {
    const input = document.getElementById('deepseek-chat-input');
    const text = input.value.trim();
    if (!text) return;
    
    const messages = document.getElementById('deepseek-chat-messages');
    messages.innerHTML += '<div class="chat-msg user"><div class="chat-bubble">' + text + '</div></div>';
    input.value = '';
    
    const response = await callDeepSeek(text);
    messages.innerHTML += '<div class="chat-msg"><div class="chat-bubble">' + response + '</div></div>';
    messages.scrollTop = messages.scrollHeight;
}

async function sendAvatarChat() {
    const input = document.getElementById('avatar-chat-input');
    const text = input.value.trim();
    if (!text) return;
    
    const messages = document.getElementById('avatar-chat-messages');
    messages.innerHTML += '<div class="chat-msg user"><div class="chat-bubble">' + text + '</div></div>';
    input.value = '';
    
    const response = await callDeepSeek(text);
    messages.innerHTML += '<div class="chat-msg"><div class="chat-bubble">' + response + '</div></div>';
}
