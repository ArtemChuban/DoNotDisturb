<script lang="ts">
	import { onMount } from 'svelte';
	import { goto } from '$app/navigation';
	import { getUser, reward, type User } from '$lib/api';
	import FetchStatus from '$lib/FetchStatus.svelte';
	import { notification, NotificationType } from '$lib/store';
	import UserSelect from '$lib/UserSelect.svelte';

	let session: string;
	let user: User;
	let username = '';
	let value = '';
	let promise: Promise<void>;

	onMount(async () => {
		const s = localStorage.getItem('session');
		if (s === null) {
			goto('/login');
			return;
		}
		session = s;
		user = await getUser();
		if (!user.is_admin) goto('/');
	});

	const handleReward = async () => {
		await reward(session, username, +value);
		notification.set({
			message: `${username} rewarded for ${value} token${+value === 1 ? '' : 's'}`,
			type: NotificationType.SUCCESS
		});
		goto('/');
	};
</script>

<div class="w-1/2">
	<h1 class="text-center mb-10 text-slate-100 font-bold text-xl">Reward</h1>
	<form on:submit|preventDefault={() => (promise = handleReward())} class="flex flex-col">
		<p class="text-slate-100 text-sm">Username</p>
		<UserSelect bind:username />
		<p class="mt-3 text-slate-100 text-sm">Value</p>
		<input
			bind:value
			type="number"
			class="mb-5 border rounded-md bg-gray-800 border-gray-700 p-1 text-slate-100"
		/>
		<button type="submit" class="text-slate-100 text-sm rounded-md p-1 bg-indigo-700">Reward</button
		>
	</form>
</div>

<div class="w-full h-8">
	<FetchStatus {promise} />
</div>
