// JS Code to interact with the simplify route (via POST request).
messages = [{"role": "system", "content": "Hello. I am your personal financial instructor. What topic would you like to learn more about today?"}];
request_messages = [];
systemFinished = true;

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
                    messages = [...messages, {"role": "system", "content": chunk}];
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
}

document.getElementById("form").onsubmit = submit;
updateChat();