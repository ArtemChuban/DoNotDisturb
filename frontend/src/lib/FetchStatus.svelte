<script lang="ts">
	import { getToastStore } from '@skeletonlabs/skeleton';
	import Loader from './Loader.svelte';
	const toastStore = getToastStore();

	export let promise: Promise<void>;
</script>

<div class="flex justify-center mt-3 items-center h-full w-full text-center" role="status">
	{#await promise}
		<Loader />
	{:catch error}
		{toastStore.trigger({ message: String(error), background: 'variant-filled-error' })}
	{/await}
</div>
