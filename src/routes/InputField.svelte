<script lang="ts">
	import { enhance } from '$app/forms';
	import { Message, Sender } from '$lib/index';

	export let isLoading = false;
	export let messages: Message[];

	let userMessage: string;

</script>

<form action="?/submit" method="POST"
			use:enhance={() => {
					isLoading = true;

					if (userMessage && userMessage.toString().trim() !== '') {
						const message = new Message(Sender.User,userMessage.toString())
						messages = [...messages, message]
					}

					userMessage = '';

					return async ({update}) => {
						await update();
						isLoading = false;
					};
			}}
>
	<div class="flex items-center p-4 bg-gray-800 rounded-lg shadow-md w-full max-w-4xl mx-auto">
		<input
			bind:value={userMessage}
			class="flex-grow px-4 py-2 mr-4 bg-gray-700 text-gray-200 rounded-lg outline-none focus:ring-2 focus:ring-blue-500"
			name="userInput"
			placeholder="Send a message..."
			type="text"
		/>

		<button
			class="bg-blue-500 hover:bg-blue-600 active:bg-blue-800 text-white font-bold py-2 px-4
		rounded-lg shadow-md transition-colors duration-200 disabled:bg-blue-300 disabled:cursor-not-allowed
		disabled:opacity-50"
			disabled={isLoading}
			type="submit"
		>
			Send
		</button>
	</div>
</form>
