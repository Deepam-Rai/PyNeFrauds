const form = document.querySelector('form');
form.addEventListener('submit', e => {
	console.log("submitting")
	e.preventDefault();
	const host = form.host.value;
	const user = form.user.value;
	const password = form.password.value;
	// validate the credentials
	fetch('/validateCredentials', {
		method: 'POST',
		headers: {
			'Content-Type': 'application/json'
		},
		body: JSON.stringify({
			host: host,
			username: user,
			password: password
		}),
		credentials: 'include'
	})
		.then(response => {
			if (response.ok) {
				// Credentials are valid, do something here
				let errDiv = document.getElementById('error')
				errDiv.style.display='none'
				console.log('Login successful');
				window.location.href = "/gui_cypher"
			} else {
				let errDiv = document.getElementById('error')
				errDiv.innerHTML = "Credentials Not Valid. Could not log-in."
				errDiv.style.display = 'block'
				console.error('Login failed:', response.statusText);
			}
		})
		.catch(error => {
			let errDiv = document.getElementById('error')
			errDiv.innerHTML = "Some error occurred on the server side."
			errDiv.style.display = 'block'
			console.error('An error occurred:', error);
		});
})
