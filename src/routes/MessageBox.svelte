<script lang="ts">
	import type { Sender } from '$lib/index';
	import { marked } from 'marked';

	export let content: string;
	export let sender: Sender;

	export let loading: boolean = false;

</script>

<div class="flex {sender === 'user' ? 'justify-end' : 'justify-start'} my-2">
	<div class="text-white p-3 max-w-xs md:max-w-md rounded-xl shadow-md flex-wrap
			{sender === 'user' ? 'bg-blue-500' : 'bg-gray-700'}
      {sender === 'user' ? 'rounded-br-none' : 'rounded-bl-none'} ">

		<!-- Display content or loading animation -->
		{#if loading}
			<div class="flex justify-center items-center">
				<svg class="animate-spin h-5 w-5 mr-3 text-white" xmlns="http://www.w3.org/2000/svg" fill="none"
						 viewBox="0 0 24 24">
					<circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
					<path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v8h8a8 8 0 01-16 0z"></path>
				</svg>
				<p class="text-lg">Model is generating response...</p>
			</div>
		{:else}
			<p class="markdown-content
				{sender === 'model' ? 'prose dark:prose-invert' : ''}">
				{@html marked.parse(content)}
			</p>
		{/if}

	</div>

</div>