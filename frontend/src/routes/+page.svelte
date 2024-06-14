<script lang="ts">
	import Router, { push } from 'svelte-spa-router';
	import Home from '../pages/Home.svelte';
	import Login from '../pages/Login.svelte';
	import Register from '../pages/Register.svelte';
	import Team from '../pages/Team.svelte';
	import Profile from '../pages/Profile.svelte';
	import wrap from 'svelte-spa-router/wrap';
	import { session } from '$lib/storage';

	const conditionFailedHandler = () => {
		if ($session === null) {
			push('/login');
		} else {
			push('/');
		}
	};

	const routes = {
		'/login': wrap({
			component: Login,
			conditions: [() => $session === null]
		}),
		'/register': wrap({
			component: Register,
			conditions: [() => $session === null]
		}),
		'/': wrap({
			component: Home,
			conditions: [() => $session !== null]
		}),
		'/profile': wrap({
			component: Profile,
			conditions: [() => $session !== null]
		}),
		'/team/:id': wrap({
			component: Team,
			conditions: [() => $session !== null]
		})
	};
</script>

<Router {routes} on:conditionsFailed={conditionFailedHandler} />
