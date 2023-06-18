// JS Code to interact with the simplify route (via POST request).
messages = [{"role": "system", "content": "Hello. I am your personal financial instructor. What topic would you like to learn more about today?"}];
request_messages = [{"role": "system", "content": "You are a helpful assistant that summarizes and simplifies Investopedia articles through your complete knowledge of finance and investing. You will also assist the user by answering questions about the article."}];

function submit(event) {
    event.preventDefault();
    user_prompt = document.getElementById("user_prompt");
    messages = [...messages, {"role": "user", "content": user_prompt.value}];
    updateChat();

    data = JSON.stringify(messages)
    if (messages.length == 2) {
        data = JSON.stringify({"topic": user_prompt.value});
    }
    
    console.log(data);

    // Send POST request to simplify route
    fetch("/simplify", {
        method: "POST",
        body: data,
        headers: {
            "Content-Type": "application/json",
        },
    })
    .then((response) => {
        if (response.status === 200) {
            return response.json();
        } else {
            console.log("Error: Simplify route returned status code " + response.status + ".");
        }
    })
    .then((data) => {
        messages = data;
        console.log(messages);
        // Update the chat
        updateChat();
    });
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