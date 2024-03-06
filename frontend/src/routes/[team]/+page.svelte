<script lang="ts">
	import { page } from '$app/stores';
	import { getModalStore } from '@skeletonlabs/skeleton';
	// @ts-expect-error, no types for this module
	import FaPaperPlane from 'svelte-icons/fa/FaPaperPlane.svelte';
	// @ts-expect-error, no types for this module
	import FaArrowLeft from 'svelte-icons/fa/FaArrowLeft.svelte';
	// @ts-expect-error, no types for this module
	import FaAward from 'svelte-icons/fa/FaAward.svelte';
	// @ts-expect-error, no types for this module
	import FaPlus from 'svelte-icons/fa/FaPlus.svelte';

	import { goto } from '$app/navigation';

	const modalStore = getModalStore();

	const teamName = $page.params.team;
	const isAdmin = false;
	const username = 'user';

	interface IUser {
		id: string;
		username: string;
		tokens: number;
	}

	let users: Array<IUser> = [
		{ id: '1', username: 'user1', tokens: 12 },
		{ id: '2', username: 'user2', tokens: 24 },
		{ id: '3', username: 'user', tokens: 36 },
		{ id: '4', username: 'user4', tokens: 48 },
		{ id: '5', username: 'ashjfioefesa', tokens: 25 },
		{ id: '6', username: 'user6', tokens: 327 },
		{ id: '7', username: 'user7', tokens: 2 }
	].sort((a, b) => b.tokens - a.tokens);

	$: users = users.sort((a, b) => b.tokens - a.tokens);

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

	const handleReward = async (user: IUser) => {
		modalStore.trigger({
			type: 'prompt',
			title: 'Reward',
			body: `Enter tokens value to reward ${user.username}`,
			valueAttr: { type: 'number', required: true },
			response: (value: number) => {
				if (!value) return;
				users[users.indexOf(user)].tokens += value;
			}
		});
	};

	const handleInvite = async () => {
		modalStore.trigger({
			type: 'prompt',
			title: 'Invite',
			body: `Enter username`,
			valueAttr: { type: 'text', required: true },
			response: (value: string) => {
				if (!value) return;
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
			<div class="flex justify-around card p-4">
				<span
					class="font-bold text-xl w-1/3 overflow-hidden {user.username === username
						? 'text-primary-500'
						: ''}"
				>
					{user.username}
				</span>
				<span class="font-bold text-xl w-1/3 text-center overflow-hidden">{user.tokens}</span>
				<div class="flex justify-end gap-4 w-1/3">
					{#if user.username !== username}
						<button
							class="btn btn-icon w-6 text-secondary-500"
							on:click={() => handleTransfer(user)}
						>
							<FaPaperPlane />
						</button>
						{#if isAdmin}
							<button class="btn btn-icon w-6 text-success-500" on:click={() => handleReward(user)}>
								<FaAward />
							</button>
						{/if}
					{/if}
				</div>
			</div>
		{/each}
		{#if isAdmin}
			<button class="flex justify-between font-bold btn card p-4" on:click={handleInvite}>
				<span>Invite team member</span>
				<div class="w-6 text-success-500"><FaPlus /></div>
			</button>
		{/if}
	</div>
</div>
