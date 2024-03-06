<script lang="ts">
	import { goto } from '$app/navigation';
	import { get_jwt_token } from '$lib/api';
	import { jwt_token } from '$lib/storage';
	import { getToastStore } from '@skeletonlabs/skeleton';

	const toastStore = getToastStore();

	let username = '';
	let password = '';

	const handleLogin = () => {
		if (username.length < 1 || password.length < 1) {
			toastStore.trigger({
				message: "Login or password can't be empty",
				background: 'variant-filled-error'
			});
			return;
		}
		get_jwt_token(username, password)
			.then((value) => {
				$jwt_token = value;
				goto('/');
			})
			.catch((error) => {
				toastStore.trigger({ message: error, background: 'variant-filled-error' });
			});
	};
</script>

<div class="flex flex-col gap-4 text-center">
	<span class="text-2xl font-bold">Login</span>
	<input type="text" class="input" placeholder="Username" bind:value={username} />
	<input type="password" class="input" placeholder="Password" bind:value={password} />
	<button type="button" class="btn variant-filled-primary" on:click={handleLogin}>Login</button>
	<a href="/register" class="anchor">I don't have an account</a>
</div>
