//We store form element
const form = document.getElementById("form")

if (form) {
    //If is true, once the form has been submitted, we extract all value
    form.addEventListener("submit", async (e) => {
        e.preventDefault();
        const username = document.getElementById("username").value;
        const age = Number(document.getElementById("age").value);
        const email = document.getElementById("email").value;
        const password = document.getElementById("password").value;

            //Post request to the register endpoint, with all data
        try {
            const response = await fetch("/user/register", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({ username, age, email, password })
            });
            //We store data and then convert it to JSON
            const data = await response.json();
            console.log("Respuesta del servidor:", data);

            if (!response.ok) {
                console.error("Registro fallido:", data);
            }
        } catch (error) {
            console.error("Server cant connect", error);
        }
    });
}
