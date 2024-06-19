<script lang="ts">
	import { ProgressRadial, getToastStore } from '@skeletonlabs/skeleton';
	// @ts-expect-error, no types for this module
	import FaArrowLeft from 'svelte-icons/fa/FaArrowLeft.svelte';
	// @ts-expect-error, no types for this module
	import FaPaperPlane from 'svelte-icons/fa/FaPaperPlane.svelte';
	// @ts-expect-error, no types for this module
	import FaAward from 'svelte-icons/fa/FaAward.svelte';
	// @ts-expect-error, no types for this module
	import FaPlus from 'svelte-icons/fa/FaPlus.svelte';

	import { session, user } from '$lib/storage';
	import { type ITransaction, getTransactions } from '$lib/api';
	import { onMount } from 'svelte';
	import { config } from '$lib/config';
	import { fly } from 'svelte/transition';
	import { push } from 'svelte-spa-router';

	export let params: { id: string };
	const toastStore = getToastStore();
	let loading = false;
	let transactions: ITransaction[] = [];
	let teamName = '';
	let fullLoaded = false;
	const TransactionsPerLoad = 8;

	onMount(() => {
		user.subscribe((value) => {
			loading = true;
			if (!Object.keys(value.teams).includes(params.id)) return;
			teamName = $user.teams[params.id].name;
			loadMoreTransactions();
		});
	});
	const loadMoreTransactions = () => {
		loading = true;
		getTransactions($session!, params.id, transactions.length, TransactionsPerLoad)
			.then((txs) => {
				if (txs.length < TransactionsPerLoad) fullLoaded = true;
				transactions = [...transactions, ...txs];
				loading = false;
			})
			.catch((error) => {
				toastStore.trigger({ message: error, background: 'variant-filled-error' });
				push('/');
			});
	};
</script>

<div class="flex flex-col h-3/4 w-3/4 gap-4">
	<div class="card flex justify-around items-center py-4">
		<button type="button" class="btn btn-icon w-6" on:click={() => push(`/team/${params.id}`)}
			><FaArrowLeft /></button
		>
		<span class="font-bold text-xl text-primary-500">{teamName}</span>
		<span class="font-bold text-xl">TXs</span>
	</div>

	<div class="flex flex-col m-1 gap-4 overflow-scroll">
		{#each transactions as tx, index (tx.id)}
			<div
				class="card p-4 relative overflow-visible"
				in:fly={{
					duration: config.duration,
					delay: index * config.delay,
					y: config.offset
				}}
			>
				<div class="flex justify-around mb-2">
					<span
						class="font-bold text-xl w-1/3 overflow-hidden {tx.from_username === $user.username
							? 'text-primary-500'
							: ''}"
					>
						{tx.from_username}
					</span>
					<div class="w-6 text-secondary-500">
						{#if tx.type === 0}
							<FaAward />
						{:else if tx.type === 1}
							<FaPaperPlane />
						{/if}
					</div>
					<div class="w-1/5 overflow-hidden text-nowrap text-center">
						<span class="font-bold text-xl">
							{tx.value}
						</span>
					</div>
					<span
						class="font-bold text-xl w-1/3 overflow-hidden {tx.to_username === $user.username
							? 'text-primary-500'
							: ''}"
					>
						{tx.to_username}
					</span>
				</div>
				<span>
					{new Date(Math.floor(tx.timestamp / 1000)).toLocaleString('en-EN')}
				</span>
				<p class="break-words">
					{tx.description}
				</p>
			</div>
		{/each}
		{#if !fullLoaded}
			<button class="flex justify-between font-bold btn card p-4" on:click={loadMoreTransactions}>
				<span>Load more</span>
				<div class="w-6 text-success-500"><FaPlus /></div>
			</button>
		{/if}
	</div>
	{#if loading}
		<div class="flex w-full justify-center">
			<ProgressRadial width="w-12" />
		</div>
	{/if}
</div>
