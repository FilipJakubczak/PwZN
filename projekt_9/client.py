import sys
import trio

PORT = 12345

async def sender(stream):
    print("Nadawca: uruchomiono")
    while True:
        data = b"Pozdrowienia dla Doktora Mrowinskiego!"
        print("Nadawca: wysyłanie {}".format(data))
        await stream.send_all(data)
        await trio.sleep(1)

async def receiver(stream):
    print("Odbiorca: uruchumiono")
    async for data in stream:
        print("Odbiorca: otrzymano {}".format(data))
    print("Odbiorca: połączenie zakończone")
    sys.exit()

async def parent():
    print("Łączenie z 127.0.0.1:{}".format(PORT))
    stream = await trio.open_tcp_stream("127.0.0.1", PORT)
    async with stream:
        async with trio.open_nursery() as nursery:
            print("Tworzenie nadawcy...")
            nursery.start_soon(sender, stream)

            print("Tworzenie odbiorcy...")
            nursery.start_soon(receiver, stream)

trio.run(parent)