<script lang="ts">
    export let username: string;
</script>

<div
	class="rounded-full bg-slate-100 text-slate-900 w-full h-full flex items-center justify-center"
>
	<span>{username[0].toUpperCase()}</span>
</div>
