import sys
import asyncio
import signal

async def run_robot(start_from):
    count = start_from
    while True:
        print(count)
        count += 1
        await asyncio.sleep(1)

async def main():
    start_from = int(sys.argv[1]) if len(sys.argv) > 1 else 0
    try:
        await run_robot(start_from)
    except asyncio.CancelledError:
        pass

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    task = loop.create_task(main())

    def signal_handler(sig, frame):
        task.cancel()

    signal.signal(signal.SIGINT, signal_handler)

    try:
        loop.run_until_complete(task)
    finally:
        loop.close()
