<script lang="ts">
	import { goto } from '$app/navigation';
	import UserAvatar from '$lib/UserAvatar.svelte';
	import { getAllUsers, type User } from '$lib/api';
	import { t } from '$lib/i18n';
	import { onMount } from 'svelte';
	import { fly } from 'svelte/transition';

	let users: Array<User> = [];

	onMount(async () => {
		users = await getAllUsers();
		users = users.sort((a: User, b: User) => b.tokens - a.tokens);
	});
</script>

<svelte:head>
	<title>Leaderboard</title>
</svelte:head>

<div class="flex flex-col w-full h-full items-center justify-start">
	<h1 class="text-2xl m-4 font-bold">{$t('leaderboard.title')}</h1>
	<div class="w-3/4 overflow-x-scroll mb-20">
		{#each users as user, id}
			<button
				on:click={() => goto(`/user/${user.username}`)}
				transition:fly={{ delay: id * 50, y: 50 }}
				class="flex bg-slate-800 rounded-md w-full p-3 my-1 justify-between items-center text-center"
			>
				<div class="w-1/3 h-full">
					<div class="w-12 h-12">
						<UserAvatar username={user.username} />
					</div>
				</div>
				<p class="w-1/3 {user.is_admin ? 'text-red-400' : ''}">{user.username}</p>
				<p class="w-1/3">{user.tokens}</p>
			</button>
		{/each}
	</div>
</div>
