async function getElements(header, footer) {
    
    //Stored our empty elements
    const header_container = document.getElementById(header)
    const footer_container = document.getElementById(footer)

    //Looking for components files and verify if exist
    try {
        const header_response = await fetch("header.html");
        const footer_response = await fetch("footer.html");
        
        if (!header_response.ok || !footer_response.ok) {
            console.error(`Error ${header_response.status}: Files not found`);
            return;
        }

        //Extract only 'html' text from the components request
        const header_html = await header_response.text();
        const footer_html = await footer_response.text();

        //Insert this text in our empty elements
        header_container.innerHTML = header_html
        footer_container.innerHTML = footer_html
        document.dispatchEvent(new Event("componentsLoaded"))

    } catch (error) {
        console.error("Error loading components:", error);
    }
}

getElements("header", "footer")


