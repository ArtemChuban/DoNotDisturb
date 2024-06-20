<script lang="ts">
	import { getMembers, reward } from '$lib/api';
	import { session } from '$lib/storage';
	import {
		Autocomplete,
		type AutocompleteOption,
		InputChip,
		getToastStore,
		ProgressRadial
	} from '@skeletonlabs/skeleton';
	import { onMount } from 'svelte';
	import { push } from 'svelte-spa-router';
	// @ts-expect-error, no types for this module
	import FaArrowLeft from 'svelte-icons/fa/FaArrowLeft.svelte';
	import { _ } from 'svelte-i18n';

	const toastStore = getToastStore();
	export let params: { id: string };
	let members: AutocompleteOption<string, string>[] = [];
	let choosed: AutocompleteOption<string, string>[] = [];
	let loading = false;
	let value = '';
	let description = '';

	$: chips = choosed.map((c) => c.label);

	let inputChip = '';

	onMount(() => {
		loading = true;
		getMembers($session!, params.id)
			.then((response_members) => {
				members = response_members.map((member) => {
					return { label: member.username, value: member.id };
				});
				loading = false;
			})
			.catch((error) => {
				toastStore.trigger({ message: error, background: 'variant-filled-error' });
				push('/');
			});
	});

	const handleSelect = (event: CustomEvent<AutocompleteOption<string, string>>) => {
		if (choosed.includes(event.detail)) return;
		choosed = [...choosed, event.detail];
	};
	const handleReward = async () => {
		loading = true;
		reward(
			$session!,
			params.id,
			choosed.map((c) => c.value),
			Number(value),
			description
		)
			.then(() => {})
			.catch((error) => {
				toastStore.trigger({ message: error, background: 'variant-filled-error' });
			})
			.finally(() => {
				push(`/team/${params.id}`);
				loading = false;
			});
	};
	const handleChipRemove = (event: CustomEvent) => {
		choosed = choosed.filter((c) => c.label !== event.detail.chipValue);
	};
</script>

{#if loading}
	<ProgressRadial width="w-6" />
{:else}
	<div class="flex flex-col gap-4 text-center">
		<div class="flex justify-evenly">
			<button type="button" class="btn btn-icon w-6" on:click={() => push(`/team/${params.id}`)}
				><FaArrowLeft /></button
			>
			<h1 class="h1">{$_('reward.title')}</h1>
		</div>
		<InputChip
			bind:input={inputChip}
			bind:value={chips}
			name="chips"
			on:remove={handleChipRemove}
		/>
		<div class="card w-full max-w-sm max-h-48 p-4 overflow-y-auto" tabindex="-1">
			<Autocomplete
				bind:input={inputChip}
				options={members.filter((m) => !choosed.includes(m))}
				on:selection={handleSelect}
			/>
		</div>
		<input
			type="number"
			disabled={loading}
			class="input"
			placeholder={$_('reward.placeholder.value')}
			bind:value
		/>
		<textarea
			class="textarea"
			rows="4"
			placeholder={$_('reward.placeholder.description')}
			bind:value={description}
		></textarea>
		<button
			type="button"
			disabled={loading}
			class="btn variant-filled-primary"
			on:click={handleReward}
		>
			{#if loading}
				<ProgressRadial width="w-6" />
			{:else}
				<span>{$_('reward.button')}</span>
			{/if}
		</button>
	</div>{/if}
