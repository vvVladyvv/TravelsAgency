const form = document.getElementById('form');

if (form) {
  const destination = new URLSearchParams(window.location.search).get('destination');
  if (destination) {
    document.getElementById('destination').value = destination;
  }

  form.addEventListener('submit', async (event) => {
    const token = localStorage.getItem('token');
    event.preventDefault();
    const destination = document.getElementById('destination').value;
    const companions = document.getElementById('companions').value;
    const include_food = document.getElementById('include_food').checked;

    const response = await fetch('/travel/reserve_travel', {
        method: 'POST',
        body: JSON.stringify({
            destination,
            companions,
            include_food
        }),
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
        }
    });

    const data = await response.json();
    console.log(data);

    }
  )
};