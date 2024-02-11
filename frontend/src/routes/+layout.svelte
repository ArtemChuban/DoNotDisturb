<script lang="ts">
	import '../app.css';
	import Menu from '$lib/Menu.svelte';
	import { page } from '$app/stores';
	import Notifications from '$lib/Notifications.svelte';

	
</script>

<div
	class="flex flex-col justify-center items-center h-[100dvh] bg-slate-900 text-slate-100 font-bold"
>
	<Notifications />
	<slot />
	{#if $page.route.id !== '/login'}
		<Menu />
	{/if}
</div>
