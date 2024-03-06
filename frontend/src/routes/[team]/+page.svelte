<script lang="ts">
	import { page } from '$app/stores';
	import { getModalStore } from '@skeletonlabs/skeleton';
	// @ts-expect-error, no types for this module
	import FaPaperPlane from 'svelte-icons/fa/FaPaperPlane.svelte';
	// @ts-expect-error, no types for this module
	import FaArrowLeft from 'svelte-icons/fa/FaArrowLeft.svelte';
	import { goto } from '$app/navigation';

	const modalStore = getModalStore();

	const teamName = $page.params.team;

	interface IUser {
		id: string;
		username: string;
		tokens: number;
	}

	const users: Array<IUser> = [
		{ id: '1', username: 'user1', tokens: 12 },
		{ id: '2', username: 'user2', tokens: 24 },
		{ id: '3', username: 'user3', tokens: 36 },
		{ id: '4', username: 'user4', tokens: 48 },
		{ id: '5', username: 'user5', tokens: 25 },
		{ id: '6', username: 'user6', tokens: 327 },
		{ id: '7', username: 'user7', tokens: 2 }
	].sort((a, b) => b.tokens - a.tokens);

	const handleTransfer = async (user: IUser) => {
		modalStore.trigger({
			type: 'prompt',
			title: 'Transfer',
			body: `Enter tokens value to transfer to ${user.username}`,
			valueAttr: { type: 'number', required: true },
			response: (value: number) => {
				if (!value) return;
				users[users.indexOf(user)].tokens += value;
			}
		});
	};
</script>

<div class="flex flex-col h-3/4 w-3/4 gap-4">
	<div class="card flex justify-around items-center py-4">
		<button type="button" class="btn btn-icon w-6" on:click={() => goto('/')}
			><FaArrowLeft /></button
		>
		<span class="font-bold text-xl text-primary-500">{teamName}</span>
		<div></div>
	</div>

	<div class="flex flex-col m-1 gap-4 overflow-scroll">
		{#each users as user (user.id)}
			<div class="flex justify-between card p-4">
				<span class="font-bold text-xl">{user.username}</span>
				<span class="font-bold text-xl">{user.tokens}</span>
				<button class="btn btn-icon w-6 text-primary-500" on:click={() => handleTransfer(user)}
					><FaPaperPlane /></button
				>
			</div>
		{/each}
	</div>
</div>
