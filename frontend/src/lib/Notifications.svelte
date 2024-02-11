<script lang="ts">
	import { NotificationType, notification, type Notification } from "$lib/store";
	import { fly } from "svelte/transition";

    let notifications: Array<Notification> = [];

const removeFirstNotification = async () => {
    await new Promise((resolve) => setTimeout(resolve, 3000));
    notifications = [...notifications.slice(1)];
};

notification.subscribe(async (notification) => {
    if (notification.type == NotificationType.EMPTY) return;
    notifications = [...notifications, notification];
    removeFirstNotification();
});
</script>

<div class="flex flex-col w-full absolute top-0 justify-start items-center">
    {#each notifications as ntf}
        <button
            in:fly={{ y: -100 }}
            out:fly={{ y: -100 }}
            class="z-20 {ntf.type} w-3/4 p-5 mt-3 rounded-md text-center"
        >
            {ntf.message}
        </button>
    {/each}
</div>