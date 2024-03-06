let counter = 0;

const randError = () => {
	counter++;
	if (counter % 2 === 0) throw new Error('Random error');
};

export const get_jwt_token: (username: string, password: string) => Promise<string> = async (
	username: string,
	password: string
) => {
	randError();
	return 'test-jwt-token';
};
