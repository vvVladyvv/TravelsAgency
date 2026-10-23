const gallery = document.getElementById("travel-gallery");
const destinationFilter = document.getElementById("destination-filter");
const categoryFilter = document.getElementById("category-filter");
const durationFilter = document.getElementById("duration-filter");
const resultsCount = document.getElementById("results-count");
const emptyState = document.getElementById("empty-state");
let allTravels = [];

function addFilterOptions(select, values, labelForValue) {
    [...new Set(values.filter((value) => value !== null && value !== undefined && value !== ""))]
        .sort((first, second) => String(first).localeCompare(String(second), undefined, { numeric: true }))
        .forEach((value) => {
            const option = document.createElement("option");
            option.value = String(value).toLowerCase();
            option.textContent = labelForValue(value);
            select.append(option);
        });
}

function createTravelCard(travel, index) {
    const card = document.createElement("article");
    card.className = "travel-card";

    const imageFrame = document.createElement("div");
    imageFrame.className = "travel-card-image";
    if (travel.image) {
        const image = document.createElement("img");
        image.src = `/uploads/${encodeURIComponent(travel.image)}`;
        image.alt = `Travel in ${travel.destination}`;
        image.loading = index < 4 ? "eager" : "lazy";
        image.addEventListener("error", () => image.remove());
        imageFrame.append(image);
    }

    const category = document.createElement("span");
    category.className = "category-label";
    category.textContent = travel.activity || "Travel";
    imageFrame.append(category);

    const copy = document.createElement("div");
    copy.className = "travel-card-copy";
    const title = document.createElement("h3");
    title.textContent = travel.destination || "Destination";

    const meta = document.createElement("p");
    meta.className = "travel-meta";
    const duration = document.createElement("span");
    duration.textContent = travel.duration ? `${travel.duration} days` : "Duration varies";
    const price = document.createElement("span");
    price.textContent = travel.price ? `$${travel.price}` : "Ask for price";
    meta.append(duration, price);

    const bookLink = document.createElement("a");
    bookLink.className = "book-link";
    bookLink.href = `/reserve_travel.html?destination=${encodeURIComponent(travel.destination || "")}`;
    bookLink.textContent = "Plan this trip";

    copy.append(title, meta, bookLink);
    card.append(imageFrame, copy);
    return card;
}

function renderTravels() {
    const destinationQuery = destinationFilter.value.trim().toLowerCase();
    const categoryQuery = categoryFilter.value;
    const durationQuery = durationFilter.value;
    const filteredTravels = allTravels.filter((travel) => {
        const matchesDestination = (travel.destination || "").toLowerCase().includes(destinationQuery);
        const matchesCategory = !categoryQuery || (travel.activity || "").toLowerCase() === categoryQuery;
        const matchesDuration = !durationQuery || String(travel.duration) === durationQuery;
        return matchesDestination && matchesCategory && matchesDuration;
    });

    gallery.replaceChildren(...filteredTravels.map(createTravelCard));
    resultsCount.textContent = `${filteredTravels.length} ${filteredTravels.length === 1 ? "trip" : "trips"}`;
    emptyState.hidden = filteredTravels.length > 0;
}

async function loadTravels() {
    try {
        const response = await fetch("/travel/get_travels");
        if (!response.ok) {
            throw new Error(`Travel request failed (${response.status})`);
        }
        allTravels = await response.json();
        addFilterOptions(categoryFilter, allTravels.map((travel) => travel.activity), String);
        addFilterOptions(durationFilter, allTravels.map((travel) => travel.duration), (value) => `${value} days`);
        renderTravels();
    } catch (error) {
        console.error("Could not load travels:", error);
        resultsCount.textContent = "Trips could not be loaded";
        emptyState.textContent = "We could not load trips right now. Please try again in a moment.";
        emptyState.hidden = false;
    }
}

destinationFilter.addEventListener("input", renderTravels);
categoryFilter.addEventListener("change", renderTravels);
durationFilter.addEventListener("change", renderTravels);
document.getElementById("clear-filters").addEventListener("click", () => {
    destinationFilter.value = "";
    categoryFilter.value = "";
    durationFilter.value = "";
    renderTravels();
});

loadTravels();