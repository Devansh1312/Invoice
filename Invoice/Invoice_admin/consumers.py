import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth.models import AnonymousUser
from asgiref.sync import sync_to_async
import logging
from datetime import datetime
import pytz

logger = logging.getLogger(__name__)

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        try:
            self.room_id = self.scope['url_route']['kwargs']['room_id']
            self.room_group_name = f'chat_{self.room_id}'
            
            # Get user from scope
            user = self.scope.get('user')
            
            if not user or user.is_anonymous:
                logger.error("Anonymous user attempted to connect")
                await self.close()
                return
            
            # Verify user has access to the room
            has_access = await self.verify_user_access(user.id, self.room_id)
            if not has_access:
                logger.error(f"User {user.id} denied access to room {self.room_id}")
                await self.close()
                return
            
            # Join room group
            await self.channel_layer.group_add(
                self.room_group_name,
                self.channel_name
            )
            
            await self.accept()
            logger.info(f"User {user.username} connected to room {self.room_id}")
            
            # Send connection success message
            await self.send(text_data=json.dumps({
                'type': 'connection_established',
                'room_id': self.room_id,
                'message': 'Connected to chat room'
            }))
            
        except Exception as e:
            logger.error(f"Error in connect: {e}")
            await self.close()

    async def disconnect(self, close_code):
        try:
            # Leave room group
            await self.channel_layer.group_discard(
                self.room_group_name,
                self.channel_name
            )
            logger.info(f"User disconnected from room {self.room_id} with code {close_code}")
        except Exception as e:
            logger.error(f"Error in disconnect: {e}")

    async def receive(self, text_data):
        try:
            text_data_json = json.loads(text_data)
            message = text_data_json.get('message', '').strip()
            message_type = text_data_json.get('type', 'message')
            
            if not message and message_type == 'message':
                return
            
            user = self.scope['user']
            
            if message_type == 'message':
                # Save message to database
                message_obj = await self.save_message(self.room_id, user.id, message)
                
                # Send message to room group
                await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                        'type': 'chat_message',
                        'message': message,
                        'user_id': user.id,
                        'username': user.username,
                        'message_id': message_obj.id,
                        'created_at': message_obj.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                        'read': False,
                    }
                )
            elif message_type == 'ping':
                # Handle ping/pong for connection keep-alive
                await self.send(text_data=json.dumps({
                    'type': 'pong',
                    'timestamp': text_data_json.get('timestamp')
                }))
            
        except json.JSONDecodeError:
            logger.error("Invalid JSON received")
            await self.send(text_data=json.dumps({
                'type': 'error',
                'message': 'Invalid message format'
            }))
        except Exception as e:
            logger.error(f"Error in receive: {e}")
            await self.send(text_data=json.dumps({
                'type': 'error',
                'message': 'Failed to process message'
            }))

    async def chat_message(self, event):
        try:
            # Send message to WebSocket
            await self.send(text_data=json.dumps({
                'type': 'chat_message',
                'message': event['message'],
                'user_id': event['user_id'],
                'username': event['username'],
                'message_id': event['message_id'],
                'created_at': event['created_at'],
                'read': event.get('read', False),
            }))
        except Exception as e:
            logger.error(f"Error in chat_message: {e}")
    
    @database_sync_to_async
    def verify_user_access(self, user_id, room_id):
        try:
            from Invoice_admin.models import User, ChatRoom
            user = User.objects.get(id=user_id)
            room = ChatRoom.objects.get(id=room_id)
            
            # Check if user is participant or has admin access
            if room.participants.filter(id=user_id).exists():
                return True
            
            # Check if user is the creator
            if room.created_by_id == user_id:
                room.participants.add(user)
                return True
            
            # Auto-add user if they have admin privileges
            if hasattr(user, 'role') and user.role and user.role.id in [1, 3]:
                room.participants.add(user)
                return True
                
            return False
            
        except Exception as e:
            logger.error(f"Error verifying user access: {e}")
            return False
    
    @database_sync_to_async
    def save_message(self, room_id, user_id, message):
        try:
            from Invoice_admin.models import ChatRoom, ChatMessage, User

            room = ChatRoom.objects.get(id=room_id)
            user = User.objects.get(id=user_id)

            # Get current Saudi time and remove tzinfo to make it naive
            riyadh_now = datetime.now(pytz.timezone('Asia/Riyadh')).replace(tzinfo=None)

            message_obj = ChatMessage.objects.create(
                room=room,
                sender=user,
                message=message,
                created_at=riyadh_now,
                updated_at=riyadh_now
            )
            return message_obj
        except Exception as e:
            logger.error(f"Error saving message: {e}")
            raise