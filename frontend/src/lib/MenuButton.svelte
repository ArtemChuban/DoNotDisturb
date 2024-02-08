<script lang="ts">
	export let onclick: () => void;
	export let icon: string;
	export let text: string;
</script>

<button
	on:click={onclick}
	class="bg-slate-900 my-1 rounded-md py-2 px-5 flex justify-center items-center"
	><img class="w-8 h-8 mr-2" src={icon} alt="" />{text}</button
>
