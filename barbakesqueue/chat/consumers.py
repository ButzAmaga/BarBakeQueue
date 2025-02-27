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
            await self.close()
        
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )
        
        # accept the connection 
        await self.accept()
        
        condition = Q(sender = self.user.id) | Q(receiver = self.user.id)
        async for message in Message.objects.select_related("sender", "receiver").filter(condition).order_by('created_at'):
            
            if message.sender.id != self.user.id:
                is_receiver = True
            else:
                is_receiver = False        


            # Render HTML template with message data
            html_content = render_to_string("chat/chat_instance.html", {
                "message":  message.message,
                "sender": message.sender, 
                "is_receiver" : is_receiver
            })
            print(message.created_at)
            # await asyncio.sleep(1)  # ✅ Yields control to other tasks
            await self.send(text_data=html_content)
        
   
        
        
    @database_sync_to_async
    def get_messages(self):
        return Message.objects.all()

           
    async def get_old_messages(self):
        '''
            sync_to_async create a seperate thread and runs the  in sync within it, if two instructions are executed within that
            then in seperate thread run the two instructions in sync manner
        '''
        
        ''' 
            get all old messages
            database_sync_to_async runs in seperated thread so the instruction below this will be executed without waiting for this
            to complete unless the instruction is wrap into sync_to_async which is also runs in different thread
            and will wait to other similar execution like the database sync_to_async
        '''
        condition = Q(sender = self.user) | Q(receiver = self.user)
        old_message = await database_sync_to_async(Message.objects.filter)(condition)

        print("Getting old messages") 
        '''
            
        '''
        await sync_to_async(print)(old_message)
        
        def send_messages(messages):
            for message in messages:
                
                if message.sender != self.user:
                    is_receiver = True
                else:
                    is_receiver = False        

                # Render HTML template with message data
                html_content = render_to_string("chat/chat_instance.html", {
                    "message": message.message,
                    "sender": str(message.sender), 
                    "is_receiver" : is_receiver
                })
                
                print(html_content)
                self.send(text_data=html_content)
                
        await sync_to_async(send_messages)(old_message)
       
            
    
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
        
        data = event['data']
        data['type'] = 'chat'
        
        
        if event["sender_id"] != self.user.id:
            
            sender = await database_sync_to_async(User.objects.get)(
                id = event["sender_id"]
            )
            
            '''
                message not saved to the database unless a reciver caught the message
            '''
            new_message = await database_sync_to_async(Message.objects.create)(
                sender = sender,
                receiver = self.user,
                message = data['message']
            )
            print(new_message)

       
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
       
       
        
        
    