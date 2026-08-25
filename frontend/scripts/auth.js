
//getting form and button elements 
const form = document.getElementById("form");
const user = document.getElementById("button")

//When user click submit button
user.addEventListener("click", () =>{
    async function get_current_user(){
        //extract token from localstorage
        const token = localStorage.getItem("token")

        try{
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

            if (!response.ok) {
                alert("Get current user failed!", data.detail)
            }

        }catch (error){
            console.error("Comunication lost", error)
        }
        

    }

})


