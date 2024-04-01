<script lang="ts">
	import { createAccount } from '$lib/api';
	import { session } from '$lib/storage';
	import { ProgressRadial, getToastStore } from '@skeletonlabs/skeleton';
	import { onMount } from 'svelte';
	import { push } from 'svelte-spa-router';

	const toastStore = getToastStore();

	let username = '';
	let password = '';
	let password_repeat = '';
	let loading = false;

	onMount(() => {
		if ($session !== null) push('/');
	});

	const handleLogin = async () => {
		if (username.length < 1 || password.length < 1) {
			toastStore.trigger({
				message: "Login or password can't be empty",
				background: 'variant-filled-error'
			});
			return;
		}
		if (password !== password_repeat) {
			toastStore.trigger({
				message: 'Passwords must match',
				background: 'variant-filled-error'
			});
			return;
		}
		loading = true;
		createAccount(username, password)
			.then((value) => {
				$session = value;
				push('/');
			})
			.catch((error) => {
				toastStore.trigger({ message: error, background: 'variant-filled-error' });
				loading = false;
			});
	};
</script>

<div class="flex flex-col gap-4 text-center">
	<span class="text-2xl font-bold">Create account</span>
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
	<input
		type="password"
		disabled={loading}
		class="input"
		placeholder="Repeat password"
		bind:value={password_repeat}
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
			<span>Register</span>
		{/if}
	</button>
	<a href="/login" class="anchor">I have an account</a>
</div>
