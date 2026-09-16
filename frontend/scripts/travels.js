//Get travels container section
const travel_section = document.getElementById("travels_container")
const travel_category = document.querySelectorAll(".category_btn")
const travel_tendence = document.getElementById("travels_tendence")


//Get request to obtain travels
async function get_travels() {
    const response = await fetch(
        "/travel/get_travels",
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

async function get_tendences() {
    const response = await fetch(
        "/travel/tendence_travels",
        {
            method: "GET",
            headers: {
                "Content-Type": "application/json",
            }
        },
    )

    const travels = await response.json()
    travels.forEach(travel => {
    //Card container for each travel object
        const card = document.createElement("div")
        card.className = "travel_card"

        const travel_image = document.createElement("img")
        travel_image.src = `uploads/${travel.image}`
        card.append(travel_image)

        const card_information = document.createElement("div")
        card_information.className = "card_information"

        const travel_destination = document.createElement("h2")
        travel_destination.innerText = travel.destination

        const travel_button = document.createElement("button")
        travel_button.innerText = "See more"
        travel_button.className = "card_button"

        card_information.append(travel_destination)
        card_information.append(travel_button)

        card.append(card_information)
        travel_tendence.append(card)
    })
};

   
        




travel_category.forEach(category => {
    category.addEventListener("click", async () => {
        travel_section.innerHTML = ""
        console.log("hello word")
        const response = await fetch(
            "/travel/get_travels",
            {
                method: "GET",
                headers: {
                    "Content-Type": "application/json"
                }
            }

        )
        const travels = await response.json()
        travels.forEach(travel => {
            if (travel.activity.toLowerCase() == category.innerText.toLowerCase()) {
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
            }

        });

    })
})


get_travels()
get_tendences()