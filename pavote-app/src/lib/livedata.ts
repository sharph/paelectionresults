import { env } from '$env/dynamic/public';

const WS_URL = env.PUBLIC_WS_URL || 'ws://localhost:8000/ws';

type MessageCallback = (msg: any) => any;

export class PubSub {
	url: string;
	ws: WebSocket | null;
	onConnectionStatusChange: ((connected: boolean) => void) | null;
	handlers: Map<string, MessageCallback[]>;
	reconnect: boolean;

	subscribe(topic: string, messageCallback: MessageCallback) {
		const callbacks = this.handlers.get(topic);
		if (callbacks === undefined) {
			const callbacks = [messageCallback];
			this.handlers.set(topic, callbacks);
			if (this.ws && this.ws.readyState == WebSocket.OPEN) {
				this.ws.send(JSON.stringify({ "subscribe": topic }));
			}
		} else {
			callbacks.push(messageCallback);
		}
	}

	setOnConnectionStatusChange(cb: (connected: boolean) => void) {
		this.onConnectionStatusChange = cb;
	}

	connect() {
		const ws = new WebSocket(this.url);
		this.ws = ws;
		ws.onopen = () => {
			if (this.onConnectionStatusChange) {
				this.onConnectionStatusChange(true);
			}
			for (const topic of this.handlers.keys()) {
				ws.send(JSON.stringify({ "subscribe": topic }));
			}
		};
		ws.onclose = async () => {
			if (this.onConnectionStatusChange) {
				this.onConnectionStatusChange(false);
			}
			await new Promise((res) => setTimeout(res, 5000));
			this.connect()
		};
		ws.onmessage = (ev) => {
			const msg = JSON.parse(ev.data);
			if (msg.topic === undefined) {
				return;
			}
			for (const topic of this.handlers.keys()) {
				if (msg.topic === topic) {
					const callbacks = this.handlers.get(topic);
					if (callbacks === undefined) {
						return;
					}
					for (const handler of callbacks) {
						handler(msg.data);
					}
				}
			}
		};
	}

	close() {
		this.reconnect = false;
		if (this.ws) {
			this.ws.close();
		}
		this.ws = null;
	}

	constructor(url: string) {
		this.onConnectionStatusChange = null;
		this.url = url;
		this.ws = null;
		this.handlers = new Map();
		this.reconnect = true;
		this.connect();
	}
}

export function connect() {
	return new PubSub(WS_URL);
}
