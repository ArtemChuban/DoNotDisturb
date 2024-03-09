<script lang="ts">
	import { getModalStore, getToastStore } from '@skeletonlabs/skeleton';
	// @ts-expect-error, no types for this module
	import FaPaperPlane from 'svelte-icons/fa/FaPaperPlane.svelte';
	// @ts-expect-error, no types for this module
	import FaArrowLeft from 'svelte-icons/fa/FaArrowLeft.svelte';
	// @ts-expect-error, no types for this module
	import FaAward from 'svelte-icons/fa/FaAward.svelte';
	// @ts-expect-error, no types for this module
	import FaPlus from 'svelte-icons/fa/FaPlus.svelte';

	import { goto } from '$app/navigation';
	import { currentTeam, session, user } from '$lib/storage';
	import { getMembers, inviteMember, type IMember, transfer, reward } from '$lib/api';
	import { onMount } from 'svelte';
	import { config } from '$lib/config';
	import { fly } from 'svelte/transition';

	const toastStore = getToastStore();
	const modalStore = getModalStore();

	onMount(async () => {
		if ($currentTeam.members.length > 0) return;
		if ($session === null) {
			goto('/login');
			return;
		}
		if ($currentTeam.name === '') {
			goto('/');
			return;
		}
		getMembers($session, $currentTeam.id)
			.then((members) => {
				$currentTeam.members = members.sort((a, b) => b.tokens - a.tokens);
			})
			.catch((error) => {
				toastStore.trigger({ message: error, background: 'variant-filled-error' });
				goto('/');
			});
	});

	const handleTransfer = async (member: IMember) => {
		modalStore.trigger({
			type: 'prompt',
			title: 'Transfer',
			body: `Enter tokens value to transfer to ${member.username}`,
			valueAttr: { type: 'number', required: true, min: 1 },
			response: (value: number) => {
				if (!value || $session === null) return;
				const user_as_member = $currentTeam.members.find(
					(member) => member.username === $user.username
				);
				if (user_as_member === undefined) return;
				if (user_as_member.tokens < value) {
					toastStore.trigger({
						message: "You don't have enough tokens",
						background: 'variant-filled-error'
					});
					return;
				}
				transfer($session, $currentTeam.id, member.id, value)
					.then(() => {
						member.tokens += value;
						user_as_member.tokens -= value;
						$currentTeam.members = $currentTeam.members.sort((a, b) => b.tokens - a.tokens);
						$currentTeam = $currentTeam;
					})
					.catch((error) => {
						toastStore.trigger({ message: error, background: 'variant-filled-error' });
					});
			}
		});
	};

	const handleReward = async (member: IMember) => {
		modalStore.trigger({
			type: 'prompt',
			title: 'Reward',
			body: `Enter tokens value to reward ${member.username}`,
			valueAttr: { type: 'number', required: true, min: 1 },
			response: (value: number) => {
				if (!value || $session === null) return;
				reward($session, $currentTeam.id, member.id, value)
					.then(() => {
						member.tokens += value;
						$currentTeam.members = $currentTeam.members.sort((a, b) => b.tokens - a.tokens);
						$currentTeam = $currentTeam;
					})
					.catch((error) => {
						toastStore.trigger({ message: error, background: 'variant-filled-error' });
					});
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
				if (!value || $session === null) return;
				inviteMember($session, $currentTeam.id, value)
					.then(() => {})
					.catch((error) => {
						toastStore.trigger({ message: error, background: 'variant-filled-error' });
					});
			}
		});
	};
</script>

<div class="flex flex-col h-3/4 w-3/4 gap-4">
	<div class="card flex justify-around items-center py-4">
		<button type="button" class="btn btn-icon w-6" on:click={() => goto('/')}
			><FaArrowLeft /></button
		>
		<span class="font-bold text-xl text-primary-500">{$currentTeam.name}</span>
		<div></div>
	</div>

	<div class="flex flex-col m-1 gap-4 overflow-scroll">
		{#each $currentTeam.members as member, index (member.id)}
			<div
				class="flex justify-around card p-4"
				in:fly={{
					duration: config.duration,
					delay: index * config.delay,
					y: config.offset
				}}
			>
				<span
					class="font-bold text-xl w-1/3 overflow-hidden {member.username === $user.username
						? 'text-primary-500'
						: ''}"
				>
					{member.username}
				</span>
				<span class="font-bold text-xl w-1/3 text-center overflow-hidden">{member.tokens}</span>
				<div class="flex justify-end gap-4 w-1/3">
					{#if member.username !== $user.username}
						<button
							class="btn btn-icon w-6 text-secondary-500"
							on:click={() => handleTransfer(member)}
						>
							<FaPaperPlane />
						</button>
					{/if}
					{#if $user.isAdmin}
						<button class="btn btn-icon w-6 text-success-500" on:click={() => handleReward(member)}>
							<FaAward />
						</button>
					{/if}
				</div>
			</div>
		{/each}
		{#if $user.isAdmin}
			<button class="flex justify-between font-bold btn card p-4" on:click={handleInvite}>
				<span>Invite team member</span>
				<div class="w-6 text-success-500"><FaPlus /></div>
			</button>
		{/if}
	</div>
</div>
