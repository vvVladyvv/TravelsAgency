const form = document.getElementById("form")

if (form) {
    form.addEventListener("submit", async (e) => {
        e.preventDefault()

        const destination = document.getElementById("destination").value
        const activity = document.getElementById("activity").value
        const price = document.getElementById("price").value
        const available = document.getElementById("available").value
        const duration = document.getElementById("duration").value
        const image = document.getElementById("img").files[0]


        const data = new FormData()

        data.append("destination", destination)
        data.append("activity", activity)
        data.append("price", price)
        data.append("available_seats", available)
        data.append("duration", duration)
        data.append("image", image)

        try {
            const response = await fetch(
                "/travel/create_travel",
                {
                    method: "POST",
                    body: data
                }
            )

            const dataResponse = await response.json();
            if (response.ok) {
                alert("Travel created successfully!")
                window.location.href = "/";
            } else {
                console.error("Create travel failed:", dataResponse);
                alert("Failed to create travel: " + JSON.stringify(dataResponse.detail));
            }
        } catch (error) {
            console.error("Http Response reject connection.", error)
            alert("Connection error occurred.")
        }
    })
}