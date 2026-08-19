const travel_section = document.getElementById("travels_container")

async function get_travels() {
    const response = await fetch(
        "/travel_maintain/get_travels",
        {
            method: "GET",
            headers: {
                "Content-Type": "application/json",
            }
        }
    )

    const travels = await response.json()
    travels.forEach(travel => {
        const card = document.createElement("div")
        card.className = "travel_card"

        /*Card Title*/
        const card_destination = document.createElement("h2")
        const destination = document.createElement("p")

        card_destination.innerText = "Destination"
        destination.innerText = travel.destination

        card.appendChild(card_destination)
        card.appendChild(destination)

         /*Card duration*/

        const card_duration = document.createElement("h2")
        const duration = document.createElement("p")

        card_duration.innerText = "Duration"
        duration.innerText = travel.duration

        card.appendChild(card_duration)
        card.appendChild(duration)

         /*Card available*/

        const card_available = document.createElement("h2")
        const available = document.createElement("p")

        card_available.innerText = "Available"
        available.innerText = travel.available_seats

        card.appendChild(card_available)
        card.appendChild(available)

         /*Card price*/

        const card_price = document.createElement("h2")
        const price = document.createElement("p")

        card_price.innerText = "Price"
        price.innerText = travel.price

        card.appendChild(card_price)
        card.appendChild(price)

        

        /*Card Image*/

        const card_image = document.createElement("img")
        card_image.src = `/uploads/${travel.image}`

        card.appendChild(card_image)



        travel_section.appendChild(card)

    });
}

get_travels()