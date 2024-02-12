<script lang="ts">
	import { goto } from '$app/navigation';
	import FetchStatus from '$lib/FetchStatus.svelte';
	import { createUser, getUser } from '$lib/api';
	import { t } from '$lib/i18n';
	import { NotificationType, notification } from '$lib/notification';
	import { session } from '$lib/user';
	import { onMount } from 'svelte';

	let username = '';
	let password = '';
	let promise: Promise<void>;

	onMount(async () => {
		session.subscribe(async (value) => {
			if (value === null) return;
			if (!(await getUser(value)).is_admin) goto('/');
		});
	});

	const handleCreate = async () => {
		if ($session === null) return;
		if (password.search(/\d/g) < 0) throw new Error('Password must contain digit');
		if (password.search(/[a-z]/g) < 0) throw new Error('Password must contain lower letter');
		if (password.search(/[A-Z]/g) < 0) throw new Error('Password must contain upper letter');

		await createUser($session, username, password);
		notification.set({
			message: `Account \'${username}\' created`,
			type: NotificationType.SUCCESS
		});
		goto('/');
	};
</script>

<svelte:head>
	<title>Create</title>
</svelte:head>

<div class="w-1/2">
	<h1 class="text-center mb-10 text-slate-100 font-bold text-xl">{$t('create.title')}</h1>
	<form on:submit|preventDefault={() => (promise = handleCreate())} class="flex flex-col">
		<p class="text-slate-100 text-sm">{$t('username')}</p>
		<input
			bind:value={username}
			class="mb-5 border rounded-md bg-gray-800 border-gray-700 p-1 text-slate-100"
		/>
		<p class="text-slate-100 text-sm">{$t('password')}</p>
		<input
			minlength="8"
			bind:value={password}
			type="password"
			class="mb-5 border rounded-md bg-gray-800 border-gray-700 p-1 text-slate-100"
		/>
		<button type="submit" class="text-slate-100 text-sm rounded-md p-1 bg-indigo-700"
			>{$t('create.button')}</button
		>
	</form>
</div>

<div class="w-full h-8">
	<FetchStatus {promise} />
</div>
