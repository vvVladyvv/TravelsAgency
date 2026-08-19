const form = document.getElementById("form")

if (form) {
    form.addEventListener("submit", async (e) => {
        e.preventDefault();
        const username = document.getElementById("username").value;
        const age = Number(document.getElementById("age").value);
        const email = document.getElementById("email").value;
        const password = document.getElementById("password").value;

        try {
            const response = await fetch("/user/register", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({ username, age, email, password })
            });

            const data = await response.json().catch(() => ({}));
            console.log("Respuesta del servidor:", data);

            if (!response.ok) {
                console.error("Registro fallido:", data);
            }
        } catch (error) {
            console.error("Server cant connect", error);
        }
    });
}
