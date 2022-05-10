window.addEventListener('DOMContentLoaded', function(e) {
    const messageInput = document.querySelector('#message');
    const button = document.querySelector('#button');
    const chatBox = document.querySelector('#chatbox');

    function generateChatBubbleItem({ uuid, message, timestamp, pid }) {
        const li = document.createElement('li');
        li.innerHTML = `[${pid}] <b>${uuid}</b>: ${message}<div style="display: inline; color: gray; font-size: 8pt; margin-left: 16px; text-align: right;">${new Date(timestamp).toLocaleString()}</div>`;
        return li;
    }

    const ws = new WebSocket(`ws://${window.location.host}/ws`);
    ws.onmessage = function(e) {
        chatBox.appendChild(generateChatBubbleItem(JSON.parse(e.data)));
    };

    button.addEventListener('click', function(e) {
        const message = messageInput.value;
        messageInput.value = '';

        ws.send(JSON.stringify({
            "message": message
        }));
    });

    messageInput.addEventListener('keypress', function(e) {
        if (e.key == 'Enter') {
            button.dispatchEvent(new MouseEvent('click'));
        }
    });
});
