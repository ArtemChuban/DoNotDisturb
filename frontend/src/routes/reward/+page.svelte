<script lang="ts">
	import { onMount } from 'svelte';
	import { goto } from '$app/navigation';
	import { getUser, reward } from '$lib/api';
	import FetchStatus from '$lib/FetchStatus.svelte';
	import { notification, NotificationType } from '$lib/notification';
	import UserSelect from '$lib/UserSelect.svelte';
	import { t } from '$lib/i18n';
	import { session } from '$lib/user';

	let username = '';
	let value = '';
	let promise: Promise<void>;

	onMount(async () => {
		session.subscribe(async (value) => {
			if (value === null) return;
			if (!(await getUser(value)).is_admin) goto('/');
		});
	});

	const handleReward = async () => {
		if ($session === null) return;
		await reward($session, username, +value);
		notification.set({
			message: `${username} rewarded for ${value} token${+value === 1 ? '' : 's'}`,
			type: NotificationType.SUCCESS
		});
		goto('/');
	};
</script>

<svelte:head>
	<title>Reward</title>
</svelte:head>

<div class="w-1/2">
	<h1 class="text-center mb-10 text-slate-100 font-bold text-xl">{$t('reward.title')}</h1>
	<form on:submit|preventDefault={() => (promise = handleReward())} class="flex flex-col">
		<p class="text-slate-100 text-sm">{$t('username')}</p>
		<UserSelect bind:username />
		<p class="mt-3 text-slate-100 text-sm">{$t('value')}</p>
		<input
			bind:value
			type="number"
			class="mb-5 border rounded-md bg-gray-800 border-gray-700 p-1 text-slate-100"
		/>
		<button type="submit" class="text-slate-100 text-sm rounded-md p-1 bg-indigo-700"
			>{$t('reward.button')}</button
		>
	</form>
</div>

<div class="w-full h-8">
	<FetchStatus {promise} />
</div>
