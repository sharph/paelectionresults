<script lang="ts">
	import { BaseMap, FeatureLayer } from 'svelte-geo';
	import countyGeoJson from './PaCounties2024Simplified.geojson.json';

	export let dataNow: any;
	export let dataThen: any;
	export let mode: string;
	export let electionMetadata: any;

	let zoomReset: any;
	const partyColors: Record<string, string> = {
		rep: '#aa0505',
		dem: '#013d72',
		lib: '#eec531',
		grn: '#6c9a55'
	};

	function toTitleCase(str: string) {
		return str.replace(
			/\w\S*/g,
			(text) => text.charAt(0).toUpperCase() + text.substring(1).toLowerCase()
		);
	}

	let then = false;
	let colors: any = {};
	let percents: any = {};
	let text: any = {};
	let data: any = null;

	$: {
		if (then) {
			data = dataThen;
		} else {
			data = dataNow;
		}
	}

	$: {
		colors = {};
		percents = {};
		text = {};
		if (data) {
			for (const [name, countyData] of Object.entries(data)) {
				const total = Object.values(countyData as any).reduce((a: any, b: any) => a + b) as number;
				if (total === 0) {
					colors[name] = '#ffffff';
					percents[name] = 0.0;
					text[name] = [name];
					continue;
				}
				const resultArr = Object.entries(countyData as any).sort(
					(a: any, b: any) => b[1] - a[1]
				) as [any, any][];
				colors[name] = partyColors[resultArr[0][0] as string];
				percents[name] = Math.max(0, resultArr[0][1] / total - 0.4) / 0.6;
				text[name] = [`${name} `];
				text[name].push(
					Number(resultArr[0][1] / total).toLocaleString(undefined, {
						style: 'percent',
						minimumFractionDigits: 2
					})
				);
				console.log(text[name]);
			}
		}
	}

	let textElement: any;
	$: textBoxWidth = textElement ? textElement.getComputedTextLength() + 10 : 0;
</script>

<div class="card p-8 m-8">
	<h2 class="h2">
		Pennsylvania County Map
		{#if then}(2020)
		{:else if mode === 'test'}(TEST DATA!){/if}
	</h2>
	<div class="space-y-2">
		<label class="flex items-center space-x-2">
			<input class="checkbox" type="checkbox" bind:checked={then} />
			<p>Show 2020</p>
		</label>
	</div>
	<div
		class="map"
		on:mouseleave={() => {
			if (zoomReset) {
				zoomReset();
			}
		}}
	>
		<BaseMap margin={{ left: 0, right: 0, top: 0, bottom: 0 }} bind:zoomReset>
			<FeatureLayer
				geojson={countyGeoJson}
				styleAccessor={(feature) => ({
					fill: colors[toTitleCase(feature.properties.COUNTY_NAM)] || '#ffffff',
					'fill-opacity': percents[toTitleCase(feature.properties.COUNTY_NAM)],
					stroke: 'black',
					'stroke-width': 2,
					'vector-effect': 'non-scaling-stroke'
				})}
				let:hoveredFeature
			>
				<rect
					width={textBoxWidth}
					height="21"
					x={-0.5 * textBoxWidth}
					y="-15"
					rx="10"
					fill="white"
					opacity="0.8"
				/>
				<text text-anchor="middle" bind:this={textElement}>
					{#if text[toTitleCase(hoveredFeature?.properties.COUNTY_NAM)]}
						{#each text[toTitleCase(hoveredFeature?.properties.COUNTY_NAM)] as line}
							{line}
						{/each}
					{/if}
				</text>
			</FeatureLayer>
		</BaseMap>
	</div>
</div>

<style lang="css">
	.map {
		width: 40em;
		height: 40em;
	}

	@media only screen and (max-width: 600px) {
		.map {
			width: 20em;
			height: 20em;
		}
	}
</style>
