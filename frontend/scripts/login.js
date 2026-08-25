//Getting our form element
const form = document.getElementById("form")


//If form element exist, once the form has been submitted
if (form){
    form.addEventListener("submit", async (e) =>{
        e.preventDefault()

        //Extract data from the form
        const email = document.getElementById("email").value;
        const password = document.getElementById("password").value;

        try{
            //Post request to our login endpoint with our data convert in json
            const response = await fetch(
                "/user/login",
                {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json"
                    },

                    body: JSON.stringify({email, password})
                },
            )

            //We store our data and convert it to json
            const data = await response.json();
            

            if (!response.ok){
                alert(data.detail || "Failed try sign in")
            }

            //Save token in localstorage, and return user to home
            localStorage.setItem("token", data.access_token)
            window.location.href = "/";
            

           

        } catch (error) {
            console.error("Http Response reject conection.", error)
        }


    })
}
