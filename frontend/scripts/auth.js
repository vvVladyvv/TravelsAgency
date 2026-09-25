async function get_current_user(){
    const user_container = document.getElementById("user-service");

    if (!user_container) {
        return;
    }

     //extract token from localstorage
        const token = localStorage.getItem("token")
        //Get request to my current_user endpoint and pass token in the header
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

        const second_data = await second_response.json()
        //if the user is logged in, display the profile and logout button
        if (second_response.ok){
            user_container.innerHTML = `
                <a href="/profile">
                    <img src="/uploads/${second_data.image}" alt="Profile Picture">
                </a>
                <div class="user-extra">
                    <li><a href="/profile">Profile</a></li>
                    <li><a href="/logout.html">Logout</a></li>
                </div>
            `
        }

            
}

function initializeAuth() {
    if (document.getElementById("user-service")) {
        get_current_user();
    }
}

document.addEventListener("componentsLoaded", initializeAuth, { once: true });
initializeAuth();




