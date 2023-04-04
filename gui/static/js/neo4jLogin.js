const form = document.querySelector('form');
form.addEventListener('submit', e => {
	e.preventDefault();
	const host = form.host.value;
	const user = form.user.value;
	const password = form.password.value;
	// TODO: send login request to Neo4j server
});
