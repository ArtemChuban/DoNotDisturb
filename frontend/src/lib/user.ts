import { writable } from 'svelte/store';

export const session = writable<string | null>(null);
export const username = writable<string | null>(null);
