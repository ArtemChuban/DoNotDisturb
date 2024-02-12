<script lang="ts">
	import { onMount } from 'svelte';
	import { goto } from '$app/navigation';
	import { username } from '$lib/user';

	onMount(async () => {
		username.subscribe((value) => {
			if (value === null) return;
			goto(`/user/${value}`);
		});
	});
</script>
