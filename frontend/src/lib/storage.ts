import { localStorageStore } from '@skeletonlabs/skeleton';
import { writable } from 'svelte/store';
import { type ITeam, type IUser } from './api';

export const session = localStorageStore<string | null>('session', null);
export const user = writable<IUser>({ username: '', invites: [], teams: [] });
export const currentTeam = writable<ITeam>({ id: '', name: '', members: [] });
