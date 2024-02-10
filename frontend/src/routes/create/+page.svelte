<script lang="ts">
	import { goto } from '$app/navigation';
	import FetchStatus from '$lib/FetchStatus.svelte';
	import { createUser, getUser, type User } from '$lib/api';
	import { NotificationType, notification } from '$lib/store';
	import { onMount } from 'svelte';

	let session: string;
	let user: User;
	let username = '';
	let password = '';
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

	const handleCreate = async () => {
		if (password.search(/\d/g) < 0) throw new Error('Password must contain digit');
		if (password.search(/[a-z]/g) < 0) throw new Error('Password must contain lower letter');
		if (password.search(/[A-Z]/g) < 0) throw new Error('Password must contain upper letter');

		await createUser(session, username, password);
		notification.set({
			message: `Account \'${username}\' created`,
			type: NotificationType.SUCCESS
		});
		goto('/');
	};
</script>

<div class="w-1/2">
	<h1 class="text-center mb-10 text-slate-100 font-bold text-xl">Create new account</h1>
	<form on:submit|preventDefault={() => (promise = handleCreate())} class="flex flex-col">
		<p class="text-slate-100 text-sm">Username</p>
		<input
			bind:value={username}
			class="mb-5 border rounded-md bg-gray-800 border-gray-700 p-1 text-slate-100"
		/>
		<p class="text-slate-100 text-sm">Password</p>
		<input
			minlength="8"
			bind:value={password}
			type="password"
			class="mb-5 border rounded-md bg-gray-800 border-gray-700 p-1 text-slate-100"
		/>
		<button type="submit" class="text-slate-100 text-sm rounded-md p-1 bg-indigo-700">Create</button
		>
	</form>
</div>

<div class="w-full h-8">
	<FetchStatus {promise} />
</div>
