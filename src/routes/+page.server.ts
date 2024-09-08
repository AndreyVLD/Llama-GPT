import type { Actions, PageServerLoad } from './$types';
import { addMessage, getAllMessages, getHistory } from '$lib/database/messages';
import { Sender } from '$lib/index';
import { fail } from '@sveltejs/kit';

export const load: PageServerLoad = async () => {
	const messages = await getAllMessages();

	return { messages: messages.map((v) => v.toJSON()) };
};

export const actions = {
	submit: async (event) => {
		const formData = await event.request.formData();
		const userQuery = formData.get('userInput') as string;
		const trimmedMessage = userQuery.trim();
		if (trimmedMessage === '')
			return;

		const history = await getHistory(10);
		await addMessage(userQuery, Sender.User);

		let response;
		try {
			response = await fetch('http://127.0.0.1:8000/infer/normal', {
				method: 'POST',
				headers: {
					'Content-Type': 'application/json'
				},
				body: JSON.stringify({
					query: userQuery,
					history: history
				})
			});
		} catch {
			return fail(400, { error: 'Model server is not online', no_response: true });
		}

		const data = await response.json();

		await addMessage(data.response, Sender.Model);

		return { success: true };
	}
} satisfies Actions;
