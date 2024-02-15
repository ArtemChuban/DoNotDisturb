<script lang="ts">
	import { t } from './i18n';
	import passwordIcon from '$lib/assets/monkey-no.svg';
	import textIcon from '$lib/assets/monkey-yes.svg';

	export let password: string = '';
	export let title: string = 'password';
	let type: string = 'password';
	let icon: string = passwordIcon;

	const toggleHandler = () => {
		if (type === 'password') {
			type = 'text';
			icon = textIcon;
		} else {
			type = 'password';
			icon = passwordIcon;
		}
	};
</script>

<p class="text-slate-100 text-sm">{$t(title)}</p>
<div class="relative">
	<input
		bind:value={password}
		{...{ type }}
		class="border rounded-md bg-gray-800 border-gray-700 p-1 text-slate-100 w-full"
	/>
	<button on:click|preventDefault={toggleHandler} class="absolute right-0" type="button"
		><img class="w-8 h-8" src={icon} alt="" /></button
	>
</div>
