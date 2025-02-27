import json 
from channels.generic.websocket import WebsocketConsumer, AsyncWebsocketConsumer
from asgiref.sync import async_to_sync, sync_to_async
from channels.db import database_sync_to_async
from django.contrib.auth.models import User
from django.utils.timezone import now
from .models import Message
from django.db.models import Q
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

from django.template.loader import render_to_string

class Async_ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.group_name = f'chat_{self.room_name}'
        
        self.user = self.scope['user']
        
        # checks if the user is logged in 
        if not self.user.is_authenticated:
            
            self.send(json.dumps({
                'type' : 'login_required',
                'message': 'Please log in an account to access the chat features'
            }))

            
            await self.close()
        
                    
        # get the user first user group
        self.user_type = await self.user.groups.afirst()
        
        # add to channel
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )
        
        # accept the connection 
        await self.accept()
        
        '''
            if user is customer then let condition to self.user, if user is staff, decode the user and use it as filter id
        '''
        
        if self.user_type.name == 'Customer':
            user_id = self.user
        elif self.user_type.name == 'Staff':
            text = self.room_name
            user_id = int(text.split("_")[-1])
            user = await User.objects.aget(id = user_id)
            
            # the target user to chat with
            user_id = user 
        
        async for message in Message.objects.select_related("user").filter(user = user_id).order_by('created_at'):
            
            '''
                check if the message is owned by the channel owner, if not then she/he recieved the message
            '''
            if message.is_channel_sender != False:
                is_receiver = True
                sender = 'Barbakesqueue Staff'
            else:
                is_receiver = False        
                sender = self.user


            # Render HTML template with message data
            html_content = render_to_string("chat/chat_instance.html", {
                "message":  message.message,
                "sender": sender, 
                "is_receiver" : is_receiver
            })
        
            # await asyncio.sleep(1)  # ✅ Yields control to other tasks
            await self.send(text_data=html_content)
        

            
    
    async def disconnect(self, code):
        
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )
        
    
    async def receive(self, text_data=None, bytes_data=None):
        
       data = json.loads(text_data)
        
       print(data) 
       # store the sender name 
       data['sender'] = str(self.user)
       
       
       '''
            Save the Message to the database
       '''

       
       if self.user_type.name == "Customer":
           user = self.user
           is_channel_sender = True 
       elif self.user_type.name == 'Staff':
    
           is_channel_sender = False
           
           '''
               get the user account of receiver, optimize this by saving it as global
           '''
           text = self.room_name
           user_id = int(text.split("_")[-1])
           user = await User.objects.aget(id = user_id)
       
       else:
           print('Invalid user')
           self.close()    
           
       # save to the database
       message = await database_sync_to_async(Message.objects.create)(  
            user = user,
            message = data['message'],
            is_channel_sender = is_channel_sender
       )
       
       
       '''
           check if the message is owned by the channel owner, if not then she/he recieved the message
       '''
       if self.user_type.name != 'Customer':
           is_receiver = True
           sender = 'Barbakesqueue Staff'
       else:
           is_receiver = False        
           sender = self.user
       
       '''
            group_send only supports JSON-serializable data.
       '''
       await self.channel_layer.group_send(
           self.group_name, 
           { 
                'type' : 'send_message',
                'data' : data,
                'sender_id' : self.user.id
           }
       )
       
    async def send_message(self, event):
        '''
            Message, implement the user and determine the is_sender through group permission?
        
        '''
        data = event['data']
        
        # add attribute type chat
        data['type'] = 'chat'
        
            
        if event["sender_id"] != self.user.id:
            is_receiver = True
        else:
            is_receiver = False        
            
        # Render HTML template with message data
        html_content = render_to_string("chat/chat_instance.html", {
            "message": data['message'],
            "sender": data['sender'], 
            "is_receiver" : is_receiver
        })
       
        await self.send(
            text_data= html_content.strip()
        )
       
       
        
        
    