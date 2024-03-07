export interface IMember {
	id: string;
	username: string;
	tokens: number;
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
	isAdmin: boolean;
}

export const get_session_token: (username: string, password: string) => Promise<string> = async (
	username: string,
	password: string
) => {
	console.log(`get_session_token(${username}, ${password})`);
	return `session:${username}:${password}`;
};

export const createAccount: (username: string, password: string) => Promise<string> = async (
	username: string,
	password: string
) => {
	console.log(`createAccount(${username}, ${password})`);
	return `session:${username}:${password}`;
};

export const getUser: (session: string) => Promise<IUser> = async (session: string) => {
	console.log(`getUser(${session})`);
	return {
		username: 'username',
		teams: [
			{ name: 'team1', id: '1', members: [] },
			{ name: 'team2', id: '2', members: [] },
			{ name: 'team3', id: '3', members: [] },
			{ name: 'team4', id: '4', members: [] }
		],
		invites: [
			{ name: 'new team 1', id: '101', members: [] },
			{ name: 'new team 2', id: '102', members: [] }
		],
		isAdmin: true
	};
};

export const inviteReply: (
	session: string,
	team_id: string,
	accepted: boolean
) => Promise<void> = async (session: string, team_id: string, accepted: boolean) => {
	console.log(`inviteReply(${session}, ${team_id}, ${accepted})`);
	return;
};

export const getMembers: (session: string, team_id: string) => Promise<Array<IMember>> = async (
	session: string,
	team_id: string
) => {
	console.log(`getMembers(${session}, ${team_id})`);
	return [
		{ id: '1', username: 'user1', tokens: 12 },
		{ id: '2', username: 'user2', tokens: 24 },
		{ id: '3', username: 'username', tokens: 36 },
		{ id: '4', username: 'user4', tokens: 48 },
		{ id: '5', username: 'ashjfioefesa', tokens: 25 },
		{ id: '6', username: 'user6', tokens: 327 },
		{ id: '7', username: 'user7', tokens: 2 }
	];
};

export const createTeam: (session: string, name: string) => Promise<ITeam> = async (
	session: string,
	name: string
) => {
	console.log(`createTeam(${session}, ${name})`);
	return { id: name, name: name, members: [] };
};

export const inviteMember: (
	session: string,
	team_id: string,
	user_id: string
) => Promise<void> = async (session: string, team_id: string, username: string) => {
	console.log(`inviteMember(${session}, ${team_id}, ${username})`);
	return;
};

export const transfer: (
	session: string,
	team_id: string,
	user_id: string,
	value: number
) => Promise<void> = async (session: string, team_id: string, user_id: string, value: number) => {
	console.log(`transfer(${session}, ${team_id}, ${user_id}, ${value})`);
	return;
};

export const reward: (
	session: string,
	team_id: string,
	user_id: string,
	value: number
) => Promise<void> = async (session: string, team_id: string, user_id: string, value: number) => {
	console.log(`reward(${session}, ${team_id}, ${user_id}, ${value})`);
	return;
};
