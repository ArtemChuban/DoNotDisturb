<script lang="ts">
	import { goto } from '$app/navigation';
	import { transfer } from '$lib/api';
	import FetchStatus from '$lib/FetchStatus.svelte';
	import UserSelect from '$lib/UserSelect.svelte';
	import { t } from '$lib/i18n';
	import { session } from '$lib/user';
	import { getToastStore } from '@skeletonlabs/skeleton';
	const toastStore = getToastStore();

	let username = '';
	let value = '';
	let promise: Promise<void>;

	$: value = value.replace(/\D/g, '');

	const handleReward = async () => {
		if ($session === null) return;
		await transfer($session, username, +value);
		toastStore.trigger({
			message: `${value} token${+value === 1 ? '' : 's'} transfered to ${username}`,
			background: 'variant-filled-success'
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
