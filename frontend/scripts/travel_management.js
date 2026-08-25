const search_button = document.getElementById("button")



search_button.addEventListener("click",async (e) =>{
    e.preventDefault()
    const travel_id = Number(document.getElementById("travelId").value);
    const token = localStorage.getItem("token")
    const response = await fetch(`/travels_maintain/get_user?travel_id=${user_id}`,
        {
        method: "POST",
        headers: {
            "Authorization": `Bearer ${token}`
        }
        }
        )
    const travel_data = await response.json()
    console.log(user_data)
})
