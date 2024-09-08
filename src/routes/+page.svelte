<script lang="ts">
	import Chat from './Chat.svelte';
	import type { PageData } from './$types';

	export let data: PageData;
</script>


<p class="text-center text-2xl text-gray-300 m-3">
	Chat Llama
</p>


<Chat data={data} />




