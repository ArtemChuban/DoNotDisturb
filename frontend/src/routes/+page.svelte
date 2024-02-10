<script lang="ts">
	import { onMount } from 'svelte';
	import { getUser } from '$lib/api';
	import { goto } from '$app/navigation';

	onMount(async () => {
		getUser()
			.then((user) => {
				goto(`/user/${user.username}`);
			})
			.catch((err) => {
				localStorage.removeItem('session');
				goto('/login');
			});
	});
</script>
