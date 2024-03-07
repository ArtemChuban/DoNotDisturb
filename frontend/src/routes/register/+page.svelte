<script lang="ts">
	import { goto } from '$app/navigation';
	import { createAccount } from '$lib/api';
	import { session } from '$lib/storage';
	import { getToastStore } from '@skeletonlabs/skeleton';
	import { onMount } from 'svelte';

	const toastStore = getToastStore();

	let username = '';
	let password = '';
	let password_repeat = '';

	onMount(() => {
		if ($session !== null) goto('/');
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
		createAccount(username, password)
			.then((value) => {
				$session = value;
				goto('/');
			})
			.catch((error) => {
				toastStore.trigger({ message: error, background: 'variant-filled-error' });
			});
	};
</script>

<div class="flex flex-col gap-4 text-center">
	<span class="text-2xl font-bold">Create account</span>
	<input type="text" class="input" placeholder="Username" bind:value={username} />
	<input type="password" class="input" placeholder="Password" bind:value={password} />
	<input type="password" class="input" placeholder="Repeat password" bind:value={password_repeat} />
	<button type="button" class="btn variant-filled-primary" on:click={handleLogin}>Login</button>
	<a href="/login" class="anchor">I have an account</a>
</div>
