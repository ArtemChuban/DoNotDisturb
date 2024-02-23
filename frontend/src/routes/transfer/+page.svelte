<script lang="ts">
	import { onMount } from 'svelte';
	import { goto } from '$app/navigation';
	import { getAllUsers, transfer, type User } from '$lib/api';
	import FetchStatus from '$lib/FetchStatus.svelte';
	import UserSelect from '$lib/UserSelect.svelte';
	import { notification, NotificationType } from '$lib/notification';
	import { t } from '$lib/i18n';
	import { session } from '$lib/user';

	let username = '';
	let value = '';
	let promise: Promise<void>;
	let users: Array<User> = [];

	$: value = value.replace(/\D/g, '');

	onMount(async () => {
		users = await getAllUsers();
	});

	const handleReward = async () => {
		if ($session === null) return;
		await transfer($session, username, +value);
		notification.set({
			message: `${value} token${+value === 1 ? '' : 's'} transfered to ${username}`,
			type: NotificationType.SUCCESS
		});
		goto('/');
	};
</script>

<svelte:head>
	<title>Transfer</title>
</svelte:head>

<div class="w-1/2">
	<h1 class="text-center mb-10 text-slate-100 font-bold text-xl">{$t('transfer.title')}</h1>
	<form on:submit|preventDefault={() => (promise = handleReward())} class="flex flex-col">
		<p class="text-slate-100 text-sm">{$t('username')}</p>
		<UserSelect bind:username />
		<input bind:value class="input my-5 text-slate-100" placeholder={$t('value')} />
		<button type="submit" class="btn variant-filled-surface text-sm rounded-md"
			>{$t('transfer.button')}</button
		>
	</form>
</div>

<div class="w-full h-8 mt-3">
	<FetchStatus {promise} />
</div>
