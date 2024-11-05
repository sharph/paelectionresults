<script lang="ts">
	import CountyPlot from './countyPlot.svelte';
	import { connect, PubSub } from '$lib/livedata';
	import { onMount } from 'svelte';
	import Summary from './summary.svelte';
	import CountyMap from './countyMap.svelte';
	import PhillyPlot from './phillyPlot.svelte';
	import PhillyMap from './phillyMap.svelte';

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
	let philly_mode = '';
	let data_2024: any = null;
	let data_2020: any = null;

	let data_phl_2024: any = null;
	let data_phl_2020: any = null;

	onMount(() => {
		pubsub = connect();
		pubsub.subscribe('2020_pa_presidential', (data) => {
			data_2020 = data;
		});
		pubsub.subscribe('2024_pa_presidential', (data) => {
			data_2024 = data.data;
			mode = data.mode;
		});
		pubsub.subscribe('2020_philly_presidential', (data) => {
			data_phl_2020 = data;
		});
		pubsub.subscribe('2024_philly_presidential', (data) => {
			data_phl_2024 = data.data;
			philly_mode = data.mode;
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
	<CountyMap dataNow={data_2024} dataThen={data_2020} {electionMetadata} {mode} />
	<CountyPlot dataNow={data_2024} dataThen={data_2020} {mode} />
	<PhillyPlot dataNow={data_phl_2024} dataThen={data_phl_2020} mode={philly_mode} />
	<PhillyMap
		dataNow={data_phl_2024}
		dataThen={data_phl_2020}
		{electionMetadata}
		mode={philly_mode}
	/>
</div>
