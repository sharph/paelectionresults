<script lang="ts">
	import { BaseMap, FeatureLayer } from 'svelte-geo';
	import phillyGeoJson from './philly.geojson.json';

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

	function insDash(str?: string) {
		if (!str) {
			return null;
		}
		return str.substring(0, 2) + '-' + str.substring(2, 4);
	}

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
			for (const [name, divData] of Object.entries(data)) {
				const total = Object.values(divData as any).reduce((a: any, b: any) => a + b) as number;
				if (total === 0) {
					colors[name] = '#ffffff';
					percents[name] = 0.0;
					text[name] = [name];
					continue;
				}
				const resultArr = Object.entries(divData as any).sort((a: any, b: any) => b[1] - a[1]) as [
					any,
					any
				][];
				colors[name] = partyColors[resultArr[0][0] as string];
				percents[name] = Math.max(0, resultArr[0][1] / total - 0.4) / 0.6;
				text[name] = [`${name} `];
				text[name].push(
					Number(resultArr[0][1] / total).toLocaleString(undefined, {
						style: 'percent',
						minimumFractionDigits: 2
					})
				);
				console.log(name);
			}
		}
	}

	let textElement: any;
	$: textBoxWidth = textElement ? textElement.getComputedTextLength() + 10 : 0;
</script>

<div class="card p-8 m-8">
	<h2 class="h2">
		Philadelphia Ward-Division Map {#if mode === 'test'}(TEST DATA!){/if}
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
				geojson={phillyGeoJson}
				styleAccessor={(feature) => ({
					fill: colors[insDash(feature.properties.DIVISION_NUM)] || '#ffffff',
					'fill-opacity': percents[insDash(feature.properties.DIVISION_NUM)],
					stroke: 'black',
					'stroke-width': 0,
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
					{#if text[insDash(hoveredFeature?.properties.DIVISION_NUM)]}
						{#each text[insDash(hoveredFeature?.properties.DIVISION_NUM)] as line}
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
		max-width: 40em;
		height: 40em;
	}
</style>
