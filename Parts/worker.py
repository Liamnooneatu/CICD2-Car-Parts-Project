import aio_pika
import asyncio
import json
import os

RABBIT_URL = os.getenv("RABBIT_URL")

async def main():
    connection = await aio_pika.connect_robust(RABBIT_URL)
    channel = await connection.channel()

    queue = await channel.declare_queue("parts_queue", durable=True)
    print("Waiting for messages on 'parts_queue'...")

    async with queue.iterator() as q:
        async for message in q:
            async with message.process():
                data = json.loads(message.body)
                print("Received:", data)

if __name__ == "__main__":
    asyncio.run(main())
