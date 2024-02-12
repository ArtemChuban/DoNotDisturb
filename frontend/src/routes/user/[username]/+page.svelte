<script lang="ts">
	import { getUserByUsername, type User } from '$lib/api';
	import { notification, NotificationType } from '$lib/notification';
	import { onMount } from 'svelte';
	import { linear } from 'svelte/easing';
	import { tweened } from 'svelte/motion';
	import UserAvatar from '$lib/UserAvatar.svelte';

	interface Data {
		username: string;
	}

	const getPromise = async () => {
		const user = await getUserByUsername(data.username);
		tokens.set(user.tokens);
		return user;
	};

	export let data: Data;
	let tokens = tweened(0, { duration: 500, easing: linear });
	let userPromise: Promise<User> = new Promise(() => null);
	onMount(() => {
		userPromise = getPromise();
	});
</script>

<svelte:head>
	<title>{data.username}</title>
</svelte:head>

<div class="flex flex-col items-center justify-center bg-slate-800 w-1/2 h-1/2 rounded-md">
	{#await userPromise}
		<div
			role="status"
			class="animate-pulse rounded-full bg-slate-100 text-slate-900 text-4xl w-24 h-24 flex items-center justify-center mb-5"
		></div>
		<span
			role="status"
			class="animate-pulse break-words w-1/2 m-5 rounded-md text-center bg-slate-700"><wbr /></span
		>
		<span role="status" class="animate-pulse mt-5 text-4xl bg-slate-700 w-1/2 rounded-md"
			><wbr /></span
		>
	{:then user}
		<div class="w-24 h-24 text-3xl mb-5">
			<UserAvatar username={user.username} />
		</div>
		<span class="{user.is_admin ? 'text-red-400' : ''} break-words w-full p-5 text-center"
			>{user.username}</span
		>
		<span class="mt-5 text-4xl">{Math.floor($tokens)}</span>
	{:catch error}
		<div
			role="status"
			class="rounded-full bg-slate-100 text-slate-900 text-4xl w-24 h-24 flex items-center justify-center mb-5"
		></div>
		<span role="status" class="break-words w-1/2 m-5 rounded-md text-center bg-slate-700"
			><wbr /></span
		>
		<span role="status" class="mt-5 text-4xl bg-slate-700 w-1/2 rounded-md"><wbr /></span>
		{(notification.set({ message: String(error), type: NotificationType.ERROR }), '')}
	{/await}
</div>
