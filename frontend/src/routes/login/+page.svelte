<script>
	import { goto } from '$app/navigation';
	import { BACKEND_URL } from '$lib/api';
	import { onMount } from 'svelte';

	onMount(() => {
		if (localStorage.getItem('token') !== null) {
			goto('/');
		}
	});

	let username = '';
	let password = '';
	let error = '';

	const handleLogin = async () => {
		try {
			const response = await fetch(
				`${BACKEND_URL}/users/token?username=${username}&password=${password}`,
				{ method: 'GET' }
			);
			if (response.ok) {
				const token = await response.json();
				localStorage.setItem('token', token);
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

<div class="flex flex-col items-center h-[100dvh] justify-center bg-slate-900">
	<div class="w-1/2">
		<h1 class="text-center mb-10 text-slate-100 font-bold text-xl">Sign in to your account</h1>
		<form on:submit|preventDefault={handleLogin} class="flex flex-col">
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
			<button type="submit" class="text-slate-100 text-sm rounded-md p-1 bg-indigo-700"
				>Sign in</button
			>
		</form>
	</div>
	{#if error}
		<p class="bg-red-700 mt-3 rounded-md p-1 w-1/2 text-slate-100 text-center">{error}</p>
	{/if}
</div>
