const form = document.getElementById('zoomForm');
const responseMessage = document.getElementById('responseMessage');

form.addEventListener('submit', async (event) => {
  event.preventDefault();

  const meetingLink = document.getElementById('meetingLink').value;

  if (!meetingLink) {
    responseMessage.textContent = "Please enter a valid Zoom meeting link.";
    responseMessage.style.color = "red";
    return;
  }

  try {
    const response = await fetch('http://127.0.0.1:5000/join_meeting', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ meeting_link: meetingLink }),
    });

    const data = await response.json();

    if (response.ok) {
      responseMessage.textContent = `Bot registered successfully! Join URL: ${data.join_url}`;
      responseMessage.style.color = "green";
    } else {
      responseMessage.textContent = `Error: ${data.error}`;
      responseMessage.style.color = "red";
    }
  } catch (error) {
    responseMessage.textContent = "An error occurred. Please try again.";
    responseMessage.style.color = "red";
  }
});
