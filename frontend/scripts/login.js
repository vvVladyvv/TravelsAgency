const form = document.getElementById("form")


if (form){
    form.addEventListener("submit", async (e) =>{
        e.preventDefault()

        const email = document.getElementById("email").value;
        const password = document.getElementById("password").value;

        try{
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

            const data = await response.json();
            console.log(data.access_token)

            if (!response.ok){
                alert(data.detail || "Failed try sign in")
            }

            localStorage.setItem("token", data.access_token)
            window.location.href = "/";
            

           

        } catch (error) {
            console.error("Http Response reject conection.", error)
        }


    })
}
