const data_container = document.getElementById("data_container")
const operations = document.getElementById("operations")
const data_edit = document.getElementById("data_edit")
const search_container = document.getElementById("search")
const edit_btn = document.getElementById("edit_btn")
const delete_btn = document.getElementById("delete_btn")
const edit_submit = document.getElementById("edit_submit")
const search_button = document.getElementById("search_button")



search_button.addEventListener("click", async (e) => {
    e.preventDefault()
    const travelId = document.getElementById("travelId").value
    const token = localStorage.getItem("token")
    const response = await fetch(`/travel_maintain/get_travel?travel_id=${travelId}`,
        {
            method: "POST",
            headers: {
                "Authorization": `Bearer ${token}`
            }
        }
    )
    const data = await response.json()
    if (response.ok){
        operations.classList.toggle("show")
        search_container.classList.toggle("hidden")
    }
    console.log(data)

    //Container for travel information
    const data_card = document.createElement("div")
    data_card.className = "data_card"

    //Create image for travel
    const image_container = document.createElement("div")
    image_container.className = "image_container"

    const image = document.createElement("img")
    image.src = `uploads/${data.image}`
    image_container.append(image)

    //Create info container
    const info_container = document.createElement("div")
    info_container.className = "info_container"

    //Create Travel info elements
    //--------------  ID  -------------- //
    const id = document.createElement("h2")
    id.innerText = "ID"
    const data_id = document.createElement("p")
    data_id.innerText = data.id

    info_container.append(id)
    info_container.append(data_id)

    //--------------  Destination  -------------- //
    const destination = document.createElement("h2")
    destination.innerText = "Destination"
    const data_destination = document.createElement("p")
    data_destination.innerText = data.destination

    info_container.append(destination)
    info_container.append(data_destination)

    //--------------  activity  -------------- //
    const activity = document.createElement("h2")
    activity.innerText = "Activity"
    const data_activity = document.createElement("p")
    data_activity.innerText = data.activity

    info_container.append(activity)
    info_container.append(data_activity)

    //--------------  price  -------------- //
    const price = document.createElement("h2")
    price.innerText = "Price"
    const data_price = document.createElement("p")
    data_price.innerText = data.price

    info_container.append(price)
    info_container.append(data_price)

    //------------- Available Seats ------------------- //
    const available_seats = document.createElement("h2")
    available_seats.innerText = "Available Seats"
    const data_available_seats = document.createElement("p")
    data_available_seats.innerText = data.available_seats

    info_container.append(available_seats)
    info_container.append(data_available_seats)

    //------------- Duration ------------------- //
    const duration = document.createElement("h2")
    duration.innerText = "Duration"
    const data_duration = document.createElement("p")
    data_duration.innerText = data.duration

    info_container.append(duration)
    info_container.append(data_duration)

    //Add all into the travel_container
    data_card.append(image_container)
    data_card.append(info_container)
    data_container.append(data_card)

    delete_travel(travelId, token)
    edit_travel(travelId, token)

})


edit_btn.addEventListener("click", ()=>{
    data_edit.classList.toggle("show")
})


async function delete_travel(travelId, token) {
    delete_btn.addEventListener("click", async (e) => {
        e.preventDefault()

        const response = await fetch(
            `/travel_maintain/delete_travel?id=${travelId}`,
            {
                method: "DELETE",
                headers: {
                    "Authorization": `Bearer ${token}`
                }
            }
        )
    })
}

async function edit_travel(travelId, token) {
    edit_submit.addEventListener("click", async (e) => {
        const new_data = new FormData() 

        const new_destination = document.getElementById("n_destination").value
        const new_activity = document.getElementById("n_activity").value
        const new_price = document.getElementById("n_price").value
        const new_available_seats = document.getElementById("n_available_seats").value
        const new_duration = document.getElementById("n_duration").value
        const new_image = document.getElementById("n_image").files[0]

        new_data.append("travelId", travelId)
        new_data.append("destination", new_destination)
        new_data.append("activity", new_activity)
        new_data.append("price", new_price)
        new_data.append("available_seats", new_available_seats)
        new_data.append("duration", new_duration)
        new_data.append("image", new_image)



        const response = await fetch(
            "/travel_maintain/edit_travel",
            {
                method: "PUT",
                headers: {
                    "Authorization": `Bearer ${token}`
                },
                body: new_data
            }
        )
    })
}

    