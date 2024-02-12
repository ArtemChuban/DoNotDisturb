import { writable } from 'svelte/store';

export let session = writable<string | null>(null);
export let username = writable<string | null>(null);
