<script>
	import { goto } from '$app/navigation';
	import { BACKEND_URL } from '$lib/api';
	import { onMount } from 'svelte';

	let user = { username: 'username', is_admin: false, tokens: 0 };
	let username = '';
	let password = '';
	let error = '';

	onMount(() => {
		const session = localStorage.getItem('session');
		if (session === null) {
			goto('/login');
			return;
		}
		fetch(`${BACKEND_URL}/users/by/session?session=${session}`, {
			method: 'GET'
		})
			.then(async (response) => {
				user = await response.json();
				if (!user.is_admin) {
					goto('/');
				}
			})
			.catch((err) => {
				console.error(err);
			});
	});

	const handleCreate = async () => {
		try {
			const response = await fetch(
				`${BACKEND_URL}/users/create?session=${localStorage.getItem('session')}&username=${username}&password=${password}`,
				{ method: 'POST' }
			);
			if (response.ok) {
				goto('/');
			} else {
				const errorData = await response.json();
				console.error('Authentication failed:', errorData);
				error = errorData.detail;
			}
		} catch (err) {
			console.error('Authentication error:', err);
			error = String(err);
		}
	};
</script>

<div class="w-1/2">
	<h1 class="text-center mb-10 text-slate-100 font-bold text-xl">Create new account</h1>
	<form on:submit|preventDefault={handleCreate} class="flex flex-col">
		<p class="text-slate-100 text-sm">Username</p>
		<input
			bind:value={username}
			class="mb-5 border rounded-md bg-gray-800 border-gray-700 p-1 text-slate-100"
		/>
		<p class="text-slate-100 text-sm">Password</p>
		<input
			bind:value={password}
			type="password"
			class="mb-5 border rounded-md bg-gray-800 border-gray-700 p-1 text-slate-100"
		/>
		<button type="submit" class="text-slate-100 text-sm rounded-md p-1 bg-indigo-700">Create</button
		>
	</form>
</div>
{#if error}
	<p class="bg-red-700 mt-3 rounded-md p-1 w-1/2 text-slate-100 text-center">{error}</p>
{/if}
