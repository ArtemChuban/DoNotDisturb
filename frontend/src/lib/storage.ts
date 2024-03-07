import { localStorageStore } from '@skeletonlabs/skeleton';
import { writable } from 'svelte/store';
import { type ITeam, type IUser } from './api';

export const session = localStorageStore<string | null>('session', null);
export const user = writable<IUser>({ username: '', invites: [], teams: [], isAdmin: false });
export const currentTeam = writable<ITeam>({ id: '', name: '', members: [] });

// session.subscribe((value) => console.log('session', value));
// user.subscribe((value) => console.log('user', value));
// currentTeam.subscribe((value) => console.log('currentTeam', value));
