import { PUBLIC_API_ENDPOINT } from '$env/static/public';

export interface IMember {
	id: string;
	username: string;
	tokens: number;
	is_admin: boolean;
}

export interface ITeam {
	id: string;
	name: string;
	members: Array<IMember>;
}

export interface IUser {
	username: string;
	teams: Array<ITeam>;
	invites: Array<ITeam>;
}

const ENDPOINT = PUBLIC_API_ENDPOINT;

export const get_session_token: (username: string, password: string) => Promise<string> = async (
	username: string,
	password: string
) => {
	const response = await fetch(`${ENDPOINT}/users/session`, {
		body: JSON.stringify({ username: username, password: password }),
		method: 'POST',
		headers: { 'Content-Type': 'application/json' }
	});
	if (!response.ok) {
		throw new Error((await response.json()).detail);
	}
	return await response.json();
};

export const createAccount: (username: string, password: string) => Promise<string> = async (
	username: string,
	password: string
) => {
	const response = await fetch(`${ENDPOINT}/users`, {
		body: JSON.stringify({ username: username, password: password }),
		method: 'POST',
		headers: { 'Content-Type': 'application/json' }
	});
	if (!response.ok) {
		throw new Error((await response.json()).detail);
	}
	return await response.json();
};

export const getUser: (session: string) => Promise<IUser> = async (session: string) => {
	const response = await fetch(`${ENDPOINT}/users`, {
		method: 'GET',
		headers: { 'Content-Type': 'application/json', session: session }
	});
	if (!response.ok) {
		throw new Error((await response.json()).detail);
	}
	const data = await response.json();
	data.invites.forEach((team: ITeam) => (team.members = []));
	data.teams.forEach((team: ITeam) => (team.members = []));
	return data;
};

export const inviteReply: (
	session: string,
	team_id: string,
	accepted: boolean
) => Promise<void> = async (session: string, team_id: string, accepted: boolean) => {
	const response = await fetch(`${ENDPOINT}/teams/invite/reply`, {
		body: JSON.stringify({ team_id: team_id, accepted: accepted }),
		method: 'POST',
		headers: { 'Content-Type': 'application/json', session: session }
	});
	if (!response.ok) {
		throw new Error((await response.json()).detail);
	}
	return await response.json();
};

export const getMembers: (session: string, team_id: string) => Promise<Array<IMember>> = async (
	session: string,
	team_id: string
) => {
	const response = await fetch(`${ENDPOINT}/teams/${team_id}/members`, {
		method: 'GET',
		headers: { 'Content-Type': 'application/json', session: session }
	});
	if (!response.ok) {
		throw new Error((await response.json()).detail);
	}
	return await response.json();
};

export const createTeam: (session: string, name: string) => Promise<ITeam> = async (
	session: string,
	name: string
) => {
	const response = await fetch(`${ENDPOINT}/teams`, {
		body: JSON.stringify({ name: name }),
		method: 'POST',
		headers: { 'Content-Type': 'application/json', session: session }
	});
	if (!response.ok) {
		throw new Error((await response.json()).detail);
	}
	return { id: await response.json(), name: name, members: new Array<IMember>() };
};

export const inviteMember: (
	session: string,
	team_id: string,
	user_id: string
) => Promise<void> = async (session: string, team_id: string, username: string) => {
	const response = await fetch(`${ENDPOINT}/teams/invite`, {
		body: JSON.stringify({ team_id: team_id, username: username }),
		method: 'POST',
		headers: { 'Content-Type': 'application/json', session: session }
	});
	if (!response.ok) {
		throw new Error((await response.json()).detail);
	}
	return await response.json();
};

export const transfer: (
	session: string,
	team_id: string,
	user_id: string,
	value: number
) => Promise<void> = async (session: string, team_id: string, user_id: string, value: number) => {
	const response = await fetch(`${ENDPOINT}/transfer`, {
		body: JSON.stringify({ team_id: team_id, user_id: user_id, value: value }),
		method: 'POST',
		headers: { 'Content-Type': 'application/json', session: session }
	});
	if (!response.ok) {
		throw new Error((await response.json()).detail);
	}
	return await response.json();
};

export const reward: (
	session: string,
	team_id: string,
	user_id: string,
	value: number
) => Promise<void> = async (session: string, team_id: string, user_id: string, value: number) => {
	const response = await fetch(`${ENDPOINT}/reward`, {
		body: JSON.stringify({ team_id: team_id, user_id: user_id, value: value }),
		method: 'POST',
		headers: { 'Content-Type': 'application/json', session: session }
	});
	if (!response.ok) {
		throw new Error((await response.json()).detail);
	}
	return await response.json();
};
