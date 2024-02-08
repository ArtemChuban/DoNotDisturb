import { goto } from "$app/navigation";

export const BACKEND_URL = "http://127.0.0.1:8000";

export interface User {
	username: string;
	is_admin: boolean;
	tokens: number;
}

export const getUser: () => Promise<User | null>  = async () => {
	const session = localStorage.getItem('session');
		if (session === null) {
			goto('/login');
			return null;
		}
		try {
			const response = await fetch(`${BACKEND_URL}/users/by/session?session=${session}`, {
				method: 'GET'
			})
			if (!response.ok) {
				return null;
			}
			return await response.json();
		}
		catch (err) {
			console.error(err);
		}
		return null;
}

export const getUserByUsername: (username: string) => Promise<User | null> = async (username: string) => {
	try {
		const response = await fetch(`${BACKEND_URL}/users/by/username?username=${username}`, {
			method: 'GET'
		})
		if (!response.ok) {
			return null;
		}
		return await response.json();
	}
	catch (err) {
		console.error(err);
	}
	return null;
}