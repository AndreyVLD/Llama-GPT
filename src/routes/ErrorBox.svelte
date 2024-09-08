<script lang="ts">
	export let errorMessage: string | undefined;
</script>

<div class="flex items-center justify-center">
	<div class="bg-red-500 text-white text-lg font-bold p-4 rounded-lg shadow-lg">
		{errorMessage}
	</div>
</div>