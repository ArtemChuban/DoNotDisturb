import { goto } from '$app/navigation';
import { env } from '$env/dynamic/public'

const BACKEND_URL = `http${env.PUBLIC_MODE === 'production' ? 's' : ''}://${env.PUBLIC_SERVER_NAME}/api`

export interface User {
	username: string;
	is_admin: boolean;
	tokens: number;
}

enum TransactionType {
	REWARD = 'Reward',
	TRANSFER = 'Transfer'
}

export interface Transaction {
	timestamp: number;
	initiator: string;
	reciever: string;
	value: number;
	type: TransactionType;
}

const throwError: (response: Response) => Promise<void> = async (response: Response) => {
	throw new Error((await response.json()).detail);
};

export const getUser: () => Promise<User> = async () => {
	const session = localStorage.getItem('session');
	if (session === null) {
		goto('/login');
		return null;
	}
	const response = await fetch(`${BACKEND_URL}/users/by/session?session=${session}`, {
		method: 'GET'
	});
	if (!response.ok) await throwError(response);

	return await response.json();
};

export const getUserByUsername: (username: string) => Promise<User> = async (username: string) => {
	const response = await fetch(`${BACKEND_URL}/users/by/username?username=${username}`, {
		method: 'GET'
	});
	if (!response.ok) await throwError(response);
	return await response.json();
};

export const getSession: (username: string, password: string) => Promise<string> = async (
	username: string,
	password: string
) => {
	const response = await fetch(
		`${BACKEND_URL}/users/session?username=${username}&password=${password}`,
		{ method: 'GET' }
	);
	if (!response.ok) await throwError(response);
	return await response.json();
};

export const changePassword: (
	session: string,
	username: string,
	new_password: string
) => Promise<void> = async (session: string, username: string, new_password: string) => {
	const response = await fetch(
		`${BACKEND_URL}/users/password?session=${localStorage.getItem('session')}&username=${username}&new_password=${new_password}`,
		{ method: 'PUT' }
	);
	if (!response.ok) await throwError(response);
};

export const getAllUsers: () => Promise<Array<User>> = async () => {
	const response = await fetch(`${BACKEND_URL}/users`);
	if (!response.ok) await throwError(response);
	return await response.json();
};

export const transfer: (session: string, username: string, value: number) => Promise<void> = async (
	session: string,
	username: string,
	value: number
) => {
	const response = await fetch(
		`${BACKEND_URL}/tokens/transfer?session=${session}&username=${username}&value=${value}`,
		{
			method: 'POST'
		}
	);
	if (!response.ok) await throwError(response);
};

export const getTransactions: (
	offset: number,
	limit: number,
	initiator: string | null,
	reciever: string | null
) => Promise<Array<Transaction>> = async (
	offset: number = 0,
	limit: number = 8,
	initiator: string | null = null,
	reciever: string | null = null
) => {
	let query = `offset=${offset}&limit=${limit}`;
	if (initiator !== null) {
		query += `&initiator=${initiator}`;
	}
	if (reciever !== null) {
		query += `&reciever=${reciever}`;
	}
	const response = await fetch(`${BACKEND_URL}/transactions?${query}`);
	if (!response.ok) await throwError(response);
	return await response.json();
};

export const createUser: (
	session: string,
	username: string,
	password: string
) => Promise<void> = async (session: string, username: string, password: string) => {
	const response = await fetch(
		`${BACKEND_URL}/users/create?session=${session}&username=${username}&password=${password}`,
		{ method: 'POST' }
	);
	if (!response.ok) await throwError(response);
};

export const reward = async (session: string, username: string, value: number) => {
	const response = await fetch(
		`${BACKEND_URL}/tokens/reward?session=${session}&username=${username}&value=${value}`,
		{
			method: 'POST'
		}
	);
	if (!response.ok) await throwError(response);
};
