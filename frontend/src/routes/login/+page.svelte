<script lang="ts">
	import { goto } from '$app/navigation';
	import FetchStatus from '$lib/FetchStatus.svelte';
	import PasswordInput from '$lib/PasswordInput.svelte';
	import { getSession } from '$lib/api';
	import { t } from '$lib/i18n';
	import { session } from '$lib/user';

	let username = '';
	let password = '';

	let promise: Promise<void>;

	const handleLogin = async () => {
		$session = await getSession(username, password);
		goto('/');
	};
</script>

<svelte:head>
	<title>Login</title>
</svelte:head>

<div class="w-1/2">
	<h1 class="text-center mb-10 text-slate-100 font-bold text-xl">{$t('login.title')}</h1>
	<form on:submit|preventDefault={() => (promise = handleLogin())} class="flex flex-col">
		<p class="text-slate-100 text-sm">{$t('username')}</p>
		<input
			bind:value={username}
			class="mb-5 border rounded-md bg-gray-800 border-gray-700 p-1 text-slate-100"
		/>
		<PasswordInput bind:password />
		<button type="submit" class="mt-5 text-slate-100 text-sm rounded-md p-1 bg-indigo-700"
			>{$t('login.button')}</button
		>
	</form>
</div>

<div class="w-full h-8">
	<FetchStatus {promise} />
</div>
