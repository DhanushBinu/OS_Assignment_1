import grpc
import asyncio
from Proto_Gen_Code import service_pb2
from Proto_Gen_Code import service_pb2_grpc
import uuid
import argparse
import logging

class ClientCode:
    def __init__(self, client_id, server_ip, port) -> None:
        self.client_id = client_id
        self.server_address = f'{server_ip}:{port}'
        self.username = f'Client-{client_id}'
        self.channel = grpc.aio.insecure_channel(self.server_address)
        self.stub = service_pb2_grpc.Server_ServiceStub(self.channel)
        self.connected = False

    async def Connect(self, username):
        self.connected = True
        self.username = username
        connect_2 = service_pb2.Connect_2(
            user_id=self.client_id,
            user_name=username,
        )
        responses = self.stub.Connect(connect_2)
        async for response in responses:
            if(response.user_name == "Server"):
                logging.info(self.username + " received " + response.user_response)
            else:
                logging.info(self.username + " Downloaded unread message " + response.user_response)

    async def Send_Message(self, username, message):
        send_message_1 = service_pb2.Request(
            user_name=username,
            user_message=message,
        )
        self.stub.Send_message(send_message_1)

    async def Receive_message(self, username):
        while True:
            receive_message = service_pb2.Connect_1(
                user_name=self.username
            )
            responses = self.stub.Send_Message_to_all(receive_message)
            async for response in responses:
                logging.info(self.username + " received " + response.user_response)

    async def input_thread(self):
        while self.connected:
            message = await asyncio.to_thread(input, "")
            print()
            if message == 'exit':
                self.connected = False
                await self.channel.close()
                break
            await self.Send_Message(self.username, message)

    async def start(self):
        if not self.connected:
            print("Please connect first.")
            return

        receive_message_coro = self.Receive_message(self.username)

        input_coro = self.input_thread()

        await asyncio.gather(receive_message_coro, input_coro)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Client for chat application')
    parser.add_argument('-client_id', type=int, required=True, help='Client ID')
    parser.add_argument('-server_ip', type=str, required=True, help='Server IP address')
    parser.add_argument('-port', type=int, required=True, help='Server port')
    parser.add_argument('-log_path', type=str, required=True, help="Log file path")
    args = parser.parse_args()

    logging.basicConfig(filename=args.log_path, level=logging.INFO, format='%(asctime)s - %(message)s')
    client = ClientCode(args.client_id, args.server_ip, args.port)
    
    loop = asyncio.get_event_loop()
    username = loop.run_until_complete(asyncio.to_thread(input, ""))

    loop.run_until_complete(client.Connect(username))
    loop.run_until_complete(client.start())





