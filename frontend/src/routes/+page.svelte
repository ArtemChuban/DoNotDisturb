<script lang="ts">
	import { onMount } from 'svelte';
	import { getUser } from '$lib/api';
	import { goto } from '$app/navigation';

	onMount(async () => {
		const user = await getUser();
		if (user === null) return;
		goto(`/user/${user.username}`);
	});
</script>
