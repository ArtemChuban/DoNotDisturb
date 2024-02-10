<script lang="ts">
	import { goto } from '$app/navigation';
	import FetchStatus from '$lib/FetchStatus.svelte';
	import UserSelect from '$lib/UserSelect.svelte';
	import { type User, changePassword, getUser } from '$lib/api';
	import { NotificationType, notification } from '$lib/store';
	import { onMount } from 'svelte';

	let current_user: User = { username: 'username', is_admin: false, tokens: 0 };
	let username = '';
	let password = '';
	let confirm_password = '';
	let promise: Promise<void>;

	onMount(async () => {
		const session = localStorage.getItem('session');
		if (session === null) {
			goto('/login');
			return;
		}
		current_user = await getUser();
	});

	const handleChange = async () => {
		const session = localStorage.getItem('session');
		if (session === null) throw new Error('Empty session');
		if (password !== confirm_password) throw new Error('wrong repeat password');
		if (password.search(/\d/g) < 0) throw new Error('Password must contain digit');
		if (password.search(/[a-z]/g) < 0) throw new Error('Password must contain lower letter');
		if (password.search(/[A-Z]/g) < 0) throw new Error('Password must contain upper letter');

		await changePassword(
			session,
			current_user.is_admin ? username : current_user.username,
			password
		);
		notification.set({ message: 'Password changed', type: NotificationType.SUCCESS });
		goto('/');
	};
</script>

<div class="w-1/2">
	<h1 class="text-center mb-10 text-slate-100 font-bold text-xl">Change password</h1>
	<form on:submit|preventDefault={() => (promise = handleChange())} class="flex flex-col">
		{#if current_user.is_admin}
			<p class="text-slate-100 text-sm">Username</p>
			<UserSelect bind:username />
		{/if}
		<p class="mt-3 text-slate-100 text-sm">New password</p>
		<input
			minlength="8"
			bind:value={password}
			type="password"
			class="mb-3 border rounded-md bg-gray-800 border-gray-700 p-1 text-slate-100"
		/>
		<p class="text-slate-100 text-sm">Repeat password</p>
		<input
			minlength="8"
			bind:value={confirm_password}
			type="password"
			class="mb-5 border rounded-md bg-gray-800 border-gray-700 p-1 text-slate-100"
		/>
		<button type="submit" class="text-slate-100 text-sm rounded-md p-1 bg-indigo-700">Change</button
		>
	</form>
</div>

<div class="w-full h-8">
	<FetchStatus {promise} />
</div>
