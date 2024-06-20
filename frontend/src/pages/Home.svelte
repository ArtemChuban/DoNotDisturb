<script lang="ts">
	import { Avatar, ProgressRadial, getToastStore } from '@skeletonlabs/skeleton';
	import { getModalStore } from '@skeletonlabs/skeleton';

	// @ts-expect-error, no types for this module
	import FaArrowRight from 'svelte-icons/fa/FaArrowRight.svelte';
	// @ts-expect-error, no types for this module
	import FaPlus from 'svelte-icons/fa/FaPlus.svelte';
	// @ts-expect-error, no types for this module
	import IoMdExit from 'svelte-icons/io/IoMdExit.svelte';
	// @ts-expect-error, no types for this module
	import FaTimes from 'svelte-icons/fa/FaTimes.svelte';
	// @ts-expect-error, no types for this module
	import FaCheck from 'svelte-icons/fa/FaCheck.svelte';
	// @ts-expect-error, no types for this module
	import FaRegEdit from 'svelte-icons/fa/FaRegEdit.svelte';

	import { session, user } from '$lib/storage';
	import { createTeam, inviteReply, type ITeam } from '$lib/api';
	import { fly } from 'svelte/transition';
	import { config } from '$lib/config';
	import { push } from 'svelte-spa-router';
	import { _ } from 'svelte-i18n';

	const modalStore = getModalStore();
	const toastStore = getToastStore();
	let loading = true;

	user.subscribe((value) => {
		if (value.username === '') return;
		loading = false;
	});

	const handleLogOut = () => {
		modalStore.trigger({
			type: 'confirm',
			title: $_('home.logout.title'),
			body: $_('home.logout.body'),
			response: (confirmed: boolean) => {
				if (!confirmed) return;
				$session = null;
				push('/login');
			}
		});
	};

	const handleInviteReply = async (team: ITeam, accepted: boolean) => {
		inviteReply($session!, team.id, accepted)
			.then(() => {
				$user.invites.splice($user.invites.indexOf(team), 1);
				if (accepted) {
					$user.teams[team.id] = team;
				}
				$user = $user;
			})
			.catch((error) => {
				toastStore.trigger({ message: error, background: 'variant-filled-error' });
			});
	};

	const handleCreateNewTeam = async () => {
		modalStore.trigger({
			type: 'prompt',
			title: $_('home.create.title'),
			body: $_('home.create.body'),
			valueAttr: { type: 'text', required: true },
			response: (team_name: string) => {
				if (!team_name) return;
				createTeam($session!, team_name)
					.then((team) => {
						$user.teams[team.id] = team;
						$user = $user;
					})
					.catch((error) => {
						toastStore.trigger({ message: error, background: 'variant-filled-error' });
					});
			}
		});
	};
</script>

<div class="flex flex-col h-3/4 w-3/4 gap-4">
	<div class="card flex justify-around items-center py-4">
		<div class="{loading ? 'animate-pulse' : ''} relative">
			<Avatar initials={$user.username} />
			<button class="w-6 absolute top-0 right-0 text-primary-500" on:click={() => push('/profile')}
				><FaRegEdit /></button
			>
		</div>
		<span
			class="text-md text-primary-500 {loading
				? 'placeholder animate-pulse '
				: ''} w-1/3 text-center"
		>
			{$user.username}
		</span>
		<button class="btn btn-icon w-8 text-error-500" on:click={handleLogOut}><IoMdExit /></button>
	</div>

	<div class="flex flex-col m-1 gap-4 overflow-scroll">
		{#each Object.values($user.teams) as team, index}
			<button
				class="flex justify-between btn card p-4"
				in:fly={{
					duration: config.duration,
					delay: index * config.delay,
					y: config.offset
				}}
				on:click={() => {
					push(`/team/${team.id}`);
				}}
			>
				<span class="font-bold text-xl">{team.name}</span>
				<div class="w-6 text-secondary-500"><FaArrowRight /></div>
			</button>
		{/each}
		{#if loading}
			<div class="w-full flex justify-center">
				<ProgressRadial width="w-12" />
			</div>
		{/if}
		{#each $user.invites as invite, index}
			<div
				class="flex justify-between items-center card p-4"
				in:fly={{
					duration: config.duration,
					delay: (index + Object.keys($user.teams).length) * config.delay,
					y: config.offset
				}}
			>
				<span class="font-bold text-xl">{invite.name}</span>
				<div class="flex items-center gap-2">
					<button
						class="btn btn-icon w-8 text-error-500"
						on:click={() => handleInviteReply(invite, false)}><FaTimes /></button
					>
					<button
						class="btn btn-icon w-6 text-success-500"
						on:click={() => handleInviteReply(invite, true)}><FaCheck /></button
					>
				</div>
			</div>
		{/each}
		{#if !loading}
			<button
				in:fly={{
					duration: config.duration,
					delay: ($user.invites.length + Object.keys($user.teams).length) * config.delay,
					y: config.offset
				}}
				class="flex justify-between font-bold btn card p-4"
				on:click={handleCreateNewTeam}
			>
				<span>{$_('home.createButton')}</span>
				<div class="w-6 text-success-500"><FaPlus /></div>
			</button>
		{/if}
	</div>
</div>
