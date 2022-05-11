window.addEventListener('DOMContentLoaded', function(e) {
    const messageInput = document.querySelector('#message');
    const button = document.querySelector('#button');
    const chatBox = document.querySelector('#chatbox');

    messageInput.focus();

    function genMessageBubble({ uuid, message, timestamp, pid }) {
        const li = document.createElement('li');
        li.innerHTML = `[${pid}] <b>${uuid}</b>: ${message}<div style="display: inline; color: gray; font-size: 8pt; margin-left: 16px; text-align: right;">${new Date(timestamp).toLocaleString()}</div>`;
        return li;
    }

    function genNotificationBubble({ message }) {
        const li = document.createElement('li');
        li.style.color = 'gray';
        li.style.fontSize = '10pt';
        li.innerHTML = message;
        return li;
    }

    const ws = new WebSocket(`ws://${window.location.host}/ws`);
    ws.onmessage = function(e) {
        const data = JSON.parse(e.data);
        if (data.tag === 'message') {
            chatBox.appendChild(genMessageBubble(data));
        } else if (data.tag === 'event') {
            chatBox.appendChild(genNotificationBubble(data));
        }
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
