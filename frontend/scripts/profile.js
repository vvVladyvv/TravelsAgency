const data_container = document.getElementById("data_container")
const operations = document.getElementById("operations")
const bookings_list = document.getElementById("bookings_list")

async function load_profile(){
    const token = localStorage.getItem("token")
       
    const response = await fetch(
        "/user/current_user",
        {
            method: "GET",
            headers: {
                "Content-Type": "application/json",
                "Authorization": `Bearer ${token}`
            }
        }
    )
        //getting data returned and convert it into json type
    const data = await response.json()
    const second_response = await fetch(
        "/user_maintain/get_user?user_id=" + data.user_id,
        {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            }
        }
    )
    const bookings_response = await fetch(
        "/booking/my_bookings",
        {
            method: "GET",
            headers: {
                "Content-Type": "application/json",
                "Authorization": `Bearer ${token}`
            }
        }
    )
    const bookings_data = await bookings_response.json()
    

    const user_data = await second_response.json()

    const user_card = document.createElement("div")
    user_card.className = "data_card"

    //Create image for user
    const image_container = document.createElement("div")
    image_container.className = "image_container"

    const user_image = document.createElement("img")
    user_image.src = `uploads/${user_data.image}`
    image_container.append(user_image)

    //Create info container
    const info_container = document.createElement("div")
    info_container.className = "info_container"

    //Create user info elements
    //--------------  ID  -------------- //
    const id = document.createElement("h2")
    id.innerText = "ID"
    const user_id = document.createElement("p")
    user_id.innerText = user_data.id

    info_container.append(id)
    info_container.append(user_id)

    //--------------  Username  -------------- //
    const username = document.createElement("h2")
    username.innerText = "Username"
    const user_username = document.createElement("p")
    user_username.innerText = user_data.username

    info_container.append(username)
    info_container.append(user_username)

    //--------------  Age  -------------- //
    const age = document.createElement("h2")
    age.innerText = "Age"
    const user_age = document.createElement("p")
    user_age.innerText = user_data.age

    info_container.append(age)
    info_container.append(user_age)

    //--------------  Email  -------------- //
    const email = document.createElement("h2")
    email.innerText = "Email"
    const user_email = document.createElement("p")
    user_email.innerText = user_data.email

    info_container.append(email)
    info_container.append(user_email)

    //------------- ROLE ------------------- //
    const role = document.createElement("h2")
    role.innerText = "Role"
    const user_role = document.createElement("p")
    user_role.innerText = user_data.role

    if (user_data.role == 'admin'){
        operations.classList.toggle("show")
    } 

    info_container.append(role)
    info_container.append(user_role)

    //Add all into the user_container
    user_card.append(image_container)
    user_card.append(info_container)
    data_container.append(user_card)

    bookings_data.forEach(booking => {
        const booking_card = document.createElement("div")
        booking_card.className = "booking_card"

        const booking_image_container = document.createElement("div")
        booking_image_container.className = "booking_image_container"
        const booking_image = document.createElement("img")
        booking_image.src = `/uploads/${booking.travel.image}`

        booking_image_container.append(booking_image)
        

        const booking_info = document.createElement("div")
        booking_info.className = "booking_info"

        

        const booking_id = document.createElement("h2")
        booking_id.innerText = "Booking ID"
        const booking_id_value = document.createElement("p")
        booking_id_value.innerText = booking.id



        const travel_destination = document.createElement("h2")
        travel_destination.innerText = "Destination"
        const travel_destination_value = document.createElement("p")
        travel_destination_value.innerText = booking.travel.destination


        const booking_cost = document.createElement("h2")
        booking_cost.innerText = "Total Cost"
        const booking_cost_value = document.createElement("p")
        booking_cost_value.innerText = booking.cost

        const booking_status = document.createElement("h2")
        booking_status.innerText = "Status"
        const booking_status_value = document.createElement("p")
        booking_status_value.innerText = booking.status

        const booking_date = document.createElement("h2")
        booking_date.innerText = "Booking Date"
        const booking_date_value = document.createElement("p")
        booking_date_value.innerText = booking.created

        booking_info.append(booking_id)
        booking_info.append(booking_id_value)
        booking_info.append(travel_destination)
        booking_info.append(travel_destination_value)
        booking_info.append(booking_cost)
        booking_info.append(booking_cost_value)
        booking_info.append(booking_status)
        booking_info.append(booking_status_value)
        booking_info.append(booking_date)
        booking_info.append(booking_date_value)

        booking_card.append(booking_image_container)
        booking_card.append(booking_info)
        bookings_list.append(booking_card)
    }
)

    

    
    

};

load_profile()