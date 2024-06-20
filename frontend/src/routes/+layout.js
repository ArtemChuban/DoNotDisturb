export const ssr = false;
export const trailingSlash = 'always';
export const prerender = true;

import '../i18n/index.ts'; // Import to initialize. Important :)
import { waitLocale } from 'svelte-i18n';

export const load = async () => {
	await waitLocale();
};
