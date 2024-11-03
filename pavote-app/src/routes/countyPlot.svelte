<script lang="ts">
	import Plot from 'svelte-plotly.js';

	export let dataNow: any;
	export let dataThen: any;
	export let mode: string;

	let log = false;
	let showThen = false;

	let data: any = [];
	let max = 0;

	function findCounty(needle: string, haystack: any): any {
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
			for (const [name, countyData_] of Object.entries(dataNow)) {
				let countyData = countyData_ as any;
				max = Math.max(max, countyData.dem, countyData.rep);
				let thenCounty = null;
				if (dataThen && showThen) {
					thenCounty = findCounty(name, dataThen);
				}
				if (thenCounty) {
					if (countyData.dem !== 0 || countyData.rep !== 0) {
						data.push({
							x: [thenCounty.rep, countyData.rep, null],
							y: [thenCounty.dem, countyData.dem, null],
							mode: 'lines+markers',
							name: name,
							marker: {
								symbol: 'arrow',
								size: 16,
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
							x: [thenCounty.rep],
							y: [thenCounty.dem],
							text: [`${name} 2020`],
							mode: 'markers',
							name: name,
							marker: {
								size: 8
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
						x: [countyData.rep],
						y: [countyData.dem],
						text: [`${name} 2024`],
						mode: 'markers',
						name: name,
						marker: {
							size: 8
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
		range: [2, 6],
		type: 'log'
	};

	let linearScale;
	$: linearScale = {
		range: [0, max + 100000]
	};
</script>

<div class="card p-8 m-8">
	<h2 class="h2">Votes for President in Pennsylvania Counties</h2>
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
				title: `Votes for President in Pennsylvania Counties${mode !== 'live' ? ' (TEST DATA!)' : ''}`,
				paper_bgcolor: 'rgba(243,244,246,255)'
			}}
			debounce={250}
			fillParent={true}
		/>
	</div>
</div>
