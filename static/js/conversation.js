// JS Code to interact with the simplify route (via POST request).
messages = [];

function submit(event) {
    event.preventDefault();
    var form = document.getElementById("form");
    var formData = new FormData(form);
    var data = {};
    for (var key of formData.keys()) {
        data[key] = formData.get(key);
    }
    messages = [...messages, {"role": "user", "content": data["message"]}];
    console.log(messages);
    
    // Send POST request to simplify route
    fetch("/simplify", {
        method: "POST",
        body: JSON.stringify(data),
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
}