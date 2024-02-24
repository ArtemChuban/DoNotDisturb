import { derived, writable } from 'svelte/store';
import { dictionary } from './translations';
import russia from '$lib/assets/russia.svg';
import usa from '$lib/assets/usa.svg';

const flags: Record<string, string> = { en: usa, ru: russia };

export const locales = Object.keys(dictionary);
export const locale = writable(locales[0]);
export const flagIcon = writable('');

locale.subscribe((value) => {
	flagIcon.set(flags[value]);
});

type Vars = Record<string, string>;

function translate(locale: string, key: string, vars: Vars) {
	if (!key) throw new Error('no key provided to $t()');
	if (!locale) throw new Error(`no translation for key "${key}"`);

	let text = dictionary[locale][key];

	if (!text) throw new Error(`no translation found for ${locale}.${key}`);

	Object.keys(vars).map((k) => {
		const regex = new RegExp(`{{${k}}}`, 'g');
		text = text.replace(regex, vars[k]);
	});

	return text;
}

export const t = derived(
	locale,
	($locale) =>
		(key: string, vars = {}) =>
			translate($locale, key, vars)
);
