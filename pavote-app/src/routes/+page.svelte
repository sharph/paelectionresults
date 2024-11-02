<script lang="ts">
	import CountyPlot from './countyPlot.svelte';
	import { connect, PubSub } from '$lib/livedata';
	import { onMount } from 'svelte';
	import Summary from './summary.svelte';

	let log = false;
	let connected = false;

	const electionMetadata = {
		dem: {
			partyName: 'Democratic',
			candidateName: 'Kamala D. Harris'
		},
		rep: {
			partyName: 'Republican',
			candidateName: 'Donald J. Trump'
		},
		lib: {
			partyName: 'Libertarian',
			candidateName: 'Chase Oliver'
		},
		grn: {
			partyName: 'Green',
			candidateName: 'Jill Stein'
		}
	};

	let pubsub: PubSub | null = null;

	let mode = '';
	let data_2024: any = null;
	let data_2020: any = null;

	onMount(() => {
		pubsub = connect();
		pubsub.subscribe('2020_pa_presidential', (data) => {
			data_2020 = data;
		});
		pubsub.subscribe('2024_pa_presidential', (data) => {
			data_2024 = data.data;
			mode = data.mode;
		});
		pubsub.setOnConnectionStatusChange((c) => {
			connected = c;
		});

		return () => {
			if (pubsub) {
				pubsub.close();
			}
		};
	});
</script>

<div class="">
	<Summary {mode} dataNow={data_2024} {electionMetadata} {connected} />
	<CountyPlot dataNow={data_2024} dataThen={data_2020} {mode} />
</div>
