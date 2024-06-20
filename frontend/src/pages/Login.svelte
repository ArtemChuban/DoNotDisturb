<script lang="ts">
	import { get_session_token } from '$lib/api';
	import { session } from '$lib/storage';
	import { ProgressRadial, getToastStore } from '@skeletonlabs/skeleton';
	import { push } from 'svelte-spa-router';
	import { _ } from 'svelte-i18n';

	const toastStore = getToastStore();

	let username = '';
	let password = '';
	let loading = false;

	const handleLogin = () => {
		if (username.length < 1 || password.length < 1) {
			toastStore.trigger({
				message: $_('login.messages.empty'),
				background: 'variant-filled-error'
			});
			return;
		}
		loading = true;
		get_session_token(username, password)
			.then((value) => {
				$session = value;
				push('/');
			})
			.catch((error) => {
				toastStore.trigger({ message: error, background: 'variant-filled-error' });
				loading = false;
			});
	};
</script>

<div class="flex flex-col gap-4 text-center">
	<span class="text-2xl font-bold">{$_('login.title')}</span>
	<input
		type="text"
		disabled={loading}
		class="input"
		placeholder={$_('login.placeholder.username')}
		bind:value={username}
	/>
	<input
		type="password"
		disabled={loading}
		class="input"
		placeholder={$_('login.placeholder.password')}
		bind:value={password}
	/>
	<button
		type="button"
		disabled={loading}
		class="btn variant-filled-primary"
		on:click={handleLogin}
	>
		{#if loading}
			<ProgressRadial width="w-6" />
		{:else}
			<span>{$_('login.button')}</span>
		{/if}
	</button>
	<a href="/register" class="anchor">{$_('login.registerLink')}</a>
</div>
