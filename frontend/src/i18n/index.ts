import { addMessages, init } from 'svelte-i18n';

import en from './en.json';
import ru from './ru.json';

addMessages('en', en);
addMessages('ru', ru);
init({
	fallbackLocale: 'en',
	initialLocale: 'ru'
});
