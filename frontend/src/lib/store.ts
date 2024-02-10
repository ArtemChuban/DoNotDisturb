import { writable, type Writable } from 'svelte/store';

export enum NotificationType {
	ERROR = 'bg-red-400',
	EMPTY = '',
	SUCCESS = 'bg-green-500'
}

export interface Notification {
	message: string;
	type: NotificationType;
}

export const notification = writable<Notification>({
	message: '',
	type: NotificationType.EMPTY
});
