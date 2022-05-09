window.addEventListener('DOMContentLoaded', function(e) {
    const messageInput = document.querySelector('#message');
    const button = document.querySelector('#button');
    const chatBox = document.querySelector('#chatbox');

    function generateChatBubbleItem({ uuid, message, timestamp }) {
        const li = document.createElement('li');
        li.innerHTML = `[${timestamp}] <b>${uuid}</b>: ${message}`;
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
