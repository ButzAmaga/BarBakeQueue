import json 
from channels.generic.websocket import WebsocketConsumer, AsyncWebsocketConsumer
from asgiref.sync import async_to_sync, sync_to_async
from channels.db import database_sync_to_async
from django.contrib.auth.models import User
from django.utils.timezone import now
from .models import Message
from django.db.models import Q
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
        
                    
        # get the user user group
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

            Get the messages from the user
        '''
        
        
        self.target_user = await self.get_target_user()
        
        async for message in Message.objects.select_related("user").filter(user = self.target_user).order_by('created_at'):
            
            '''
                check if the message is owned by the channel owner, if not then she/he recieved the message
            '''
            
            sender , is_align_end = self.get_sender_and_align_connect(message=message)         

            # Render HTML template with message data
            html_content = render_to_string("chat/chat_instance.html", {
                "message":  message.message,
                "sender": sender, 
                "align_end" : is_align_end
            })
        
            # await asyncio.sleep(1)  # ✅ Yields control to other tasks
            await self.send(text_data=html_content)
        

    def get_sender_and_align_connect(self, message):
        if self.user_type.name == 'Staff':
                
            is_align_end = True
            sender = 'Barbakesqueue Staff'

            if message.is_channel_sender:
                is_align_end = False
                sender = message.user
            

        elif self.user_type.name == 'Customer':
            
            is_align_end = False
            sender = 'Barbakesqueue Staff'

            if message.is_channel_sender:
                is_align_end = True
                sender = message.user    
            
        return [sender, is_align_end] 
       
    async def get_target_user(self):
        if self.user_type.name == 'Customer':
            return self.user
        
        elif self.user_type.name == 'Staff':
            ''' Decode the target user using the room name '''
            text = self.room_name
            user_id = int(text.split("_")[-1])
            user = await User.objects.aget(id = user_id)
            
            # the target user to chat with
            return user 
    
    async def disconnect(self, code):
        
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )
        
    
    async def receive(self, text_data=None, bytes_data=None):
        
       data = json.loads(text_data)
        
       print(data) 
       # store the sender name 
       data['sender'] = self.user.id
       
       
       '''
            Save the Message to the database
       '''
       
       if self.target_user == self.user:
           channel_sender = True 
       else:
           channel_sender = False
           
           
       # save to the database
       message = await database_sync_to_async(Message.objects.create)(  
            user = self.target_user,
            message = data['message'],
            is_channel_sender = channel_sender
       )
       
       
       '''
            group_send only supports JSON-serializable data.
       '''
       await self.channel_layer.group_send(
           self.group_name, 
           { 
                'type' : 'send_message',
                'data' : data,

           }
       )
       
    async def send_message(self, event):
        '''
            Message, implement the user and determine the is_sender through group permission?
        '''
        data = event['data']
        
        # get the sender account 
        sender = await User.objects.aget(id = data['sender'])
        
        # get message alignment
        if sender == self.user:
            # own message
            is_align_end = True
        else:
            # received message
            is_align_end = False        
            
        # get the sender name
        group = await sender.groups.afirst()
        if group.name == 'Customer':
            sender_name = sender
        else:
            sender_name = "Barbakesqueue Staff"
            
            
        # Render HTML template with message data
        html_content = render_to_string("chat/chat_instance.html", {
            "message": data['message'],
            "sender": sender_name, 
            "align_end" : is_align_end
        })
       
        await self.send(
            text_data= html_content.strip()
        )
       
       
        
        
    