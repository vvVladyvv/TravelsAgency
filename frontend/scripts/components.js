async function getElements(id, path) {
    try {
        const response = await fetch(path);

        // Si el servidor da 404, no inyectes el error en el HTML
        if (!response.ok) {
            console.error(`Error ${response.status}: No se encontró el archivo en '${path}'`);
            return;
        }

        const html = await response.text();
        document.getElementById(id).innerHTML = html;
    } catch (error) {
        console.error("Error al cargar el componente:", error);
    }
}

getElements("header", "base.html")
