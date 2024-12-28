<script lang="ts">
	import { getAdminDetails } from '$lib/apis/auths';
	import { onMount, onDestroy, tick, getContext } from 'svelte';

	const i18n = getContext('i18n');

	let timeoutHandle: NodeJS.Timeout | null = null;

	async function refreshPage() {
		window.location.reload();
	}

	onMount(async () => {
		timeoutHandle = setInterval(async () => {
			await refreshPage();
		}, 30000);
	});

	onDestroy(() => {
		if (timeoutHandle) {
			clearTimeout(timeoutHandle);
		}
	});
</script>

<div class="fixed w-full h-full flex z-[999]">
	<div
		class="absolute w-full h-full backdrop-blur-lg bg-white/10 dark:bg-gray-900/50 flex justify-center"
	>
		<div class="m-auto pb-10 flex flex-col justify-center">
			<div class="max-w-md">
				<div class="text-center dark:text-white text-2xl font-medium z-50">
					{$i18n.t('Account setup pending')}
				</div>

				<div class=" mt-4 text-center text-sm dark:text-gray-200 w-full">
					{$i18n.t('We are currently preparing your account, this may take a few seconds.')}
				</div>

				<div class=" mt-6 mx-auto relative group w-fit">
					<button
						class="relative z-20 flex px-5 py-2 rounded-full bg-white border border-gray-100 dark:border-none hover:bg-gray-100 text-gray-700 transition font-medium text-sm"
						on:click={async () => {
							location.href = '/';
						}}
					>
						{$i18n.t('Check Again')}
					</button>

					<button
						class="text-xs text-center w-full mt-2 text-gray-400 underline"
						on:click={async () => {
							localStorage.removeItem('token');
							location.href = '/auth';
						}}>{$i18n.t('Sign Out')}</button
					>
				</div>
			</div>
		</div>
	</div>
</div>
