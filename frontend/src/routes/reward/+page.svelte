<script lang="ts">
	import { onMount } from 'svelte';
	import { goto } from '$app/navigation';
	import { getAllUsers, getUser, reward } from '$lib/api';
	import FetchStatus from '$lib/FetchStatus.svelte';
	import { t } from '$lib/i18n';
	import { session } from '$lib/user';
	import { writable } from 'svelte/store';
	import {
		Autocomplete,
		InputChip,
		getToastStore,
		type AutocompleteOption
	} from '@skeletonlabs/skeleton';
	const toastStore = getToastStore();

	let value = '';
	let promise: Promise<void>;
	let inputChip = '';
	let inputChipList: Array<string> = [];
	const options = writable<Array<AutocompleteOption<string>>>([]);
	let inputChipComponent: InputChip;
	let whitelist = writable<Array<string>>([]);

	options.subscribe((options) => {
		$whitelist = options.map((option) => option.value);
	});

	onMount(async () => {
		session.subscribe(async (value) => {
			if (value === null) return;
			if (!(await getUser(value)).is_admin) goto('/');
		});
		getUsernames();
	});

	const getUsernames = async () => {
		(await getAllUsers()).forEach((user) => {
			$options.push({ label: user.username, value: user.username });
		});
		$options = $options;
	};

	const handleReward = async () => {
		inputChipList.forEach(async (username) => {
			if ($session === null) return;
			await reward($session, username, +value);
		});
		toastStore.trigger({
			message: `${Array.from(inputChipList)} rewarded for ${value} token${+value === 1 ? '' : 's'}`,
			background: 'variant-filled-success'
		});
		goto('/');
	};

	const onInputChipSelect = (event: CustomEvent) => {
		inputChipComponent.addChip(event.detail.value);
		inputChip = '';
	};
</script>

<svelte:head>
	<title>Reward</title>
</svelte:head>

<div class="w-1/2">
	<h1 class="text-center mb-3 text-slate-100 font-bold text-xl">{$t('reward.title')}</h1>
	<form on:submit|preventDefault={() => (promise = handleReward())} class="flex flex-col">
		<InputChip
			bind:this={inputChipComponent}
			bind:input={inputChip}
			bind:value={inputChipList}
			placeholder={'Search...'}
			whitelist={$whitelist}
			allowUpperCase
			name="chips"
		/>
		<div class="card mt-5 max-h-48 overflow-y-auto" tabindex="-1">
			<Autocomplete
				bind:input={inputChip}
				options={$options}
				denylist={inputChipList}
				on:selection={onInputChipSelect}
			/>
		</div>
		<input bind:value type="number" class="input my-5" placeholder={$t('value')} />
		<button type="submit" class="btn variant-filled-surface text-sm">{$t('reward.button')}</button>
	</form>
</div>

<div class="w-full h-8">
	<FetchStatus {promise} />
</div>
