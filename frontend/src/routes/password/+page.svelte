<script lang="ts">
	import { goto } from '$app/navigation';
	import FetchStatus from '$lib/FetchStatus.svelte';
	import UserSelect from '$lib/UserSelect.svelte';
	import { changePassword, getUser } from '$lib/api';
	import { onMount } from 'svelte';
	import { t } from '$lib/i18n';
	import { session } from '$lib/user';
	import PasswordInput from '$lib/PasswordInput.svelte';
	import { getToastStore } from '@skeletonlabs/skeleton';
	const toastStore = getToastStore();

	let is_admin = false;
	let username = '';
	let password = '';
	let confirm_password = '';
	let promise: Promise<void>;

	onMount(async () => {
		session.subscribe(async (value) => {
			if (value === null) return;
			const user = await getUser(value);
			is_admin = user.is_admin;
			username = user.username;
		});
	});

	const handleChange = async () => {
		if ($session === null) return;
		if (password !== confirm_password) throw new Error('wrong repeat password');
		if (password.search(/\d/g) < 0) throw new Error('Password must contain digit');
		if (password.search(/[a-z]/g) < 0) throw new Error('Password must contain lower letter');
		if (password.search(/[A-Z]/g) < 0) throw new Error('Password must contain upper letter');

		await changePassword($session, username, password);
		toastStore.trigger({ message: 'Password changed' });
		goto('/');
	};
</script>

<svelte:head>
	<title>Password</title>
</svelte:head>

<div class="w-2/3">
	<h1 class="text-center mb-10 text-slate-100 font-bold text-xl">{$t('password.title')}</h1>
	<form on:submit|preventDefault={() => (promise = handleChange())} class="flex flex-col">
		{#if is_admin}
			<p class="text-slate-100 text-sm">{$t('username')}</p>
			<UserSelect bind:username />
		{/if}
		<div class="my-2">
			<PasswordInput bind:password title={'password.new'} />
		</div>
		<PasswordInput bind:password={confirm_password} title={'password.repeat'} />
		<button type="submit" class="btn variant-filled-surface text-sm rounded-md mt-5"
			>{$t('password.button')}</button
		>
	</form>
</div>

<div class="w-full h-8">
	<FetchStatus {promise} />
</div>
