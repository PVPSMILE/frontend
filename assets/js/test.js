document.getElementById("form-btn").addEventListener("click", async () => {
    const form = document.getElementById("form");

    const name = form.elements["name"].value;
    const email = form.elements["email"].value;
    const message = form.elements["message"].value;

    const response = await fetch("http://127.0.0.1:8000/contact/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ name, email, message })
    });

    if (response.ok) {
        alert("Message sent successfully!");
        form.reset();
    } else {
        alert("Error sending message!");
    }
});
