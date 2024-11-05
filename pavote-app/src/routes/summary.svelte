<script lang="ts">
	export let mode: string;
	export let dataNow: any;
	export let electionMetadata: any;
	export let connected: boolean;

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

<div class="p-8 m-8">
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
		Data: <a href="https://www.electionreturns.pa.gov/" target="_blank">
			https://www.electionreturns.pa.gov/</a
		>,
		<a href="https://vote.phila.gov/results/" target="_blank">https://vote.phila.gov/results/</a>
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
