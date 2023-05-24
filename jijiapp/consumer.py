# from channels.generic.websocket import AsyncWebsocketConsumer

# class InboxConsumer(AsyncWebsocketConsumer):
#     async def connect(self):
#         self.user = self.scope['user']
#         self.room_group_name = f'inbox_{self.user.id}'

#         # Join the room group
#         await self.channel_layer.group_add(
#             self.room_group_name,
#             self.channel_name
#         )

#         await self.accept()

#     async def disconnect(self, close_code):
#         # Leave the room group
#         await self.channel_layer.group_discard(
#             self.room_group_name,
#             self.channel_name
#         )

#     async def receive(self, text_data):
#         message = json.loads(text_data)
#         if message['type'] == 'message.count':
#             count = message['count']
#             # Send the message count to the client
#             await self.send(text_data=json.dumps({'count': count}))
