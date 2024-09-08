<script lang="ts">
	import { type Message, Sender } from '$lib/index';
	import MessageBox from './MessageBox.svelte';
	import InputField from './InputField.svelte';
	import { afterUpdate } from 'svelte';
	import { page } from '$app/stores';
	import ErrorBox from './ErrorBox.svelte';

	export let data: { messages: Message[] };

	let isLoading = false;

	let messageContainer: HTMLDivElement;

	afterUpdate(() =>
		scrollToBottom()
	);

	function scrollToBottom() {
		messageContainer.scrollTop = messageContainer.scrollHeight;
	}

	$: formData = $page.form;
</script>


<div class="flex flex-row justify-center h-[92%]">
	<div class="flex flex-col w-1/2 m-2">
		<div bind:this={messageContainer}
				 class="flex flex-col bg-gray-950 overflow-y-scroll overflow-x-clip h-full p-3 rounded-lg scroll-smooth">
			<ul>
				{#each data.messages as mes}
					<li>
						<MessageBox content={mes.content} sender={mes.sender} />
					</li>
				{/each}
				{#if isLoading}
					<li>
						<MessageBox content="..." sender={Sender.Model} loading={true} />
					</li>
				{/if}
				{#if formData?.no_response}
					<ErrorBox errorMessage={formData.error} />
				{/if}
			</ul>
		</div>
		<InputField bind:isLoading={isLoading} bind:messages={data.messages} />
	</div>
</div>