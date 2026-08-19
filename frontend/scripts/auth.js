const form = document.getElementById("form");
const user = document.getElementById("button")


/*First verify if login is valid*/

user.addEventListener("click", () =>{
    async function get_current_user(){
        const token = localStorage.getItem("token")
        console.log(token)

        try{
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

            const data = await response.json()

            console.log(data)

            if (!response.ok) {
                alert("Get current user failed!", data.detail)
            }

        }catch (error){
            console.error("Comunication lost", error)
        }
        

    }

    get_current_user()

})


/*Then add event and stop page reload*/



/*Request to the login endpoint */
/*Handle possible errors */

/*Catch token if login success */

