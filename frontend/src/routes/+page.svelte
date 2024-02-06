<script>
	import { onMount } from 'svelte';
	import { goto } from '$app/navigation';

	onMount(() => {
		if (localStorage.getItem('token') === null) {
			goto('/login');
		}
	});
</script>

<div>
	<h1>Главная страница</h1>
	<p>Добро пожаловать!</p>
</div>
