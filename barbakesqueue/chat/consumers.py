import json 
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync

class ChatConsumer(WebsocketConsumer):
    
    def connect(self):
        
        
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.group_name = f'chat_{self.room_name}'
        
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
                'message' : message # data to passed in method event variable
            }
        )  
        #return super().receive(text_data, bytes_data)
        
    
    def send_message(self, event):
        message = event['message']
        
        self.send(json.dumps({
            'type': 'chat',
            'message': message
        }))    