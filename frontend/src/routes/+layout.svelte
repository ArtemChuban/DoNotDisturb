<script lang="ts">
	import '../app.postcss';

	// Highlight JS
	import hljs from 'highlight.js/lib/core';
	import 'highlight.js/styles/github-dark.css';
	import { Toast, storeHighlightJs } from '@skeletonlabs/skeleton';
	import xml from 'highlight.js/lib/languages/xml'; // for HTML
	import css from 'highlight.js/lib/languages/css';
	import javascript from 'highlight.js/lib/languages/javascript';
	import typescript from 'highlight.js/lib/languages/typescript';

	hljs.registerLanguage('xml', xml); // for HTML
	hljs.registerLanguage('css', css);
	hljs.registerLanguage('javascript', javascript);
	hljs.registerLanguage('typescript', typescript);
	storeHighlightJs.set(hljs);

	// Floating UI for Popups
	import { computePosition, autoUpdate, flip, shift, offset, arrow } from '@floating-ui/dom';
	import { storePopup } from '@skeletonlabs/skeleton';
	storePopup.set({ computePosition, autoUpdate, flip, shift, offset, arrow });

	import Menu from '$lib/Menu.svelte';
	import { onMount } from 'svelte';
	import { session, username } from '$lib/user';
	import { goto } from '$app/navigation';
	import { getUser } from '$lib/api';
	import { locale } from '$lib/i18n';
	import { initializeStores } from '@skeletonlabs/skeleton';
	initializeStores();

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

<Menu />
<Toast position="t" />
<div
	class="flex flex-col justify-center items-center h-[100dvh] text-slate-100 font-bold transition-transform"
>
	<slot />
</div>
