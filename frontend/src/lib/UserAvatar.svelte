<script lang="ts">
	import { Avatar } from '@skeletonlabs/skeleton';

	export let username: string;
</script>

<Avatar initials={username[0].toUpperCase()} width="full" />
