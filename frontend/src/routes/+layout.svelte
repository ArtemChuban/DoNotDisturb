<script lang="ts">
	import '../app.css';
	import Menu from '$lib/Menu.svelte';
	import Notifications from '$lib/Notifications.svelte';
	import { onMount } from 'svelte';
	import { session, username } from '$lib/user';
	import { goto } from '$app/navigation';
	import { getUser } from '$lib/api';
	import { locale } from '$lib/i18n';

	onMount(async () => {
		$session = localStorage.getItem('session');
		const loc = localStorage.getItem('locale');
		if (loc !== null) $locale = loc;
		session.subscribe(async (value) => {
			if (value === null) {
				localStorage.removeItem('session');
				goto('/login');
				return;
			}
			localStorage.setItem('session', value);
			const user = await getUser(value);
			$username = user.username;
		});
		locale.subscribe((value) => {
			localStorage.setItem('locale', value);
		});
	});
</script>

<div
	class="flex flex-col justify-center items-center h-[100dvh] bg-slate-900 text-slate-100 font-bold"
>
	<Notifications />
	<slot />
	<Menu />
</div>
