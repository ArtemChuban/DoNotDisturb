<script lang="ts">
	import { updateAccount } from '$lib/api';
	import { session, user } from '$lib/storage';
	import { ProgressRadial, getToastStore } from '@skeletonlabs/skeleton';
	import { push } from 'svelte-spa-router';

	let loading = true;
	let username = $user.username;
	let password = '';
	let password_repeat = '';
	const toastStore = getToastStore();

	user.subscribe((value) => {
		if (value.username === '') return;
		loading = false;
		username = value.username;
	});

	const handleUpdate = () => {
		if (password.length < 1) {
			toastStore.trigger({
				message: "Password can't be empty",
				background: 'variant-filled-error'
			});
			return;
		}
		if (password !== password_repeat) {
			toastStore.trigger({
				message: 'Passwords must match',
				background: 'variant-filled-error'
			});
			return;
		}
		loading = true;
		updateAccount($session!, password)
			.then(() => {
				toastStore.trigger({ message: 'Password changed', background: 'variant-filled-success' });
				push('/');
			})
			.catch((error) => {
				toastStore.trigger({ message: error, background: 'variant-filled-error' });
				loading = false;
			});
	};
</script>

<div class="flex flex-col gap-4 text-center">
	<span class="text-2xl font-bold">Change user info</span>
	<input
		type="text"
		disabled={true}
		class="input"
		placeholder="New username"
		bind:value={username}
	/>
	<input
		type="password"
		disabled={loading}
		class="input"
		placeholder="New password"
		bind:value={password}
	/>
	<input
		type="password"
		disabled={loading}
		class="input"
		placeholder="Repeat new password"
		bind:value={password_repeat}
	/>
	<div class="w-full flex justify-around gap-4">
		<button
			type="button"
			disabled={loading}
			class="btn variant-filled-primary w-full"
			on:click={() => push('/')}
		>
			<span>Back</span>
		</button>
		<button
			type="button"
			disabled={loading}
			class="btn variant-filled-primary w-full"
			on:click={handleUpdate}
		>
			{#if loading}
				<ProgressRadial width="w-6" />
			{:else}
				<span>Save</span>
			{/if}
		</button>
	</div>
</div>
