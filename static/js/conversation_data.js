async function addConversation(cid, messages, request_messages) {
    const response = await fetch('/conversations', {
        method: 'POST',
        headers: {
            'action': 'add',
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            'cid': cid,
            'messages': messages,
            'request_messages': request_messages
        })
    }).then((response) => {
        if (response.status !== 200) {
            onFail(ticker);
        }
        return response;
    });
}

async function removeConversation(cid, messages, request_messages) {
    const response = await fetch('/conversations', {
        method: 'POST',
        headers: {
            'action': 'remove',
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            'cid': cid,
            'messages': messages,
            'request_messages': request_messages
        })
    }).then((response) => {
        if (response.status !== 200) {
            onFail(ticker);
        }
        return response;
    });
}

async function getConversations() {
    const response = await fetch('/conversations').then((response) => {
        if (response.status !== 200) {
            onFail(ticker);
        }
        return response;
    });
    return response.json();
}