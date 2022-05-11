# wschat/chat/consumers.py
import json

from channels.generic.websocket import AsyncWebsocketConsumer


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        """
        self.scope['url_route']['kwargs']['room_name']
        Получает 'room_name'параметр из URL-маршрута chat/routing.py, 
        который открыл соединение WebSocket с потребителем.
        Каждый потребитель имеет область, которая содержит информацию 
        о его подключении, включая, в частности, любые позиционные или 
        ключевые аргументы из маршрута URL и текущего аутентифицированного 
        пользователя, если таковой имеется. 
        """
        self.room_group_name = f'chat_{self.room_name}'
        """
        Создает имя группы каналов непосредственно из указанного пользователем 
        имени комнаты без каких-либо кавычек или экранирования.
        Имена групп могут содержать только буквы, цифры, дефисы и точки. Поэтому 
        этот пример кода не будет работать с именами комнат, содержащими другие 
        символы.
        """

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data=None, bytes_data=None):
        """
        Receive message from WebSocket
        """
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    async def chat_message(self, event):
        """
        Receive message from room group
        """
        message = event['message']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message
        }))

