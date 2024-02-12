<script lang="ts">
	import Loader from './Loader.svelte';
	import { notification, NotificationType } from '$lib/notification';

	export let promise: Promise<void>;
</script>

<div class="flex justify-center mt-3 items-center h-full w-full text-center" role="status">
	{#await promise}
		<Loader />
	{:catch error}
		{@const _ = notification.set({ message: String(error), type: NotificationType.ERROR })}
	{/await}
</div>
