<script lang="ts">
	import { goto } from '$app/navigation';

	let username = '';
	let password = '';

	const handleLogin = async () => {
		console.log(username, password);
		goto('/');
	};
</script>

<div class="flex flex-col gap-4 text-center">
	<span class="text-2xl font-bold">Login</span>
	<input type="text" class="input" placeholder="Username" bind:value={username} />
	<input type="password" class="input" placeholder="Password" bind:value={password} />
	<button type="button" class="btn variant-filled-primary" on:click={handleLogin}>Login</button>
	<a href="/register" class="anchor">I don't have an account</a>
</div>
