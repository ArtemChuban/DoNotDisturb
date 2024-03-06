<script lang="ts">
	import { goto } from '$app/navigation';

	let username = '';
	let password = '';
	let password_repeat = '';

	const handleLogin = async () => {
		console.log(username, password, password_repeat);
		goto('/');
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
