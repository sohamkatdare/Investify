// JS Code to interact with the simplify route (via POST request).
messages = [{"role": "system", "content": "Hello. I am your personal financial instructor. What topic would you like to learn more about today?"}];
request_messages = [];
systemFinished = true;

// Unique ID for the conversation.
conversation_id = Math.random().toString(16).slice(2);

// If query string is not empty, then the user is loading a saved conversation.
const urlParams = new URLSearchParams(window.location.search);
cid = urlParams.get('cid');
if (cid) {
    // Get the conversation from the backend.
    getConversations().then((conversations) => {
        // Iterate over the conversations and find the one with the matching cid.
        let found = false
        for (var i = 0; i < conversations.length; i++) {
            if (conversations[i]["cid"] === cid) {
                // Set the messages and request_messages variables to the conversation's messages.
                messages = conversations[i]["messages"];
                request_messages = conversations[i]["request_messages"];
                conversation_id = cid;

                // Update the save button.
                saveState = true;
                document.getElementById("save-button").classList.toggle("bg-rose-900");
                document.getElementById("save-button").classList.toggle("hover:bg-rose-700");

                // Update the chat UI.
                updateChat();
                found = true;
                break;
            }
        }

        if (!found) {
            // If the conversation was not found, then redirect to the simplify page without query params.
            window.location.href = "/simplify";
        }
    });
}

function submit(event) {
    event.preventDefault();
    if (!systemFinished) {
        return;
    }

    user_prompt = document.getElementById("user_prompt");
    messages = [...messages, {"role": "user", "content": user_prompt.value}];
    updateChat();

    data = JSON.stringify({"messages": messages})
    if (messages.length == 2) {
        data = JSON.stringify({"topic": user_prompt.value});
    }
    user_prompt.value = ""; // Clear the input field.
    systemFinished = false;

    // Send POST request to simplify route. Response will be a stream.
    fetch("/simplify", {
        method: "POST",
        body: data,
        headers: {
            "Content-Type": "application/json"
        }
    })
    // Retrieve its body as ReadableStream
    .then((response) => {
        const reader = response.body.getReader();
        // read() returns a promise that resolves when a value has been received
        reader.read().then(function pump({ done, value }) {
            if (done) {
                // Do something with last chunk of data then exit reader
                return;
            }
            // Otherwise do something here to process current chunk
            // Convert Uint8Array to string
            var decoder = new TextDecoder();
            var chunk = decoder.decode(value);

            // Check if the chunk is a json object in string form.
            try {
                chunk = JSON.parse(chunk);
            } catch (e) {
                // If not, then it is a string.
                chunk = chunk;
            }

            // If chunk is a json...
            if (typeof chunk === "object") {
                request_messages = chunk;
            } else {
                if (typeof chunk !== "string") {
                    chunk = chunk.toString();
                }
                // Replace all newlines with <br> tags.
                chunk = chunk.replace(/\n/g, "<br>");
                // Replace ** with nothing.
                chunk = chunk.replace(/\*\*/g, "");

                // If last message is a user message, add the chunk to the messages array.
                if (messages[messages.length - 1]["role"] === "user") {
                    var conversation = document.getElementById("conversation");
                    messages = [...messages, {"role": "system", "content": chunk}];
                    const last_message = conversation.lastChild;
                    last_message.scrollIntoView();
                } else {
                    messages[messages.length - 1]["content"] += chunk;
                }
            }

            // Update the chat UI
            updateChat();

            // Read some more, and call this function again
            return reader.read().then(pump);
        });
        systemFinished = true;
    })
    .catch((err) => console.error(err));
}

function updateChat() {
    // Update the Chat UI to reflect the messages data model.
    var conversation = document.getElementById("conversation");

    // Clear the conversation.
    conversation.innerHTML = "";

    // Iterate through messages and add them to the conversation.
    for (var i = 0; i < messages.length; i++) {
        var message = messages[i];
        var div = document.createElement("div");
        div.className = "h-auto w-full text-lg text-white py-10 px-[10vw]";
        if (message["role"] === "user") {
            div.className += " bg-slate-100/25";
        }
        div.innerHTML = message["content"];
        conversation.appendChild(div);
    }
    conversation.scrollTop = conversation.scrollHeight - conversation.clientHeight;

    if (messages.length > 1 && saveButton) {
        saveButton.classList.remove("hidden");
    }
}

let saveState = false;
async function toggleSave(e) {
    // Toggle the favorite button state in the backend asychronously
    saveState = !saveState;
    if (saveState) {
        addConversation(conversation_id, messages, request_messages);
    } else {
        removeConversation(conversation_id, messages, request_messages);
    }
    document.getElementById("save-button").classList.toggle("bg-rose-900");
    document.getElementById("save-button").classList.toggle("hover:bg-rose-700");
}


document.getElementById("form").onsubmit = submit;
let saveButton = document.getElementById("save-button")
if (saveButton) {
    saveButton.addEventListener("click", toggleSave)
}

updateChat();