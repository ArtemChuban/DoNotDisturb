<script lang="ts">
	import { onMount } from 'svelte';
	import { goto } from '$app/navigation';
	import { getTransactions, type Transaction } from '$lib/api';
	import UserSelect from '$lib/UserSelect.svelte';
	import TransactionComponent from '$lib/Transaction.svelte';
	import Loader from '$lib/Loader.svelte';
	import { writable } from 'svelte/store';
	import { notification, NotificationType } from '$lib/notification';
	import { t } from '$lib/i18n';

	let transactions: Array<Transaction> = [];
	let initiator = writable('Any');
	let reciever = writable('Any');
	let transactionsDiv: HTMLElement;
	let loadMoreButtonVisible = true;
	let limit = 8;
	let promise: Promise<void>;

	const repopulateTransactions = async () => {
		transactions = await getTransactions(
			0,
			limit,
			$initiator === 'Any' ? null : $initiator,
			$reciever === 'Any' ? null : $reciever
		);
		loadMoreButtonVisible = transactions.length >= limit;
	};

	const getMoreTransactions = async () => {
		const offset = transactionsDiv.childElementCount - 1;
		const newTransactions = await getTransactions(
			offset,
			limit,
			$initiator === 'Any' ? null : $initiator,
			$reciever === 'Any' ? null : $reciever
		);
		transactions = [...transactions, ...newTransactions];
		if (newTransactions.length < limit) {
			loadMoreButtonVisible = false;
		}
	};

	onMount(async () => {
		const session = localStorage.getItem('session');
		if (session === null) {
			goto('/login');
			return;
		}
		promise = repopulateTransactions();
		initiator.subscribe(repopulateTransactions);
		reciever.subscribe(repopulateTransactions);
	});
</script>

<svelte:head>
	<title>Transactions</title>
</svelte:head>

<div class="w-full h-full flex flex-col justify-start items-center">
	<h1 class="text-2xl m-4 font-bold">{$t('transactions.title')}</h1>
	<div class="flex w-5/6 justify-around items-center mb-5">
		<p class="mr-3">{$t('transactions.from')}</p>
		<UserSelect bind:username={$initiator} usernames={['Any']} />
		<p class="mx-3">{$t('transactions.to')}</p>
		<UserSelect bind:username={$reciever} usernames={['Any']} />
	</div>
	<div
		class="overflow-y-scroll overflow-x-hidden w-full flex flex-col justify-start items-center pt-1 mb-20"
		bind:this={transactionsDiv}
	>
		{#each transactions as transaction (transaction.id)}
			<TransactionComponent {transaction} />
		{/each}

		{#await promise}
			<div class="flex p-3 justify-center items-center w-full">
				<Loader />
			</div>
		{:then}
			{#if transactions.length === 0}
				{$t('transactions.not_found')}
			{/if}
			{#if loadMoreButtonVisible}
				<button
					class="flex w-5/6 bg-slate-800 rounded-md justify-center p-3 items-center relative"
					on:click={() => (promise = getMoreTransactions())}
				>
					Load more
				</button>
			{/if}
		{:catch error}
			{@const _ = (notification.set({ message: String(error), type: NotificationType.ERROR }), '')}
		{/await}
	</div>
</div>
