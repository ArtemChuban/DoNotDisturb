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

<div class="w-full input-group input-group-divider grid-cols-[1fr_auto]">
	<input bind:value={password} {...{ type }} class="input" placeholder={$t(title)} />
	<button on:click|preventDefault={toggleHandler} class="" type="button"
		><img class="w-8 h-8" src={icon} alt="" /></button
	>
</div>
