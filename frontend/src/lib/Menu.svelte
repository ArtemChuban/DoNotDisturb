<script lang="ts">
	import { slide } from 'svelte/transition';
	import { goto, onNavigate } from '$app/navigation';
	import { onMount } from 'svelte';
	import { getUser } from './api';
	import MenuButton from './MenuButton.svelte';
	import passwordIcon from '$lib/assets/key.svg';
	import logoutIcon from '$lib/assets/door.svg';
	import transactionsIcon from '$lib/assets/papers.svg';
	import transferIcon from '$lib/assets/money.svg';
	import profileIcon from '$lib/assets/person.svg';
	import createIcon from '$lib/assets/add.svg';
	import rewardIcon from '$lib/assets/reward.svg';
	import usersIcon from '$lib/assets/collaboration.svg';

	let menuOpened = false;
	let is_admin = false;

	onNavigate(() => {
		menuOpened = false;
	});

	onMount(async () => {
		const user = await getUser();
		if (user === null) return;
		is_admin = user.is_admin;
	});

	const logout = () => {
		localStorage.removeItem('session');
		goto('/login');
	};

	const menuInteract = () => {
		menuOpened = !menuOpened;
	};
</script>

<div
	class="z-10 transition-opacity bg-black {menuOpened
		? 'bg-opacity-50 h-full'
		: 'bg-opacity-0'} w-full flex flex-col justify-end items-center absolute bottom-0"
>
	<button
		on:click={menuInteract}
		class="mb-4 w-12 h-12 bg-slate-800 rounded-full flex justify-center items-center"
	>
		<svg
			class="w-1/2 h-1/2 {menuOpened ? '-scale-y-100' : ''}"
			fill="#f1f5f9"
			viewBox="0 0 330 330"
		>
			<path
				d="M325.606,229.393l-150.004-150C172.79,76.58,168.974,75,164.996,75c-3.979,0-7.794,1.581-10.607,4.394  l-149.996,150c-5.858,5.858-5.858,15.355,0,21.213c5.857,5.857,15.355,5.858,21.213,0l139.39-139.393l139.397,139.393  C307.322,253.536,311.161,255,315,255c3.839,0,7.678-1.464,10.607-4.394C331.464,244.748,331.464,235.251,325.606,229.393z"
			/>
		</svg>
	</button>
	{#if menuOpened}
		<nav
			transition:slide
			class="flex flex-col w-full bg-slate-800 p-3 justify-between rounded-t-md"
		>
			<MenuButton icon={logoutIcon} onclick={logout} text="Log out" />
			<MenuButton icon={passwordIcon} onclick={() => goto('/password')} text="Change password" />
			<MenuButton
				icon={transactionsIcon}
				onclick={() => goto('/transactions')}
				text="Transactions"
			/>
			<MenuButton icon={transferIcon} onclick={() => goto('/transfer')} text="Transfer" />
			<MenuButton icon={profileIcon} onclick={() => goto('/')} text="My profile" />
			<MenuButton icon={usersIcon} onclick={() => goto('/users')} text="Leaderboard" />

			{#if is_admin}
				<MenuButton icon={createIcon} onclick={() => goto('/create')} text="Create user" />
				<MenuButton icon={rewardIcon} onclick={() => goto('/reward')} text="Reward" />
			{/if}
		</nav>
	{/if}
</div>
