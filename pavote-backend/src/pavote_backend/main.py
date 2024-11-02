from typing import Union

from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect
import os

import aiopubsub
import asyncio
import json
import redis.asyncio as redis
from typing import Optional

app = FastAPI()
hub = aiopubsub.Hub()
redis_pool: Optional[redis.ConnectionPool] = None

ALLOWED_TOPICS = ["2020_pa_presidential", "2024_pa_presidential"]

current_states = {k: None for k in ALLOWED_TOPICS}

def get_handler(topic, websocket: WebSocket, subscriber):
    async def handle_data(key, data):
        try:
            await websocket.send_json({"topic": topic, "data": data})
        except RuntimeError:
            await subscriber.remove_all_listeners()

    return handle_data


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()

    while True:
        try:
            msg = await websocket.receive_json()
        except WebSocketDisconnect:
            return
        if 'subscribe' in msg and msg['subscribe'] in ALLOWED_TOPICS:
            sub = aiopubsub.Subscriber(hub, websocket.client.host)
            key = aiopubsub.Key("pubsub", msg['subscribe'])
            await websocket.send_json({"subscribed":  msg['subscribe']})
            if current_states[msg['subscribe']] is not None:
                await websocket.send_json({"topic": msg["subscribe"], "data": current_states[msg['subscribe']]})
            sub.add_async_listener(key, get_handler(msg['subscribe'], websocket, sub))
        else:
            await websocket.send_json({"not_subscribed": msg['subscribe']})


async def handle_pubsub_message(msg):
    decoded = json.loads(msg)
    if decoded['topic'] not in ALLOWED_TOPICS:
        return
    publisher = aiopubsub.Publisher(hub, aiopubsub.Key("pubsub"))
    current_states[decoded['topic']] = decoded['message']
    publisher.publish(aiopubsub.Key(decoded['topic']), decoded['message'])


async def setup_redis_pool():
    global redis_pool
    redis_pool = redis.ConnectionPool.from_url(os.getenv("REDIS_URL", 'redis://localhost'))

async def read_initial():
    client = redis.Redis(connection_pool=redis_pool)
    for topic in ALLOWED_TOPICS:
        msg = await client.get(f"pubsub_{topic}")
        if msg is not None:
            await handle_pubsub_message(msg)
        else:
            print(f"no existing message for {topic}")
    await client.aclose()


async def pubsub():
    while True:
        try:
            print("init pubsub")
            async def reader(channel: redis.client.PubSub):
                while True:
                    message = await channel.get_message(ignore_subscribe_messages=True, timeout=None)
                    if message is not None:
                        try:
                            await handle_pubsub_message(message['data'].decode())
                        except Exception:
                            pass
            client = redis.Redis(connection_pool=redis_pool)
            try:
                async with client.pubsub() as pubsub:
                    await pubsub.subscribe("pubsub")
                    await read_initial()
                    await reader(pubsub)
            finally:
                await asyncio.sleep(5)
                await client.aclose()
        except Exception:
            print("pubsub broke")



@app.on_event("startup")
async def start_loop():
    await setup_redis_pool()
    asyncio.create_task(pubsub())
