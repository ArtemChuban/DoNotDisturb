<script lang="ts">
	import { goto } from '$app/navigation';
	import { getUserByUsername, type User } from '$lib/api';
	import { onMount } from 'svelte';
	import { linear } from 'svelte/easing';
	import { tweened } from 'svelte/motion';

	interface Data {
		username: string;
	}

	export let data: Data;

	let user: User = { username: 'username', is_admin: false, tokens: 0 };
	let tokens = tweened(0, { duration: 500, easing: linear });

	onMount(async () => {
		const value = await getUserByUsername(data.username);
		if (value === null) {
			goto('/');
			return;
		}
		user = value;
		$tokens = user.tokens;
	});
</script>

<div class="flex flex-col items-center justify-center bg-slate-800 w-1/2 h-1/2 rounded-md">
	<div
		class="rounded-full bg-slate-100 text-slate-900 text-4xl w-24 h-24 flex items-center justify-center mb-5"
	>
		<span>{user.username[0].toUpperCase()}</span>
	</div>
	<span class="{user.is_admin ? 'text-red-400' : ''} break-words w-full p-5 text-center"
		>{user.username}</span
	>
	<span class="mt-5 text-4xl">{Math.floor($tokens)}</span>
</div>
