<script lang="ts">
	import { type Transaction } from '$lib/api';
	import { fly } from 'svelte/transition';
	import { t } from './i18n';

	export let transaction: Transaction;
</script>

<div
	in:fly={{ y: 50 }}
	out:fly={{ y: -50 }}
	class="card flex w-5/6 justify-between p-3 my-5 items-center relative"
>
	<a href="/user/{transaction.initiator}" class="bg-surface-900 px-2 py-1 rounded-md"
		>{transaction.initiator}</a
	>
	<div class="mx-1">{$t(`transactions.${transaction.type.toLowerCase()}s`)}</div>
	<a
		href="/user/{transaction.reciever}"
		class="bg-surface-900 px-2 py-1 rounded-md overflow-hidden max-w-1/4">{transaction.reciever}</a
	>
	<div class="ml-1">{transaction.value}</div>
	<div class="card absolute -top-6 -left-5 rounded-md p-1">
		{new Date(transaction.timestamp * 1000).toLocaleString('ru-RU')}
	</div>
</div>
