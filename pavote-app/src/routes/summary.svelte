<script lang="ts">
	import { onMount } from 'svelte';

	export let mode: string;
	export let dataNow: any;
	export let electionMetadata: any;
	export let connected: boolean;
	export let updated: any;
	export let phillyUpdated: any;

	let results: any = {};
	let total = 0;

	let resultsArr: any = [];

	$: {
		resultsArr = Object.entries(results).map(([name, r]) => ({
			party: name,
			votes: r
		}));
		resultsArr.sort((a: any, b: any) => b.votes - a.votes);
		console.log(resultsArr);
	}

	let updatedAgo: any = null;
	let phillyUpdatedAgo: any = null;
	let invalidator = false;

	$: {
		if (updated) {
			updatedAgo = updated.fromNow();
		}
		if (phillyUpdated) {
			phillyUpdatedAgo = phillyUpdated.fromNow();
		}
		invalidator;
	}

	let invalidatorInterval: any = null;

	onMount(() => {
		invalidatorInterval = setInterval(() => {
			invalidator = !invalidator;
		}, 1000);
		return () => {
			clearInterval(invalidatorInterval);
		};
	});

	$: {
		const parties: any = {};
		if (dataNow) {
			for (const party of ['dem', 'rep', 'lib', 'grn']) {
				results[party] = Object.values(dataNow)
					.map((c: any) => c[party])
					.reduce((a, b) => a + b);
			}
			total = Object.values(results).reduce((a: any, b: any) => a + b) as number;
		}
	}
</script>

<div class="sticky top-0 p-16 pt-4 pb-4 border-black border-b-4 bg-blue-50 z-40">
	<h1 class="h1">PA 2024 Presidential Election Results</h1>
	{#if mode === 'test'}
		<h2 class="h2">TEST DATA! TEST DATA!</h2>
	{/if}
	<p>
		{#if connected}
			🟢 WebSockets connected! (No need to refresh!)
		{:else}
			🔴 WebSockets disconnected. Reconnecting!
		{/if}
	</p>
	<p>
		{#if updatedAgo}PA updated {updatedAgo}, {updated.calendar()}{/if} /
		{#if phillyUpdatedAgo}Philly updated {phillyUpdatedAgo}, {phillyUpdated.calendar()}{/if}
	</p>
</div>

<div class="card p-8 m-8">
	<h3 class="mb-4">Welcome!</h3>
	<p class="mb-4">
		On election night and the days that follow, this site will update in real time with data from
		Pennsylvania's and Philadelphia's election returns site, with a few charts and maps that I hope
		can illustrate how this election compares to 2020.
	</p>
	<p class="mb-4">
		Data is updated in your browser in real-time -- there's no need to refresh the page. You won't
		get updated data faster by doing so. The server hosting this page tries to fetch new data a few
		times a minute.
	</p>
	<p class="mb-4">
		I built this site in a weekend so that we can all be updated about how PA's election is going as
		soon as possible, but needless to say it's rough around the edges and I can't make any
		guarantees around the data or what the visualizations might imply. <b
			>In particular: I have no access to data about turnout or completeness of reporting, and if
			results come in slowly it may appear as if a county's or division's turnout is low. The charts
			can still be useful for understanding where results might be headed. Just understand what you
			are seeing.</b
		>
	</p>
	<p class="mb-4">
		Source code is available <a href="https://github.com/sharph/paelectionresults" target="_blank"
			>on GitHub</a
		>. (It's a bit rough, but I did rush to get it working over the weekend.) Data is from
		<a href="https://www.electionreturns.pa.gov/" target="_blank">
			https://www.electionreturns.pa.gov/</a
		>
		and
		<a href="https://vote.phila.gov/results/" target="_blank">https://vote.phila.gov/results/</a>.
		<a href="https://www.pasda.psu.edu/uci/DataSummary.aspx?dataset=24"
			>County boundries shapefile.</a
		>
		<a href="https://opendataphilly.org/datasets/political-ward-divisions/"
			>Philly Ward-Division shapefile.</a
		>
	</p>
	<p class="mb-4">
		- sharp<br /><a href="https://bsky.app/profile/sharphall.org" target="_blank"
			>🦋 @sharphall.org</a
		>
	</p>
</div>
<div class="card p-8 m-8">
	<div class="table-container">
		<table class="table table-hover">
			<thead>
				<tr>
					<th>Name</th>
					<th>Party</th>
					<th>Votes</th>
					<th>%</th>
				</tr>
			</thead>
			<tbody>
				{#each resultsArr as result}
					<tr>
						<td>{electionMetadata[result.party].candidateName}</td>
						<td>{electionMetadata[result.party].partyName}</td>
						<td>{result.votes.toLocaleString()}</td>
						<td
							>{Number(result.votes / total).toLocaleString(undefined, {
								style: 'percent',
								minimumFractionDigits: 2
							})}</td
						>
					</tr>
				{/each}
			</tbody>
			<tfoot>
				<tr>
					<th>Total</th>
					<td></td>
					<td>{total.toLocaleString()}</td>
					<td>100%</td>
				</tr>
			</tfoot>
		</table>
	</div>
</div>

<style type="css">
	a {
		color: #0033ff;
	}
</style>
