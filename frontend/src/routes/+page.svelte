<script lang="ts">
	import Router from 'svelte-spa-router';
	import Home from '../pages/Home.svelte';
	import Login from '../pages/Login.svelte';
	import Register from '../pages/Register.svelte';
	import Team from '../pages/Team.svelte';
	const routes = {
		'/': Home,
		'/login': Login,
		'/register': Register,
		'/team/:id': Team
	};
</script>

<Router {routes} />
