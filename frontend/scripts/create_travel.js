//getting form element from our create_travel file
const form = document.getElementById("form")

//If exist, we stored each value from the form 
if (form) {
    form.addEventListener("submit", async (e) => {
        e.preventDefault()

        const destination = document.getElementById("destination").value
        const activity = document.getElementById("activity").value
        const price = document.getElementById("price").value
        const available = document.getElementById("available").value
        const duration = document.getElementById("duration").value
        const image = document.getElementById("img").files[0]

        //Create a formData object, for store our values in dict(key-value). This cause we have diferent type value
        const data = new FormData()

        data.append("destination", destination)
        data.append("activity", activity)
        data.append("price", price)
        data.append("available_seats", available)
        data.append("duration", duration)
        data.append("image", image)

        //Post request to our Create_travel endpoint, awith data travel
        try {
            const token = localStorage.getItem("token")
            const response = await fetch(
                "/travel/create_travel",
                {
                    method: "POST",
                    headers: {
                        "Authorization": `Bearer ${token}`
                    },
                    body: data
                }
            )
            //We Store the returned data and convert it to json
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