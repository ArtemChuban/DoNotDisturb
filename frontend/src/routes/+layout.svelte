<script>
	import '../app.css';
	import Menu from '$lib/Menu.svelte';
	import { getUser } from '$lib/api';
	import { onMount } from 'svelte';
	import { page } from '$app/stores';
</script>

<div
	class="flex flex-col justify-center items-center h-[100dvh] bg-slate-900 text-slate-100 font-bold"
>
	{#if $page.route.id !== '/login'}
		<Menu />
	{/if}
	<slot />
</div>
