<script lang="ts">
	import { goto } from '$app/navigation';
	import { get_session_token } from '$lib/api';
	import { session } from '$lib/storage';
	import { ProgressRadial, getToastStore } from '@skeletonlabs/skeleton';
	import { onMount } from 'svelte';

	const toastStore = getToastStore();

	let username = '';
	let password = '';
	let loading = false;

	onMount(() => {
		if ($session !== null) goto('/');
	});

	const handleLogin = () => {
		if (username.length < 1 || password.length < 1) {
			toastStore.trigger({
				message: "Login or password can't be empty",
				background: 'variant-filled-error'
			});
			return;
		}
		loading = true;
		get_session_token(username, password)
			.then((value) => {
				$session = value;
				goto('/');
			})
			.catch((error) => {
				toastStore.trigger({ message: error, background: 'variant-filled-error' });
				loading = false;
			});
	};
</script>

<div class="flex flex-col gap-4 text-center">
	<span class="text-2xl font-bold">Login</span>
	<input
		type="text"
		disabled={loading}
		class="input"
		placeholder="Username"
		bind:value={username}
	/>
	<input
		type="password"
		disabled={loading}
		class="input"
		placeholder="Password"
		bind:value={password}
	/>
	<button
		type="button"
		disabled={loading}
		class="btn variant-filled-primary"
		on:click={handleLogin}
	>
		{#if loading}
			<ProgressRadial width="w-6" />
		{:else}
			<span>Login</span>
		{/if}
	</button>
	<a href="/register" class="anchor">I don't have an account</a>
</div>
