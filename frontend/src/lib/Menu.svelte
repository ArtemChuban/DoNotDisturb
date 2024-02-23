<script lang="ts">
	import { slide } from 'svelte/transition';
	import { goto, onNavigate } from '$app/navigation';
	import { onMount } from 'svelte';
	import { changeLocale, getUser } from './api';
	import { t, locale, locales, flagIcon } from './i18n';
	import MenuButton from './MenuButton.svelte';
	import passwordIcon from '$lib/assets/key.svg';
	import logoutIcon from '$lib/assets/door.svg';
	import transactionsIcon from '$lib/assets/papers.svg';
	import transferIcon from '$lib/assets/money.svg';
	import profileIcon from '$lib/assets/person.svg';
	import createIcon from '$lib/assets/add.svg';
	import rewardIcon from '$lib/assets/reward.svg';
	import usersIcon from '$lib/assets/collaboration.svg';
	import { session } from './user';
	import { page } from '$app/stores';

	let menuOpened = false;
	let is_admin = false;

	onNavigate(() => {
		menuOpened = false;
	});

	onMount(async () => {
		session.subscribe(async (value) => {
			if (value === null) return;
			const user = await getUser(value);
			$locale = user.locale;
			is_admin = user.is_admin;
		});
	});

	const changeLocaleHandle = async () => {
		$locale = locales[(locales.indexOf($locale) + 1) % locales.length];
		if ($session !== null) {
			changeLocale($session, $locale);
		}
	};
</script>

<div
	class="z-10 transition-opacity bg-black {menuOpened
		? 'bg-opacity-50 h-full'
		: 'bg-opacity-0'} w-full flex flex-col justify-end items-center absolute bottom-0"
>
	<button
		on:click={() => (menuOpened = !menuOpened)}
		class="mb-4 w-12 h-12 bg-surface-900 border rounded-full flex justify-center items-center"
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
			class="flex flex-col w-full bg-surface-800 p-3 justify-between rounded-t-md"
		>
			<MenuButton icon={$flagIcon} onclick={changeLocaleHandle} text={$t('menu.language')} />
			{#if $page.route.id !== '/login'}
				<MenuButton icon={logoutIcon} onclick={() => ($session = null)} text={$t('menu.logout')} />
				<MenuButton
					icon={passwordIcon}
					onclick={() => goto('/password')}
					text={$t('menu.password')}
				/>
				<MenuButton
					icon={transactionsIcon}
					onclick={() => goto('/transactions')}
					text={$t('menu.transactions')}
				/>
				<MenuButton
					icon={transferIcon}
					onclick={() => goto('/transfer')}
					text={$t('menu.transfer')}
				/>
				<MenuButton icon={profileIcon} onclick={() => goto('/')} text={$t('menu.profile')} />
				<MenuButton icon={usersIcon} onclick={() => goto('/users')} text={$t('menu.leaderboard')} />

				{#if is_admin}
					<MenuButton icon={createIcon} onclick={() => goto('/create')} text={$t('menu.create')} />
					<MenuButton icon={rewardIcon} onclick={() => goto('/reward')} text={$t('menu.reward')} />
				{/if}
			{/if}
		</nav>
	{/if}
</div>
