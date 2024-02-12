<script lang="ts">
	import { getAllUsers } from '$lib/api';
	import { onMount } from 'svelte';

	export let username: string;
	export let additional: Array<string> = [];
	let usernames: Array<string> = [];
	let promise: Promise<void>;

	const getUsernames = async () => {
		usernames = [...(await getAllUsers()).map((user) => user.username), ...additional];
	};

	onMount(async () => {
		promise = getUsernames();
	});
</script>

{#await promise}
	<div class="bg-slate-800 p-1 rounded-md w-full animate-pulse"><wbr /></div>
{:then}
	<select class="bg-slate-800 p-1 rounded-md w-full" bind:value={username}>
		{#each usernames as username}
			<option value={username}>{username}</option>
		{/each}
	</select>
{:catch}
	<div class="bg-slate-800 p-1 rounded-md w-full"><wbr /></div>
{/await}
