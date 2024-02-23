<script lang="ts">
	import { onMount } from 'svelte';
	import { goto } from '$app/navigation';
	import { getUser, reward } from '$lib/api';
	import FetchStatus from '$lib/FetchStatus.svelte';
	import { notification, NotificationType } from '$lib/notification';
	import UserSelect from '$lib/UserSelect.svelte';
	import { t } from '$lib/i18n';
	import { session } from '$lib/user';
	import { writable } from 'svelte/store';
	import { fly } from 'svelte/transition';

	let usernames = writable(new Set<string>());
	let username = writable('');
	let value = '';
	let promise: Promise<void>;
	let selectable: Array<string> = [];

	onMount(async () => {
		session.subscribe(async (value) => {
			if (value === null) return;
			if (!(await getUser(value)).is_admin) goto('/');
		});
	});

	username.subscribe((value) => {
		if (value === '') return;
		$usernames.add($username);
		$usernames = $usernames;
		$username = '';
		selectable.splice(selectable.indexOf(value), 1);
	});

	const deselect = (username: string) => {
		$usernames.delete(username);
		$usernames = $usernames;
		selectable = [...selectable, username];
	};

	const handleReward = async () => {
		$usernames.forEach(async (username) => {
			if ($session === null) return;
			await reward($session, username, +value);
		});
		notification.set({
			message: `${Array.from($usernames)} rewarded for ${value} token${+value === 1 ? '' : 's'}`,
			type: NotificationType.SUCCESS
		});
		goto('/');
	};
</script>

<svelte:head>
	<title>Reward</title>
</svelte:head>

<div class="w-1/2">
	<h1 class="text-center mb-3 text-slate-100 font-bold text-xl">{$t('reward.title')}</h1>
	<form on:submit|preventDefault={() => (promise = handleReward())} class="flex flex-col">
		<p class="text-slate-100 text-sm">{$t('username')}</p>
		<UserSelect bind:username={$username} bind:usernames={selectable} />
		<div class="w-full flex flex-wrap mt-5">
			{#each $usernames as username (username)}
				<button
					transition:fly={{ y: 50 }}
					type="button"
					on:click|preventDefault={() => deselect(username)}
					class="bg-slate-800 rounded-md p-1 mr-2 mb-2">{username}</button
				>
			{/each}
		</div>
		<input bind:value type="number" class="input mb-5" placeholder={$t('value')} />
		<button type="submit" class="btn variant-filled-surface text-sm">{$t('reward.button')}</button>
	</form>
</div>

<div class="w-full h-8">
	<FetchStatus {promise} />
</div>
