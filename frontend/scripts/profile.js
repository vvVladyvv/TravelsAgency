const user_container = document.getElementById("user_container")
const operations = document.getElementById("operations")

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

    const user_data = await second_response.json()

    const user_card = document.createElement("div")
    user_card.className = "user_card"

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
    user_container.append(user_card)
    

    
    

};

load_profile()