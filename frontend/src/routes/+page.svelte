<script lang="ts">
	import { goto } from '$app/navigation';
	import { Avatar } from '@skeletonlabs/skeleton';
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

	const modalStore = getModalStore();
	let username: string = 'artemchuban';

	interface ITeam {
		id: string;
		name: string;
	}

	let teams: Array<ITeam> = [
		{ name: 'team1', id: '1' },
		{ name: 'team2', id: '2' },
		{ name: 'team3', id: '3' },
		{ name: 'team4', id: '4' }
	];
	let invites: Array<ITeam> = [
		{ name: 'new team 1', id: '101' },
		{ name: 'new team 2', id: '102' }
	];

	const handleLogOut = () => {
		modalStore.trigger({
			type: 'confirm',
			title: 'Log out',
			body: 'Are you sure you wish to log out from your account?',
			response: (confirmed: boolean) => {
				if (!confirmed) return;
				goto('/login');
			}
		});
	};

	const handleInviteAccept = async (id: string) => {
		invites.forEach((team, index) => {
			if (team.id !== id) return;
			invites.splice(index, 1);
			teams.push(team);
		});
		invites = invites;
		teams = teams;
	};

	const handleInviteDeny = async (id: string) => {
		invites.forEach((team, index) => {
			if (team.id !== id) return;
			invites.splice(index, 1);
		});
		invites = invites;
	};

	const handleCreateNewTeam = async () => {
		modalStore.trigger({
			type: 'prompt',
			title: 'Create new team',
			body: 'New team name',
			valueAttr: { type: 'text', required: true },
			response: (team_name: string) => {
				if (!team_name) return;
				teams = [...teams, { name: team_name, id: team_name }];
			}
		});
	};
</script>

<div class="flex flex-col h-3/4 w-3/4 gap-4">
	<div>If you see this, s3 works fine</div>
	<div class="card flex justify-around items-center py-4">
		<Avatar initials={username} />
		<span class="text-md text-primary-500">{username}</span>
		<button class="btn btn-icon w-8 text-error-500" on:click={handleLogOut}><IoMdExit /></button>
	</div>

	<div class="flex flex-col m-1 gap-4 overflow-scroll">
		{#each teams as team (team.id)}
			<button class="flex justify-between btn card p-4" on:click={() => goto(`/team`)}>
				<span class="font-bold text-xl">{team.name}</span>
				<div class="w-6 text-secondary-500"><FaArrowRight /></div>
			</button>
		{/each}
		{#each invites as invite (invite.id)}
			<div class="flex justify-between items-center card p-4">
				<span class="font-bold text-xl">{invite.name}</span>
				<div class="flex items-center gap-2">
					<button
						class="btn btn-icon w-8 text-error-500"
						on:click={() => handleInviteDeny(invite.id)}><FaTimes /></button
					>
					<button
						class="btn btn-icon w-6 text-success-500"
						on:click={() => handleInviteAccept(invite.id)}><FaCheck /></button
					>
				</div>
			</div>
		{/each}
		<button class="flex justify-between font-bold btn card p-4" on:click={handleCreateNewTeam}>
			<span>Create new team</span>
			<div class="w-6 text-success-500"><FaPlus /></div>
		</button>
	</div>
</div>
