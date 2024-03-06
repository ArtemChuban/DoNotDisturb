import { localStorageStore } from '@skeletonlabs/skeleton';

export const jwt_token = localStorageStore<string | null>('jwt_token', null);
