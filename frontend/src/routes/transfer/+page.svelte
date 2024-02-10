<script lang="ts">
	import { onMount } from 'svelte';
	import { goto } from '$app/navigation';
	import { getAllUsers, transfer, type User } from '$lib/api';
	import FetchStatus from '$lib/FetchStatus.svelte';
	import UserSelect from '$lib/UserSelect.svelte';
	import { notification, NotificationType } from '$lib/store';

	let username = '';
	let value = '';
	let promise: Promise<void>;
	let users: Array<User> = [];

	$: value = value.replace(/\D/g, '');

	onMount(async () => {
		const session = localStorage.getItem('session');
		if (session === null) {
			goto('/login');
			return;
		}
		users = await getAllUsers();
	});

	const handleReward = async () => {
		const session = localStorage.getItem('session');
		if (session === null) throw new Error('Empty session');
		console.log(username);
		await transfer(session, username, +value);
		notification.set({
			message: `${value} token${+value === 1 ? '' : 's'} transfered to ${username}`,
			type: NotificationType.SUCCESS
		});
		goto('/');
	};
</script>

<div class="w-1/2">
	<h1 class="text-center mb-10 text-slate-100 font-bold text-xl">Transfer</h1>
	<form on:submit|preventDefault={() => (promise = handleReward())} class="flex flex-col">
		<p class="text-slate-100 text-sm">Username</p>
		<UserSelect bind:username />
		<p class="mt-3 text-slate-100 text-sm">Value</p>
		<input
			bind:value
			class="mb-5 border rounded-md bg-gray-800 border-gray-700 p-1 text-slate-100"
		/>
		<button type="submit" class="text-slate-100 text-sm rounded-md p-1 bg-indigo-700">Send</button>
	</form>
</div>

<div class="w-full h-8 mt-3">
	<FetchStatus {promise} />
</div>
