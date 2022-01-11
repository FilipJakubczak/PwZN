import trio
from itertools import count

PORT = 12345

CONNECTION_COUNTER = count()

async def server(server_stream):
    id = next(CONNECTION_COUNTER)
    print("Server {}: uruchomiono".format(id))
    try:
        async for data in server_stream:
            print("Server {}: otrzymano {}".format(id, data))
            await server_stream.send_all(data)
        print("Server {}: połączenie zakończone".format(id))
    except Exception as exc:
        print("Server {}: spadłem z rowerka: {}".format(id, exc))

async def main():
    await trio.serve_tcp(server, PORT)

trio.run(main)