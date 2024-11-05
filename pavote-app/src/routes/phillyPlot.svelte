<script lang="ts">
	import Plot from 'svelte-plotly.js';
	import { browser } from '$app/environment';

	export let dataNow: any;
	export let dataThen: any;
	export let mode: string;

	let log = false;
	let showThen = false;

	let data: any = [];
	let max = 0;

	function findDiv(needle: string, haystack: any): any {
		const found = Object.entries(haystack).filter(([name, data]) => name === needle)[0];
		if (found) {
			return found[1];
		} else {
			return null;
		}
	}

	$: {
		data = [];
		max = 0;
		if (dataNow) {
			for (const [name, divData_] of Object.entries(dataNow)) {
				let divData = divData_ as any;
				max = Math.max(max, divData.dem, divData.rep);
				let thenDiv = null;
				if (dataThen && showThen) {
					thenDiv = findDiv(name, dataThen);
				}
				if (thenDiv) {
					if (divData.dem !== 0 || divData.rep !== 0) {
						data.push({
							x: [thenDiv.rep, divData.rep, null],
							y: [thenDiv.dem, divData.dem, null],
							mode: 'lines+markers',
							name: name,
							marker: {
								symbol: 'arrow',
								size: 8,
								angleref: 'previous'
							},
							text: [`${name} 2020`, `${name} 2024`, null],
							hovertemplate:
								'<b>%{text}</b><br><br>' +
								'%{yaxis.title.text}: %{y}<br>' +
								'%{xaxis.title.text}: %{x}<br>' +
								'<extra></extra>'
						});
					} else {
						data.push({
							x: [thenDiv.rep],
							y: [thenDiv.dem],
							text: [`${name} 2020`],
							mode: 'markers',
							name: `${name} (2020)`,
							marker: {
								size: 4,
								width: 1
							},
							hovertemplate:
								'<b>%{text}</b><br><br>' +
								'%{yaxis.title.text}: %{y}<br>' +
								'%{xaxis.title.text}: %{x}<br>' +
								'<extra></extra>'
						});
					}
				} else {
					data.push({
						x: [divData.rep],
						y: [divData.dem],
						text: [`${name} 2024`],
						mode: 'markers',
						name: name,
						marker: {
							size: 4
						},
						hovertemplate:
							'<b>%{text}</b><br><br>' +
							'%{yaxis.title.text}: %{y}<br>' +
							'%{xaxis.title.text}: %{x}<br>' +
							'<extra></extra>'
					});
				}
			}
		}

		data.push({
			x: [0, 800000],
			y: [0, 800000],
			mode: 'lines'
		});
	}

	const logScale = {
		range: [1, 4],
		type: 'log'
	};

	let linearScale;
	$: linearScale = {
		range: [0, max + 100]
	};
</script>

<div class="card p-8 m-8">
	<h2 class="h2">Votes for President in Philadelphia Ward-Divisions</h2>
	<div class="space-y-2">
		<label class="flex items-center space-x-2">
			<input class="checkbox" type="checkbox" bind:checked={log} />
			<p>Log Scale</p>
		</label>
		<label class="flex items-center space-x-2">
			<input class="checkbox" type="checkbox" bind:checked={showThen} />
			<p>Show 2020</p>
		</label>
	</div>
	<div class="h-screen">
		<div class="h-5/6">
			<Plot
				{data}
				layout={{
					xaxis: {
						title: 'Votes Republican',
						...(log ? logScale : linearScale)
					},
					yaxis: {
						title: 'Votes Democrat',
						...(log ? logScale : linearScale)
					},
					title: `Votes for President in Philadelphia Ward-Divisions${mode !== 'live' ? ' (TEST DATA!)' : ''}`,
					paper_bgcolor: 'rgba(243,244,246,255)',
					showlegend: browser ? window.screen.width > 600 : false
				}}
				debounce={250}
				fillParent={true}
			/>
		</div>
	</div>
</div>
