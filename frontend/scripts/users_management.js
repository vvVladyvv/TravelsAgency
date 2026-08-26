const search_button = document.getElementById("button")



search_button.addEventListener("click",async (e) =>{
    e.preventDefault()
    const user_id = Number(document.getElementById("userId").value);
    const token = localStorage.getItem("token")
    const response = await fetch(`/user_maintain/get_user?user_id=${user_id}`,
        {
        method: "POST",
        headers: {
            "Authorization": `Bearer ${token}`
        }
        }
        )
    const user_data = await response.json()
    
})
