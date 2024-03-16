<script lang="ts">
	import '../app.postcss';

	// Floating UI for Popups
	import { computePosition, autoUpdate, flip, shift, offset, arrow } from '@floating-ui/dom';
	import { Modal, Toast, getToastStore, storePopup } from '@skeletonlabs/skeleton';
	storePopup.set({ computePosition, autoUpdate, flip, shift, offset, arrow });

	import { initializeStores } from '@skeletonlabs/skeleton';
	import { onMount } from 'svelte';
	import { session, user } from '$lib/storage';
	import { getUser } from '$lib/api';
	import { goto } from '$app/navigation';
	initializeStores();

	const toastStore = getToastStore();

	onMount(async () => {
		session.subscribe((value) => {
			if (value === null) return;
			getUser(value)
				.then((value) => {
					$user = value;
				})
				.catch((error) => {
					toastStore.trigger({ message: error, background: 'variant-filled-error' });
					$session = null;
					goto('/login');
				});
		});
	});
</script>

<Modal />
<Toast position="t" />

<div class="flex flex-col w-full h-full justify-center items-center">
	<slot />
</div>
