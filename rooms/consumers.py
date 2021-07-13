import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from .models import Message, Room
from accounts.models import CustomUser
from django.shortcuts import get_object_or_404
from channels.generic.websocket import AsyncWebsocketConsumer

class ChatConsumer(WebsocketConsumer):

    def fetch_messages(self,data):
        code = data['room_code']
        room = get_object_or_404(Room, code=code)
        messages = Message.objects.filter(room=room).reverse()
        content = {
            'command': 'messages',
            'message': self.messages_to_json(messages)
        }
        self.send_message(content)

    def new_message(self,data):
        author = data['from']
        author_user = get_object_or_404(CustomUser, id=author)
        code = data['room_code']
        room = get_object_or_404(Room, code=code)
        message = Message.objects.create(
            author = author_user,
            message = data['message'],
            room = room
        )
        content = {
            'command': 'new_message',
            'message': self.message_to_json(message)
        }
        return self.send_chat_message(content)
        

    def messages_to_json(self, messages):
        result = []
        if(len(messages)>0):
            message_date = str(messages[0].timestamp).split()[0]
            result.append({
                'date': messages[0].timestamp.strftime("%d/%m/%y")
            })
        for message in messages:
            cur_msg_date = str(message.timestamp).split()[0]
            if(message_date != cur_msg_date):
                message_date = cur_msg_date
                result.append({
                    'date': message.timestamp.strftime("%d/%m/%y")
                })
            result.append(self.message_to_json(message))
        return result

    def message_to_json(self, message1):
        return {
            'author': message1.author.email,
            'message': message1.message,
            'timestamp': message1.timestamp.strftime("%I:%M %p"),
            'author_name': message1.author.profile.name,
            'author_id': message1.author.id,
            'author_pic': str(message1.author.profile.profile_pic)
        }

    commands = {
        'fetch_messages': fetch_messages,
        'new_message':new_message
    }

    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_code']
        self.room_group_name = 'chat_%s' % self.room_name

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        data = json.loads(text_data)
        self.commands[data['command']](self, data)
    
    def send_chat_message(self, message):
        
        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    def send_message(self, message):
        self.send(text_data=json.dumps(message))

    # Receive message from room group
    def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        self.send(text_data=json.dumps(message))



class CallConsumer(AsyncWebsocketConsumer):
    
    async def connect(self):
        
        self.room_group_name = self.scope['url_route']['kwargs']['room_code']

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

        print('Disconnected!')
        

    # Receive message from WebSocket
    async def receive(self, text_data):
        receive_dict = json.loads(text_data)
        message = receive_dict['message']
        action = receive_dict['action']

        if(action == 'new-offer' or action == 'new-answer'):
            receiver_channel_name = receive_dict['message']['receiver_channel_name']

            receive_dict['message']['receiver_channel_name'] = self.channel_name

            await self.channel_layer.send(
                receiver_channel_name,
                {
                    'type': 'send.sdp',
                    'recieve_dict': receive_dict
                }
            )


            return

        receive_dict['message']['receiver_channel_name'] = self.channel_name
        
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'send.sdp',
                'recieve_dict': receive_dict
            }
        )

    async def send_sdp(self, event):
        recieve_dict = event['recieve_dict']

        await self.send(text_data=json.dumps(recieve_dict))