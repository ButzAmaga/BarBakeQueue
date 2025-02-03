import json 
from channels.generic.websocket import WebsocketConsumer, AsyncWebsocketConsumer
from asgiref.sync import async_to_sync
from channels.db import database_sync_to_async
from django.utils.timezone import now
from .models import Message
class ChatConsumer(WebsocketConsumer):
    
    def connect(self):
        
        
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.group_name = f'chat_{self.room_name}'
        
        user = self.scope['user']
        
        if not user.is_authenticated:
            self.close()
        
        async_to_sync(self.channel_layer.group_add)(
            self.group_name,
            self.channel_name
        )
        
        self.accept()
        
    
    
    
    def disconnect(self, code):
        
        async_to_sync(self.channel_layer.group_discard)(
            self.group_name, self.channel_name
        )
        
        pass
        # return super().disconnect(code)
    
    def receive(self, text_data=None, bytes_data=None):
        
        # convert the json into python dict
        data_json = json.loads(text_data)
        
        # access the message key
        message = data_json['message']
        
        message_instance = Message(sender = self.user)
        
        '''
        # send a message to the user
        self.send(
            text_data = json.dumps( { 
                'type' : 'chat',
                'message' : message} )
        )
        '''
        
        async_to_sync(self.channel_layer.group_send)(
            self.group_name, 
            { 
                'type' : 'send_message', # method name to execute,
                'message' : message, # data to passed in method event variable
                'message_instance' : message_instance
            }
        )  
        #return super().receive(text_data, bytes_data)
        
    
    def send_message(self, event):
        message = event['message']
        
        self.send(json.dumps({
            'type': 'chat',
            'message': message
        }))    

class Async_ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.group_name = f'chat_{self.room_name}'
        
        self.user = self.scope['user']
        
        # checks if the user is logged in 
        if not self.user.is_authenticated:
            await self.close()
        
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )
        
        await self.accept()
    
    
    async def disconnect(self, code):
        
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )
        
    
    async def receive(self, text_data=None, bytes_data=None):
        
       data = json.loads(text_data)
       
       data['user'] = str(self.user)
       
       message_instance = Message(sender = self.user)
        
       await self.channel_layer.group_send(
           self.group_name, 
           { 
                'type' : 'send_message',
                'data' : data,
                'message_instance' : message_instance 
           }
       )
       
    async def send_message(self, event):
        
        data = event['data']
        data['type'] = 'chat'
        
        message_instance = event['message_instance']
        message_instance.receiver = self.user # bind the recipient
        message_instance.created = now()
        
        print(message_instance)
        
       
        await self.send(
            text_data= json.dumps(data)
        )
       
       
        
        
    