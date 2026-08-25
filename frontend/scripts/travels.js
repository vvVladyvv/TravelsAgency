//Get travels container section
const travel_section = document.getElementById("travels_container")


//Get request to obtain travels
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

    //We store the returned data(travels object) and convert it to JSON
    const travels = await response.json()
    //For each travel object we create a travel card container with mini info
    travels.forEach(travel => {
        //Create travel_Card container with class "travel_card"
        const card = document.createElement("div")
        card.className = "travel_card"

        //little container for info into the card
        const card_information = document.createElement("div")
        card_information.className = "card_information"

        //Inside the info container we create tittle and button
        const travel_destination = document.createElement("h2")
        travel_destination.innerText = travel.destination

        const travel_button = document.createElement("button")
        travel_button.innerText = "See more"
        travel_button.className = "card_button"

        //Then create a new container inside the card for image
        const image_container = document.createElement("div")
        image_container.className = "card_image"

        const image = document.createElement("img")
        image.src = `uploads/${travel.image}`
        image_container.append(image)


        card_information.append(travel_destination)
        card_information.append(travel_button)

        card.append(image_container)
        card.append(card_information)

        //Putting all containers inside the travel section (Main container)
        travel_section.append(card)

        //When mouse are hover the card(image) this show hidde info
        image_container.addEventListener("mouseenter", () => {
            card_information.classList.add("show")
        })
        //But when mouse leave the card(image) this info is hidden again
        image_container.addEventListener("mouseleave", () => {
            card_information.classList.remove("show")
        })
    });

}

get_travels()