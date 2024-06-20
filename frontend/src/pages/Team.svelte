<script lang="ts">
	import { ProgressRadial, getModalStore, getToastStore } from '@skeletonlabs/skeleton';
	// @ts-expect-error, no types for this module
	import FaPaperPlane from 'svelte-icons/fa/FaPaperPlane.svelte';
	// @ts-expect-error, no types for this module
	import FaArrowLeft from 'svelte-icons/fa/FaArrowLeft.svelte';
	// @ts-expect-error, no types for this module
	import FaAward from 'svelte-icons/fa/FaAward.svelte';
	// @ts-expect-error, no types for this module
	import FaPlus from 'svelte-icons/fa/FaPlus.svelte';
	// @ts-expect-error, no types for this module
	import FaHistory from 'svelte-icons/fa/FaHistory.svelte';

	import { session, user } from '$lib/storage';
	import { getMembers, inviteMember, type IMember, transfer, type ITeam } from '$lib/api';
	import { onMount } from 'svelte';
	import { config } from '$lib/config';
	import { fly } from 'svelte/transition';
	import { push } from 'svelte-spa-router';
	import { _ } from 'svelte-i18n';

	export let params: { id: string };
	const toastStore = getToastStore();
	const modalStore = getModalStore();
	let isAdmin = false;
	let loading = false;
	let totalTokens = 0;
	let currentTeam: ITeam = { id: '', members: [], name: '' };

	$: totalTokens = currentTeam.members
		.map((member) => member.tokens)
		.reduce((sum, value) => sum + value, 0);
	$: currentTeam.members.forEach((member) => {
		if (member.username === $user.username) isAdmin = member.is_admin;
	});

	onMount(() => {
		user.subscribe((value) => {
			if (value.username === '') return;
			currentTeam = value.teams[params.id];
			if (currentTeam.members.length > 0) return;
			loading = true;
			getMembers($session!, currentTeam.id)
				.then((members) => {
					if (currentTeam === undefined) return;
					currentTeam.members = members.sort((a, b) => b.tokens - a.tokens);
					loading = false;
				})
				.catch((error) => {
					toastStore.trigger({ message: error, background: 'variant-filled-error' });
					push('/');
				});
		});
	});

	const handleTransfer = async (member: IMember) => {
		modalStore.trigger({
			type: 'prompt',
			title: $_('team.transfer.title'),
			body: $_('team.transfer.body.value'),
			valueAttr: { type: 'number', required: true, min: 1 },
			response: (value: number) => {
				if (!value) return;
				modalStore.trigger({
					type: 'prompt',
					title: $_('team.transfer.title'),
					body: $_('team.transfer.body.description'),
					valueAttr: { type: 'string', required: true },
					response: (description: string) => {
						const user_as_member = currentTeam.members.find(
							(member) => member.username === $user.username
						);
						if (user_as_member === undefined) return;
						if (user_as_member.tokens < value) {
							toastStore.trigger({
								message: $_('team.messages.lowTokens'),
								background: 'variant-filled-error'
							});
							return;
						}
						transfer($session!, currentTeam.id, member.id, value, description)
							.then(() => {
								member.tokens += value;
								user_as_member.tokens -= value;
								currentTeam.members = currentTeam.members.sort((a, b) => b.tokens - a.tokens);
								currentTeam = currentTeam;
							})
							.catch((error) => {
								toastStore.trigger({ message: error, background: 'variant-filled-error' });
							});
					}
				});
			}
		});
	};

	const handleInvite = async () => {
		modalStore.trigger({
			type: 'prompt',
			title: $_('team.invite.title'),
			body: $_('team.invite.body'),
			valueAttr: { type: 'text', required: true },
			response: (value: string) => {
				if (!value) return;
				inviteMember($session!, currentTeam.id, value)
					.then(() => {})
					.catch((error) => {
						toastStore.trigger({ message: error, background: 'variant-filled-error' });
					});
			}
		});
	};

	const getPercentage = (value: number, total: number): number => {
		if (total === 0) {
			return 0;
		}
		return Math.floor((value / total) * 100_0) / 10;
	};
</script>

<div class="flex flex-col h-3/4 w-3/4 gap-4">
	<div class="card flex justify-around items-center py-4">
		<button type="button" class="btn btn-icon w-6" on:click={() => push('/')}
			><FaArrowLeft /></button
		>
		<span class="font-bold text-xl text-primary-500">{currentTeam.name}</span>
		<span class="font-bold text-xl text-primary-500">{totalTokens}</span>
		{#if isAdmin}
			<button
				class="btn btn-icon w-6 text-success-500"
				on:click={() => push(`/team/${currentTeam.id}/reward`)}
			>
				<FaAward />
			</button>
		{/if}
		<button
			class="w-6 text-secondary-500"
			on:click={() => push(`/team/${currentTeam.id}/transactions`)}><FaHistory /></button
		>
	</div>

	<div class="flex flex-col m-1 gap-4 overflow-scroll">
		{#if loading}
			<div class="flex w-full justify-center">
				<ProgressRadial width="w-12" />
			</div>
		{/if}
		{#each currentTeam.members as member, index (member.id)}
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
				<div class="w-1/3 overflow-hidden text-nowrap text-center">
					<span class="font-bold text-xl">
						{member.tokens}
					</span>
					<span class="text-xs text-">
						{getPercentage(member.tokens, totalTokens)}%
					</span>
				</div>
				<div class="flex justify-end gap-4 w-1/3">
					{#if member.username !== $user.username}
						<button
							class="btn btn-icon w-6 text-secondary-500"
							on:click={() => handleTransfer(member)}
						>
							<FaPaperPlane />
						</button>
					{/if}
				</div>
			</div>
		{/each}
		{#if isAdmin}
			<button class="flex justify-between font-bold btn card p-4" on:click={handleInvite}>
				<span>{$_('team.invite.button')}</span>
				<div class="w-6 text-success-500"><FaPlus /></div>
			</button>
		{/if}
	</div>
</div>
