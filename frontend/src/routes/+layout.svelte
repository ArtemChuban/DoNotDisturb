<script lang="ts">
	import '../app.postcss';

	// Floating UI for Popups
	import { computePosition, autoUpdate, flip, shift, offset, arrow } from '@floating-ui/dom';
	import { Modal, storePopup } from '@skeletonlabs/skeleton';
	storePopup.set({ computePosition, autoUpdate, flip, shift, offset, arrow });

	import { initializeStores } from '@skeletonlabs/skeleton';
	initializeStores();
</script>

<Modal />

<div class="flex flex-col w-full h-full justify-center items-center">
	<slot />
</div>

<!-- == Страница регистрации (/register):
Форма логин + пароль + повтор пароля

== Страница входа (/login):
Форма логин + пароль

== Страница своих команд (/):
Список всех команд, где есть вользователь, при нажатии переход на эту команду
Список всех приглашений в команды с кнопкой принять и отклонить
Кнопка создания новой команды

== Страница команды (/{team_name}):
Таблица лидеров участников, рядом с каждым есть кнопка перевести - модалка
Если админ, то:
- Рядом с каждым пользователем есть кнопка дать или забрать права администратора - вспывает подтверждение
- Есть кнопка наградить - модалка

username password id

id team_name role tokens -->
