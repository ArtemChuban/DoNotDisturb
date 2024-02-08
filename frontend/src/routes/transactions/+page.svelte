<script lang="ts">
	import { onMount } from 'svelte';
	import { goto } from '$app/navigation';
	import { BACKEND_URL } from '$lib/api';
	import { fade } from 'svelte/transition';

	enum TransactionType {
		REWARD = 'Reward',
		TRANSFER = 'Transfer'
	}

	interface Transaction {
		timestamp: number;
		initiator: string;
		reciever: string;
		value: number;
		type: TransactionType;
	}

	interface User {
		username: string;
		is_admin: boolean;
		tokens: number;
	}

	let transactions: Array<Transaction> = [];
	let users: Array<User> = [];
	let initiator = '';
	let reciever = '';
	let transactionsDiv: HTMLElement;
	let loadMoreButtonVisible = true;
	let limit = 8;

	const fetchTransactions = async (offset: number = 0) => {
		let query = `offset=${offset}&limit=${limit}`;
		if (initiator !== '') {
			query += `&initiator=${initiator}`;
		}
		if (reciever !== '') {
			query += `&reciever=${reciever}`;
		}
		const response = await fetch(`${BACKEND_URL}/transactions?${query}`);
		if (!response.ok) return [];
		return await response.json();
	};

	const getTransactions = async () => {
		transactions = await fetchTransactions();
		loadMoreButtonVisible = transactions.length >= limit;
	};

	const getMoreTransactions = async () => {
		const offset = transactionsDiv.childElementCount - 1;
		const newTransactions = await fetchTransactions(offset);
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
		getTransactions();
		fetch(`${BACKEND_URL}/users`).then(async (response) => {
			users = await response.json();
		});
	});
</script>

<div class="w-full h-full flex flex-col justify-start items-center">
	<h1 class="text-2xl m-4 font-bold">Transactions</h1>
	<div class="flex w-5/6 justify-around items-center mb-5">
		<p>From</p>
		<select
			class="bg-slate-800 p-1 rounded-md w-1/2 mx-3"
			bind:value={initiator}
			on:change={getTransactions}
		>
			<option value="" selected>Any</option>
			{#each users as user}
				<option value={user.username}>{user.username}</option>
			{/each}
		</select>
		<p>To</p>
		<select
			class="bg-slate-800 p-1 rounded-md w-1/2 ml-3"
			bind:value={reciever}
			on:change={getTransactions}
		>
			<option value="" selected>Any</option>
			{#each users as user}
				<option value={user.username}>{user.username}</option>
			{/each}
		</select>
	</div>
	<div
		class="overflow-y-scroll overflow-x-visible w-full flex flex-col justify-start items-center mb-20"
		bind:this={transactionsDiv}
	>
		{#each transactions as transaction}
			<div
				class="flex w-5/6 bg-slate-800 rounded-md justify-between p-3 my-5 items-center relative"
			>
				<a href="/user/{transaction.initiator}" class="bg-slate-900 px-2 py-1 rounded-md"
					>{transaction.initiator}</a
				>
				<div class="mx-1">{transaction.type.toLowerCase()}s</div>
				<a
					href="/user/{transaction.reciever}"
					class="bg-slate-900 px-2 py-1 rounded-md overflow-hidden max-w-1/4"
					>{transaction.reciever}</a
				>
				<div class="ml-1">{transaction.value}</div>
				<div class="absolute -top-6 -left-5 bg-slate-700 rounded-md p-1">
					{new Date(transaction.timestamp * 1000).toLocaleString('ru-RU')}
				</div>
			</div>
		{/each}
		{#if loadMoreButtonVisible}
			<button
				transition:fade={{ duration: 100 }}
				class="flex w-5/6 bg-slate-800 rounded-md justify-center p-3 items-center relative"
				on:click={getMoreTransactions}
			>
				Load more
			</button>
		{/if}
	</div>
</div>
